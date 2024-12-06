import logging
import threading
import traceback
from concurrent import futures
from pathlib import Path

import grpc
import jax
import numpy as np
import typer

from . import proto
from .common import get_dtype, decode_image, TokenValidationInterceptor

app = typer.Typer(pretty_exceptions_enable=False)

_MAX_MSG_SIZE=1024*1024*128
_TARGET_CELL_SIZE=32


def process_input(request: proto.DetectionRequest):
    pixels = request.image_data.pixels
    settings = request.detection_settings

    image = decode_image(pixels)

    physical_size = np.array([
        pixels.physical_size_z or pixels.physical_size_x, # one might set xy but not z
        pixels.physical_size_y, 
        pixels.physical_size_x,
    ], dtype="float")
    if (physical_size == 0).any():
        physical_size[:] = 1.0

    if settings.HasField("cell_diameter_hint"):
        scaling = _TARGET_CELL_SIZE / settings.cell_diameter_hint * physical_size

    else:
        if physical_size[1] != physical_size[2]:
            raise ValueError("Scaling hint provided, but pixel is not isometric")

        scaling = np.array([ settings.scaling_hint or 1.0 ] * 3, dtype="float")
        scaling[0] *= physical_size[0] / physical_size[1] 
    
    logging.info(f"Requested rescaling factor is {scaling}")

    shape_hint = tuple( np.round(scaling * image.shape[:3]).astype(int) )

    if image.shape[0] == 1: # 2D
        image = image.squeeze(0)
        shape_hint = shape_hint[1:]

    kwargs = dict(
        reshape_to = shape_hint,
        score_threshold = settings.min_score or 0.4,
        min_area = settings.min_cell_area,
        nms_iou = settings.nms_iou,
        segmentation_threshold = settings.segmentation_threshold or 0.5,
    )

    return image, kwargs


def process_result(preds, image) -> proto.DetectionResponse:
    response = proto.DetectionResponse()

    if image.ndim == 3: # returns polygon

        for contour, score in zip(preds["pred_contours"], preds["pred_scores"]):
            if len(contour) == 0:
                continue

            scored_roi = proto.ScoredROI(
                score = score,
                roi = proto.ROI(
                    polygon = proto.Polygon(points = [proto.Point(x=p[0], y=p[1]) for p in contour]),
                )
            )

            response.detections.append(scored_roi)

    else: # 3d returns Mesh
        for mesh, score in zip(preds["pred_contours"], preds["pred_scores"]):
            scored_roi = proto.ScoredROI(
                score = score,
                roi = proto.ROI(
                    mesh = proto.Mesh(
                        verts = [proto.Point(z=v[0], y=v[1], x=v[2]) for v in mesh['verts']],
                        faces = [proto.Mesh.Face(p1=p[0], p2=p[1], p3=p[2]) for p in mesh['faces']],
                    ),
                )
            )

            response.detections.append(scored_roi)

    return response


class LacssServicer(proto.LacssServicer):

    def __init__(self, model, max_image_size, max_image_size_3d):
        self.model = model
        self.max_image_size = max_image_size
        self.max_image_size_3d = max_image_size_3d

        self._lock = threading.RLock()

    def RunDetection(self, request, context):
        with self._lock:

            logging.info(f"Received message of size {request.ByteSize()}")

            try:
                image, kwargs = process_input(request)

                reshape_to = kwargs["reshape_to"]

                if image.ndim == 4:
                    is_img_too_big = max(reshape_to) > self.max_image_size_3d
                else:
                    is_img_too_big = max(reshape_to) > self.max_image_size

                if is_img_too_big:
                    raise ValueError("image size exeeds limit")

                logging.info(f"received image {image.shape}")

                # dont' reshape image if the request is almost same as the orginal 
                rel_diff = np.abs(np.array(reshape_to) / image.shape[:-1] - 1)
                if (rel_diff < 0.1).all():
                    kwargs['reshape_to'] = None

                preds = self.model.predict(
                    image, output_type="contour", **kwargs,
                )

                response = process_result(preds, image)

                logging.info(f"Reply with message of size {response.ByteSize()}")

                return response
            
            except ValueError as e:
                
                logging.error(repr(e))

                logging.error(traceback.format_exc())

                context.abort(grpc.StatusCode.INVALID_ARGUMENT, repr(e))

            except Exception as e:

                logging.error(repr(e))

                logging.error(traceback.format_exc())

                context.abort(grpc.StatusCode.UNKNOWN, f"prediction failed with error: {repr(e)}")



    def RunDetectionStream(self, request_iterator, context):
        with self._lock:
            request = proto.DetectionRequest()

            for next_request in request_iterator:

                if next_request.image_data.HasField("pixels"):
                    request.image_data.pixels.CopyFrom(next_request.image_data.pixels)

                if next_request.image_data.HasField("image_annotation"):
                    request.image_data.image_annotation.CopyFrom(next_request.image_data.image_annotation)
                
                if next_request.HasField("detection_settings"):
                    request.detection_settings.CopyFrom(next_request.detection_settings)
                
                if request.image_data.HasField("pixels"):
                    yield self.RunDetection(request, context)


def get_predictor(modelpath):
    from .predict import Predictor

    model = Predictor(modelpath)

    logging.info(f"lacss_server: loaded model from {modelpath}")

    model.module.detector.max_output = 512  # FIXME good default?
    model.module.detector.min_score = 0.05

    logging.debug(f"lacss_server: precompile for most common shapes")

    _ = model.predict(np.ones([512,512,3]), output_type="contour")
    _ = model.predict(np.ones([1088,1088,3]), output_type="contour")
    _ = model.predict(np.ones([256,256,256,3]), output_type="contour")

    return model


def show_urls():
    from . import model_urls
    
    print("Pretrained model files:")
    print("==============================")
    for k, v in model_urls.items():
        print(f"{k}: {v}")
    print()


@app.command()
def main(
    modelpath: Path|None = None,
    port: int = 50051,
    workers: int = 10,
    ip: str = "0.0.0.0",
    local: bool = False,
    token: bool|None = None,
    debug: bool = False,
    compression: bool = True,
    max_image_size: int = 1088,
    max_image_size_3d: int = 512,
):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    if modelpath is None:
        show_urls()
        return

    print ("server starting ...")

    model = get_predictor(modelpath)

    logging.info(f"lacss_server: default backend is {jax.default_backend()}")

    if jax.default_backend() == "cpu":
        logging.warning(
            f"lacss_server: WARNING: No GPU configuration. This might be very slow ..."
        )

    if token is None:
        token = not local
    if token:
        import secrets

        token_str = secrets.token_urlsafe(64)

        print()
        print("COPY THE TOKEN BELOW FOR ACCESS.")
        print("=======================================================================")
        print(f"{token_str}")
        print("=======================================================================")
        print()
    else:
        token_str = None

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=workers),
        compression=grpc.Compression.Gzip if compression else grpc.Compression.NoCompression,
        interceptors=(TokenValidationInterceptor(token_str),),
        options=(("grpc.max_receive_message_length", _MAX_MSG_SIZE),),
    )

    proto.add_LacssServicer_to_server(
        LacssServicer(
            model,
            max_image_size,
            max_image_size_3d,
        ), 
        server,
    )

    if local:
        server.add_secure_port(f"127.0.0.1:{port}", grpc.local_server_credentials())
    else:
        server.add_insecure_port(f"{ip}:{port}")

    logging.info(f"lacss_server: listening on port {port}")

    print ("server starting ... ready")

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    # jax.config.update("jax_compilation_cache_dir", "jax_cache")
    # jax.config.update("jax_persistent_cache_min_entry_size_bytes", -1)
    # jax.config.update("jax_persistent_cache_min_compile_time_secs", 5)
    app()

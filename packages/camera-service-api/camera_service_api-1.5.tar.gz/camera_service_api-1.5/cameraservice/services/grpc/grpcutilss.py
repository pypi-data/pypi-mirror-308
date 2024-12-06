from datetime import datetime
from typing import List, Union

from cameraservice.services.cameras.camera_provider import CameraMeta
from cameraservice.services.grpc import camera_service_pb2 as service_pb2
from cameraservice.services.grpc.pb2utils import value_or_empty

from cameraservice.services.cameras.models import ImageShape, ImageRequest

class local_to_pb2:
    @staticmethod
    def to_CameraMeta(s: CameraMeta) -> service_pb2.CameraMeta_:
        x = service_pb2.CameraMeta_()
        x.cameraType = value_or_empty(s.cameraType)
        x.serialNumber = value_or_empty(s.serialNumber)  # value_or_empty_dict(s, 'name')
        x.modelName = value_or_empty(s.modelName)
        x.manufactureName = value_or_empty(s.manufactureName)
        x.deviceVersion = value_or_empty(s.deviceVersion)
        x.userDefinedName = value_or_empty(s.userDefinedName)
        x.address = value_or_empty(s.address)
        if s.info is not None:
            for kk in s.info:
                vv = s.info[kk]
                x.info[kk] = vv

        return x

    @staticmethod
    def to_CameraMetas(metas: List[CameraMeta]) -> service_pb2.CameraMetas:
        output = []
        if metas is not None and len(metas) > 0:
            for a in metas:
                output.append(local_to_pb2.to_CameraMeta(a))

        return service_pb2.CameraMetas(status=0, message="", data=output)

    @staticmethod
    def to_ImageResponse_( content: bytes , status=0, message="" ) -> service_pb2.ImageResponse_:
        x = service_pb2.ImageResponse_(content=content, status=status, message=message)
        return x

    @staticmethod
    def to_ImageShape(imageShape: ImageShape) -> service_pb2.ImageShape_:
        x = service_pb2.ImageShape_(width=imageShape.width, height=imageShape.height,
                                    channel=imageShape.channel, imageType=imageShape.image_type,
                                    quality=imageShape.quality, method=imageShape.method)
        return x

    @staticmethod
    def to_ImageRequest(sn: str, imageShape: ImageShape) -> service_pb2.ImageRequest_:
        x = service_pb2.ImageRequest_(sn = sn, imageShape=local_to_pb2.to_ImageShape(imageShape))
        return x
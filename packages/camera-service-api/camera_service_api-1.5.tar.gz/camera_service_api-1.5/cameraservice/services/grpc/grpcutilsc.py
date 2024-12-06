from datetime import datetime
from typing import List, Union

from cameraservice.services.cameras.camera_provider import CameraMeta
from cameraservice.services.grpc import camera_service_pb2 as service_pb2

from cameraservice.services.cameras.models import ImageShape, ImageRequest
from cameraservice.util.exceptions import ErrorCode, ErrorException


class pb2_to_local:

    @staticmethod
    def to_ImageRequest(s: service_pb2.ImageRequest_) -> (str, ImageShape):
        sn = s.sn
        imageShape = ImageShape(shape=(s.imageShape.width, s.imageShape.height, s.imageShape.channel))

        return sn, imageShape

    @staticmethod
    def to_CameraMeta(s: service_pb2.CameraMeta_) -> CameraMeta:
        x = CameraMeta()
        x.cameraType = s.cameraType
        x.serialNumber = s.serialNumber  # value_or_empty_dict(s, 'name')
        x.modelName = s.modelName
        x.manufactureName = s.manufactureName
        x.deviceVersion = s.deviceVersion
        x.userDefinedName = s.userDefinedName

        for key in s.info:
            x.info[key] = s.info[key]

        return x


    @staticmethod
    def to_CameraMetas(metas: service_pb2.CameraMetas) -> List[CameraMeta]:

        if metas.status != ErrorCode.ok:
            raise ErrorException(metas.status, metas.message )

        output = []
        inp = metas.data
        if inp is None or len(inp) == 0:
            return output;
        for a in inp:
            output.append(pb2_to_local.to_CameraMeta(a))
        return output

    # @staticmethod
    # def to_Bytes (s: service_pb2.BytesBody) -> bytes :
    #     return s.content

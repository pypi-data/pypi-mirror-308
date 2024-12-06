from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraMeta_(_message.Message):
    __slots__ = ("serialNumber", "modelName", "manufactureName", "deviceVersion", "userDefinedName", "cameraType", "address", "info")
    class InfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SERIALNUMBER_FIELD_NUMBER: _ClassVar[int]
    MODELNAME_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURENAME_FIELD_NUMBER: _ClassVar[int]
    DEVICEVERSION_FIELD_NUMBER: _ClassVar[int]
    USERDEFINEDNAME_FIELD_NUMBER: _ClassVar[int]
    CAMERATYPE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    serialNumber: str
    modelName: str
    manufactureName: str
    deviceVersion: str
    userDefinedName: str
    cameraType: str
    address: str
    info: _containers.ScalarMap[str, str]
    def __init__(self, serialNumber: _Optional[str] = ..., modelName: _Optional[str] = ..., manufactureName: _Optional[str] = ..., deviceVersion: _Optional[str] = ..., userDefinedName: _Optional[str] = ..., cameraType: _Optional[str] = ..., address: _Optional[str] = ..., info: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CameraMetas(_message.Message):
    __slots__ = ("status", "message", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    data: _containers.RepeatedCompositeFieldContainer[CameraMeta_]
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ..., data: _Optional[_Iterable[_Union[CameraMeta_, _Mapping]]] = ...) -> None: ...

class ImageShape_(_message.Message):
    __slots__ = ("imageType", "width", "height", "channel", "quality", "method")
    IMAGETYPE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    imageType: str
    width: int
    height: int
    channel: int
    quality: int
    method: int
    def __init__(self, imageType: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., channel: _Optional[int] = ..., quality: _Optional[int] = ..., method: _Optional[int] = ...) -> None: ...

class ImageRequest_(_message.Message):
    __slots__ = ("sn", "imageShape")
    SN_FIELD_NUMBER: _ClassVar[int]
    IMAGESHAPE_FIELD_NUMBER: _ClassVar[int]
    sn: str
    imageShape: ImageShape_
    def __init__(self, sn: _Optional[str] = ..., imageShape: _Optional[_Union[ImageShape_, _Mapping]] = ...) -> None: ...

class ImageResponse_(_message.Message):
    __slots__ = ("status", "message", "content")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    status: int
    message: str
    content: bytes
    def __init__(self, status: _Optional[int] = ..., message: _Optional[str] = ..., content: _Optional[bytes] = ...) -> None: ...

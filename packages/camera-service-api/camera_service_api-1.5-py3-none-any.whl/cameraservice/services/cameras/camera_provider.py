from typing import Protocol, List

from cameraservice.services.cameras.models import ImageShape


class CameraMeta:

    def __init__(self):
        '''
          string serialNumber = 1;
          string modelName = 2;
          string manufactureName = 3;
          string deviceVersion = 4;
          string userDefinedName = 5;
          map<string, string> info = 6;
        '''

        self.cameraType = ""
        self.serialNumber = ""
        self.modelName = ""
        self.manufactureName = ""
        self.deviceVersion = ""
        self.userDefinedName = ""
        self.address = ""
        self.info = {}

    def add_info(self, k: str, v: str):
        if self.info is None:
            self.info = {}

        self.info[k] = v

    def get_sn(self):
        return self.serialNumber


class CameraProvider(Protocol):

    # Reset camera
    def reset(self):
        ...

    # 输入 SN（camera 的唯一标识），返回当前图片
    def get_image(self, sn: str, imageShape: ImageShape) -> bytes:
        ...

    # 返回当前服务，支持多少个 摄像头
    def get_camera_metas(self) -> List[CameraMeta]: ...

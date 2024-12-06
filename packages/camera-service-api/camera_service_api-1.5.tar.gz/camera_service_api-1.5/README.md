# Camera service grpc API 



## Install Camerm api 

### Install 

1. using pip install local package 
  
```bash
# Python12 
pip install camera-service-api==1.1.0


# Python7 
pip install camera-service-api==1.1.1


```


### Dependencies 

- grpcio     1.63.0
- protobuf   5.26.1


## Build by proto 

```shell

pip install   grpcio grpcio-tools protobuf

```


## API 



### Get API Instance  `create_camera_service_api`  

- host , camera server host , e.g.  `localhost` 
- port , camera server port , e.g.  `6000`


```python 

# host 
api = create_camera_service_api(host, port)


```
### Get All camera meta infos `get_camera_metas`

```python

def get_camera_metas(self) -> List[CameraMeta]:
    ...     

```

```python

metas = api.get_camera_metas()
for meta in metas:
    print(f"Camera modelName: {meta.modelName} - deviceVersion: {meta.deviceVersion}")
    print("get camera image serialNumber ", meta.serialNumber)
    print("get info ", meta.info)


```

### CameraMeta 

- cameraType , camera type , `GIGE` | `u3v` 
- serialNumber : camera serial number , 
- modelName  : model name 
- manufactureName : manufacture name 
- deviceVersion :  device version 
- userDefinedName : name defined by user 
- info : Map[string,string] , ext info 


### Get live image by serial number 

input camera serial number and return live image (jpg), bytes.
and if return `None` means the camera maybe offline. 

and using `try .. except` for catch `exception` 

```python

def get_image(self, sn: str) -> bytes:
    ...     

```

Example: 

```python

...
body = api.get_image(meta.serialNumber)
print(" body : ", len(body)  )

...

fopen = open('test.jpg', 'wb+')
fopen.write( body )
fopen.close()

...

```


## Example 

```python
import time

import grpc

from services.cameras.camera_service_api import create_camera_service_api


max_test = 100

def test_camera_api(host, port):
    #
    api = create_camera_service_api(host, port)
    metas = api.get_camera_metas()
    for meta in metas:
        print(f"Camera modelName: {meta.modelName} - deviceVersion: {meta.deviceVersion}")
        print("get camera image serialNumber ", meta.serialNumber)
        print("get info ", meta.info)

        t1 = time.time()
        try:
        
            for i in range( max_test ):
                body = api.get_image(meta.serialNumber)
                print(" body : ", i, len(body)  )

        except Exception as e:
            print( e) 

        t2 = time.time()
        tt = t2-t1
        avg = tt / max_test
        print( f" Try {max_test} times get image , using {tt} , avg {avg} ")

        # fopen = open('body.jpg'.encode('utf-8'), 'wb+')
        # fopen.write( body, )
        # fopen.close()

# protect the entry point
if __name__ == '__main__':
    print("GRPC Version : {} ".format(grpc.__version__))
    test_camera_api("127.0.0.1", 6000)



```
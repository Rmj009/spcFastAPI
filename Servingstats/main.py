# main.py 
"""REF:
https://realpython.com/fastapi-python-web-apis/
terminal bash$ uvicorn main:app --reload
"""
import uvicorn
from fastapi import FastAPI, Request
# , File, UploadFile
from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError
from Servingstats.model.models import Capability,Neslson,User
# from tools.spcTable import SpcTable
from Servingstats.tools.gauge import Gauge
# from errors import *
# from config import *

app = FastAPI() #create a FastAPI instance:
"""
# Authorize in the swagger
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/items/") 
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}


@app.get('/v2/nelson-new/',response_model=Neslson)
def GormToNelson(points: str, request: Request):
    client_host = request.client.host
    # print(points)
    # print(type(points))
    try:
        # Capability(points=[33,22,55,22,23,26])
        if (points == None) or (len(points) == 0):
            result = 'PointsInvaild'
            return {"client_host": client_host, "results": result}, 400
        else:
            result = Gauge.nelson(points)
            return JSONResponse(content=str(result)) #status_code=202,

    except ValidationError as e:
        print('validationE',e.json())
    except Exception as errors:
        print('SHOWerror',errors)
    return 'CalcFail', 500


@app.get("/v2/capability-new",response_model=Capability)
def GormToCPR(points,USL,LSL,good,defect,measureAmount,stdValue):
  try:
    if (points == None) or (len(points) == 0):
      result = 'PointsInvaild'
      return result, 400
    elif (USL == None) or (len(USL) == 0):
      result = 'USLInvaild'
      return result, 400
    elif (LSL == None) or (len(LSL) == 0):
      result = 'LSLInvaild'
      return result, 400
    elif (good == None) or (len(good) == 0):
      result = 'GOODInvaild'
      return result, 400
    elif (defect == None) or (len(defect) == 0):
      result = 'DefectInvaild'
      return result, 400
    elif (measureAmount == None) or (len(measureAmount) == 0):
      result = 'measureAmountInvaild'
      return result, 400
    elif (stdValue == None) or (len(stdValue) == 0):
      result = 'StdValueInvaild'
      return result, 400
    else:
      result = Gauge.stats(points,good,defect,LSL,USL,measureAmount,stdValue)
      return JSONResponse(content=str(result)) #status_code=202,

  except ValidationError as e:
        print('validationE',e.json())
  except Exception as errors:
    print('error',errors)
    return 'CalcFail', 500

if __name__ == "__main__":
    uvicorn.run(app, debug=True)
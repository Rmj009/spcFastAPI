# main.py 
"""REF:
https://realpython.com/fastapi-python-web-apis/
terminal bash$ uvicorn main:app --reload
"""
from fastapi import responses
from requests.api import request
import starlette
import uvicorn, time, os, requests, asyncio
from fastapi import FastAPI, Request, Depends
# , File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from starlette.responses import Response

"""
project.components import
"""
from Servingstats.model.models import Capability,Neslson,User
# from Servingstats.tools.spcTable import SpcTable    # fastapi ORM not ready
from Servingstats.tools.gauge import Gauge
# from errors import *
# from config import *


app = FastAPI() #create a FastAPI instance:
app.mount("/static", StaticFiles(directory="Servingstats/static") ,name="static") 
templates = Jinja2Templates(directory="templates")
"""
# Authorize in the swagger
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):

#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     # response.headers["X-Process-Time"] = str(process_time)
#     print('request.headers',request.headers)
#     response.headers["Authorization"] = str(request.headers)
#     print('path: {0}, url: {1} , endpoint:{2}'.format(request.url.path, request.url.scheme, request.body)) #request.endpoint
  
#     header = request.headers
#     endpoint = request.method
#     print("///////////////////")
#     # print('show',header,endpoint)
#     print("///////////////////")
#     if "Authorization" in header: 
#         print("header auth yes")
#         AuthorizationToken =  header['Authorization']
#         is_auth = True
#         # async_check_auth(AuthorizationToken)
#         if is_auth != True:
#           # return render_template('401.html'), 401
#           return templates.TemplateResponse("401.html", {"request": request})

#         else:
#             # app.register_blueprint(app2)
#           return 
    
#     elif ("Authorization" not in header) and ('NelsonAPI'== endpoint or 'CPR'== endpoint):
#       # print("requestendpoint",endpoint)
#       # print("Nelson API or Capability API without BearerAuth", request.endpoint)
#       return templates.TemplateResponse("401.html", {"request": request})

    
#     elif ("Authorization" not in header) and ('app2' or 'static' in endpoint):
#       # print("requestendpoint",endpoint)
#       # print("Nelson API or Capability API without BearerAuth", request.endpoint)
#       # return render_template('401.html'), 401
#       return

#     else:
#       print("NO AUTH header\n")
#       print(" request.url ",  request.url )
#       return templates.TemplateResponse("401.html", {"request": request})

#       print('//////////////',response)
#       return response

# ################################################################################################
# ################################################################################################
# ################################################################################################


# def async_check_auth(AuthorizationToken: str):
#   request: Request
#   # assert scope['type'] == 'http'
#   # request = Request(scope, receive)
#   # content = '%s %s' % (request.method, request.url.path)
#   # response = Response(content, media_type='text/plain')
#   # print("starlette resp" , response )
#   # body = b''
#   # async for chunk in request.stream():
#   #   body += chunk
#   #   response = Response(body, media_type='text/plain')
#   #   print("starlette resp2" , response )
#   # await response(scope, receive, send)


#   url = os.getenv('DZ_TOKEN_PERMISSION')
#   headers = { 'Authorization': AuthorizationToken}
# #   # r = requests.get(url, headers=headers)
#   response = requests.request("GET", url, headers=headers) #, data=payload, files=files)
#   print('BUG2',response.status_code )
#   json_text = response.json()
#   print('JSONTEXT::::::::;',json_text)
#   if (response.status_code == 400):
#     # return render_template('400.html'), 400
#     return templates.TemplateResponse("400.html", {"request": request})

#   elif response.status_code != 200:

#     return False
#     # 400, status.HTTP_400_BAD_REQUEST

#   elif json_text['access'] == True:

#     return True
#     # 400, status.HTTP_400_BAD_REQUEST

#   else:
#     return False


# def auth(request: Request):
  
    # return

################################################################################################
################################################################################################
################################################################################################
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
async def root(string:str):
    return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id": item_id}


@app.get('/v2/nelson-new/',response_model=Neslson)
def GormToNelson(points: str, request: Request):
    client_host = request.client.host
    # auth(request)
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
    uvicorn.run("main:app", debug=True,reload = True,log_level="info")

# uvicorn Servingstats.app.main:app --reload
# gunicorn --chdir . main:app -w 2 --threads 2 -b 0.0.0.0:8000
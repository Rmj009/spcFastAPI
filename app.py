# export DATABASE_URL='postgres://localhost:5432/
from datetime import datetime
import os,html,sys,traceback
from flask import Flask, request, render_template, abort, url_for, redirect, json, jsonify, escape
from flask_cors import CORS
# from flask_jsonpify import jsonpify
from spcTable import SpcTable
from errors import *


app = Flask(__name__, static_url_path='')
# cors = CORS(app, resources={r"/capability/*"})

app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:edge9527@host.docker.internal:5432/dev_tenant'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:edge9527@aaaaa:5432/dev_tenant'

#------------CONFIGURATION--------------
# print(os.getcwd()) # print the pwd status
#----------------GET-------------------
# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='static/img/Nelson65.png')
# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
#     axis.plot(xs, ys)
#     return fig

@app.route('/front', methods=['GET'])
def index():
  if request.method == "GET":
    try: 
      return render_template('index2.html', title="spc_show", name = 'new_plot', url ='/static/Nelson65.png')#, jsonfile=json.jsonify(resultCapablity) )
    except Exception as e:
      print('type of:',type(e))

@app.route('/api-docs/')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

@app.route("/v1/capability", methods=['GET'])
def capability():
  # query params
  b = request.args.get('startTime') # sync to cloud
  e = request.args.get('endTime') 
  wuuid = request.args.get('workOrderOpHistoryUUID')
  suuid = request.args.get('spcMeasurePointConfigUUID')
  try:  
    if (suuid == None) or (len(suuid) == 0):
      result = 'config point error'
      return result, 400
    elif (b == None) or (len(b) == 0):
      result = 'start time error'
      return result, 400
    elif (e == None) or (len(e) == 0):
      result = 'end time error'
      return result, 400
    else:
      result = SpcTable.CPRfunc(b=b, e=e, wuuid=wuuid, suuid=suuid)# (startTime=b,endTime=e,wooh_uuid=wuuid,smpc_uuid=suuid)
      return result, 200
  except Exception as errors:
    return 'Query Fail', 500

@app.route("/v1/nelson", methods=['GET'])
def nelson():
  b = request.args.get('startTime') # sync to cloud
  e = request.args.get('endTime') 
  wuuid = request.args.get('workOrderOpHistoryUUID')
  suuid = request.args.get('spcMeasurePointConfigUUID')
  try:
    if (suuid == None) or (len(suuid) == 0):
      result = 'config point error'
      return result, 400
    elif (b == None) or (len(b) == 0):
      result = 'start time error'
      return result, 400
    elif (e == None) or (len(e) == 0):
      result = 'end time error'
      return result, 400
    else:
      result = SpcTable.NelsonDraw(b=b, e=e, wuuid=wuuid, suuid=suuid)
      return result, 200
  except Exception as errors:
    return 'Query Fail', 500

#-----------------ENTRANCE-----------------------
@app.route('/', methods=['GET'])
def home():
  return 'ok', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv('PORT')) #os.getenv('PORT')

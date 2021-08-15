# from ..components.alchemy_db import spc_measure_point_config,spc_measure_point_history,work_order_op_history
# from re import A
# import os,json
# from sqlalchemy import create_engine,exc #select, column, join,
# from sqlalchemy.orm import sessionmaker, aliased
# from sqlalchemy.exc import DatabaseError
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm.query import QueryContext
# from ..utils.calculator import Calculator
# from ..utils.nelsonRules import *

# db = SQLAlchemy() 
# # db.init_app(app)
# # engine = create_engine('postgresql://postgres:edge9527@localhost:5432/dev_tenant',echo = False)
# engine = create_engine(os.getenv('PG_URL'),echo = False)
# # print('PG_URLPG_URLPG_URLPG_URL',os.getenv('PG_URL'),sep='\n')
# connection = engine.connect()

# Session = sessionmaker(bind=engine)
# # create a configured "Session" class
# session = Session() # create a Session

# """
# # app.config['SQLALCHEMY_DATABASE_URI'] = [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:edge9527@host.docker.internal:5432/dev_tenant'
# # table_smph.work_order_op_history_uuid = wooh_uuid
# Definition of the table format
# 1. spc_measure_point_config
# 2. spc_measure_point_history

# user params input: 
# * spc_measure point config UUID, work order op history uuid
# * startTime 開工 
# * endTime 完工
# python output:
# cpl,cp,cpk,ppk,..
# """

# #-----------------------------------------------
# class SpcTable:
#     # def __init__(self,rule):
#     #     self.rule = rule
        
#     # def __repr__(self) -> str:
#     #     print(f'Query and wrap up dataflow')
#     #     return super().__repr__()
    
#     def queryfunc(startTime,endTime,wooh_uuid,smpc_uuid): 
#         table_smpc = aliased(spc_measure_point_config) # operation_uuid <=> table_opwh
#         table_smph = aliased(spc_measure_point_history) # work_order_op_history_uuid <=> table_opwh.uuid
#         table_opwh = aliased(work_order_op_history) # operation_uuid <=> table_smpc
#         try:
#             j1 = session.query(table_smph.value,table_opwh.good,table_opwh.defect,table_smpc.lsl,table_smpc.usl,table_smpc.measure_amount,table_smpc.std_value)\
#             .join(table_smpc, table_smph.spc_measure_point_config_uuid == table_smpc.uuid)\
#             .join(table_opwh, table_opwh.uuid == table_smph.work_order_op_history_uuid)\
#             .where((table_opwh.start_time > startTime) & (table_opwh.end_time < endTime) & (table_smph.spc_measure_point_config_uuid == smpc_uuid))\
#             .order_by(table_smph.work_order_op_history_uuid)\
#             .order_by(table_smph.measure_object_id.asc())
#             if (wooh_uuid == None):
#                 queryResult = [row for row in session.execute(j1)]
#             elif (len(wooh_uuid) == 0):
#                 queryResult = [row for row in session.execute(j1)]
#             else:
#                 yy = j1.filter(table_smph.work_order_op_history_uuid == wooh_uuid)
#                 queryResult = [row for row in session.execute(yy)]
#             return queryResult

#         except DatabaseError:
#             print('dbERROR_session',db.session.rollback())
#             db.session.rollback()
#             # handle_sqlalchemy_database_error()
#         except exc.SQLAlchemyError as e:
#             print("error type: ",type(e),str(e))
#             db.session.rollback()
#             raise None
#         except Exception as errors:
#             print('Finalerror',errors)
#             db.session.rollback()
#             return ' Failure :',errors
#         # else:
#         #     db.session.rollback()
#     """
#     Calculate metrics after querying the datasets 
#     """
#     def CPRfunc(beginTime,finalTime,wuuid,suuid):
#         queryResult = SpcTable.queryfunc(startTime=beginTime, endTime=finalTime, wooh_uuid=wuuid, smpc_uuid=suuid)
#         CapabilityCol = ["valuelst","goodlst","defectlst","lsllst","usllst","amount","stdValue"]
#         Query_context = pd.DataFrame()
#         for i in range(len(CapabilityCol)):
#             Query_context[CapabilityCol[i]] = [item[i] for item in queryResult]
#         # t = threading.Thread(target = apply_rules, args=(qResult['valuelst'],'all',2) ,daemon=True);t.start()
#         # # SpcTable.drawchart2(original=datatables.valuelst) #draw and save the raw
#         try:
#             CapabilityResult = Calculator.calc(datatables = Query_context)
#         except Exception as errors:
#             raise f'Calcu Failure: %s{0}'.format(errors)
#         return CapabilityResult

#     def Nelsonfunc(beginTime,finalTime,wuuid,suuid):
#         try:
#             queryResult = SpcTable.queryfunc(startTime=beginTime, endTime=finalTime, wooh_uuid=wuuid, smpc_uuid=suuid)
#         except Exception as errors:
#             raise f'NelsonQuery Failure:{0}'.format(errors)
#         CapabilityCol = ["valuelst","goodlst","defectlst","lsllst","usllst","amount","stdValue"]
#         Query_context = pd.DataFrame()
#         for i in range(len(CapabilityCol)):
#             Query_context[CapabilityCol[i]] = [item[i] for item in queryResult]
        
#         nelsonBool = apply_rules(original=Query_context.valuelst) # markup points after rules verified 
#         df_list = nelsonBool.values.tolist()
#         NelsonCol = ["data","rule1","rule2","rule3","rule4","rule5","rule6","rule7","rule8"]
#         """
#         Another parsing method requires to be mentioned.
#          NelsonContext = pd.DataFrame()
#          for j in range(len(NelsonCol)):
#              NelsonContext[NelsonCol[j]] = [item[j] for item in df_list]
#         """
#         data = [item[0] for item in df_list]
#         rule1 = [item[1] for item in df_list]
#         rule2 = [item[2] for item in df_list]
#         rule3 = [item[3] for item in df_list]
#         rule4 = [item[4] for item in df_list]
#         rule5 = [item[5] for item in df_list]
#         rule6 = [item[6] for item in df_list]
#         rule7 = [item[7] for item in df_list]
#         rule8 = [item[8] for item in df_list]
#         columnValue = [data,rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]
#         NelsonContext = dict(zip(NelsonCol,columnValue))
#         # NelsonContext = json.loads(NelsonContext.to_json(orient="split"))
#         return NelsonContext

  

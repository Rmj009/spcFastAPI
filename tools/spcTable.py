from components.alchemy_db import spc_measure_point_config,spc_measure_point_history,work_order_op_history
from re import A
import os,json
from sqlalchemy import create_engine,exc #select, column, join,
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.exc import DatabaseError
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm.query import QueryContext
from utils.calculator import Calculator
from utils.nelsonRules import *
from model.setting import *


db = SQLAlchemy() # db.init_app(app)
# engine = create_engine('postgresql://postgres:edge9527@localhost:5432/dev_tenant')
# print(os.getenv('PG_URL'))
engine = create_engine(os.getenv('PG_URL'))

Session = sessionmaker(bind=engine)
# create a configured "Session" class
session = Session() # create a Session
connection = engine.connect()

"""
# app.config['SQLALCHEMY_DATABASE_URI'] = [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:edge9527@host.docker.internal:5432/dev_tenant'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:edge9527@aaaaa:5432/dev_tenant'

Definition of the table format
1. spc_measure_point_config
2. spc_measure_point_history

user params input: 
* spc_measure point config UUID, work order op history uuid
* startTime 開工 
* endTime 完工
python output:
cpl,cp,cpk,ppk,..
"""
#-----------------------------------------------
class SpcTable:
    def __init__(self,rule):
        self.rule = rule
        
    def __repr__(self) -> str:
        print(f'Query and wrap up dataflow')
        return super().__repr__()
    def drawchart1(datapoints):
        #---------invoke western------------
        # datapoints = valuelst
        trendObj = {'all_vals': datapoints,'format_1': np.zeros(len(datapoints)),'format_2': np.zeros(len(datapoints)),'format_3': np.zeros(len(datapoints)),'format_4': np.zeros(len(datapoints))}
        print("pppppppppp",trendObj['all_vals'])
        # assign_datum(obj = trendObj, datum = 10)
        def format_arr(rule):
            rule_arr = 'format_' + str(rule)
            return [index for index,val in enumerate(trendObj[rule_arr]) if val]
        def plotAxlines(array):
            theMean = np.mean(array)
            sd = np.std(array)
            colors = ['black','green','violet','red']
            for level,color in enumerate(colors):
                upper = theMean + sd*level
                lower = theMean - sd*level
                plt.axhline(y=upper, linewidth=0.5, color=color)
                plt.axhline(y=lower, linewidth=0.5, color=color)
            return
        mark = 3.5
        plt.figure(figsize=(60,30))
        plt.plot(trendObj['all_vals'], color='red',markevery=format_arr(1), ls="", marker='s',mfc = 'none', mec='red', label="Rule1", markersize=mark*1.5)
        plt.plot(trendObj['all_vals'], color='blue',markevery=format_arr(2), ls="", marker='o', mfc='none',mec='blue',label="Rule2", markersize=mark*1)
        plt.plot(trendObj['all_vals'], color='brown',markevery=format_arr(3), ls="", marker='o', mfc='none',mec='brown',label="Rule3", markersize=mark*1.5)
        plt.plot(trendObj['all_vals'], color='blue',markevery=format_arr(4), ls="", marker='s', mfc='none',mec='green',label="Rule4", markersize=mark*1.0)
        plt.plot(trendObj['all_vals'], color='#81B5CB', ls="", marker=".", markersize=mark)
        plotAxlines(trendObj['all_vals'])
        plt.legend()
        plt.ylim(0,25)
        # # plt.plot(datapoints)
        # plt.savefig('static/img/control-chart.png')
        # # g = sns.relplot(x = 'all_vals', y = 'format_1', data = trendObj, kind="line")
        # # g.fig.autofmt_xdate()
        plt.show()


    # def drawchart2(original):
    #     """Plot RawData"""
    #     text_offset = 70
    #     mean = np.mean(original)
    #     sigma = np.std(original)
    #     # print("###",[mean,sigma])
    #     fig = plt.figure(figsize=(20, 10))
    #     ax1 = fig.add_subplot(1, 1, 1)
    #     ax1.plot(original, color='blue', linewidth=1.5)

    #     # plot mean
    #     ax1.axhline(mean, color='r', linestyle='--', alpha=0.5)
    #     ax1.annotate('$\overline{x}$', xy=(len(original), mean), textcoords=('offset points'),
    #                 xytext=(text_offset, 0), fontsize=18)

    #     # plot 1-3 standard deviations
    #     sigma_range = np.arange(1,4)
    #     for i in range(len(sigma_range)):
    #         ax1.axhline(mean + (sigma_range[i] * sigma), color='black', linestyle='-', alpha=(i+1)/10)
    #         ax1.axhline(mean - (sigma_range[i] * sigma), color='black', linestyle='-', alpha=(i+1)/10)
    #         ax1.annotate('%s $\sigma$' % sigma_range[i], xy=(len(original), mean + (sigma_range[i] * sigma)),
    #                     textcoords=('offset points'),
    #                     xytext=(text_offset, 0), fontsize=18)
    #         ax1.annotate('-%s $\sigma$' % sigma_range[i],
    #                     xy=(len(original), mean - (sigma_range[i] * sigma)),
    #                     textcoords=('offset points'),
    #                     xytext=(text_offset, 0), fontsize=18)
    #     # plt.show()
    #     plt.savefig('static/img/classicialcc.png')
    #     return

    def queryfunc(startTime,endTime,wooh_uuid,smpc_uuid): 
        table_smpc = aliased(spc_measure_point_config) # operation_uuid <=> table_opwh
        table_smph = aliased(spc_measure_point_history) # work_order_op_history_uuid <=> table_opwh.uuid
        table_opwh = aliased(work_order_op_history) # operation_uuid <=> table_smpc
        try:
            # table_smph.work_order_op_history_uuid = wooh_uuid
            j1 = session.query(table_smph.value,table_opwh.good,table_opwh.defect,table_smpc.lsl,table_smpc.usl,table_smpc.measure_amount,table_smpc.std_value)\
            .join(table_smpc, table_smph.spc_measure_point_config_uuid == table_smpc.uuid)\
            .join(table_opwh, table_opwh.uuid == table_smph.work_order_op_history_uuid)\
            .where((table_opwh.start_time > startTime) & (table_opwh.end_time < endTime) & (table_smph.spc_measure_point_config_uuid == smpc_uuid))\
            .order_by(table_smph.work_order_op_history_uuid)\
            .order_by(table_smph.measure_object_id.asc())
            if (wooh_uuid == None):
                queryResult = [row for row in session.execute(j1)]
            elif (len(wooh_uuid) == 0):
                queryResult = [row for row in session.execute(j1)]
            else:
                yy = j1.filter(table_smph.work_order_op_history_uuid == wooh_uuid)
                queryResult = [row for row in session.execute(yy)]
            return queryResult

        except DatabaseError:
            db.session.rollback()
            print('dbERROR_session',db.session.rollback())
            # handle_sqlalchemy_database_error()
        except exc.SQLAlchemyError as e:
            print("error type: ",type(e),str(e))
            db.session.rollback()
            raise None
        except Exception as errors:
            print('Finalerror',errors)
            db.session.rollback()
            return ' Failure :',errors
        else:
            db.session.rollback()
    """
    Calculate metrics after querying the datasets 
    """
    def CPRfunc(beginTime,finalTime,wuuid,suuid):
        queryResult = SpcTable.queryfunc(startTime=beginTime, endTime=finalTime, wooh_uuid=wuuid, smpc_uuid=suuid)
        CapabilityCol = ["valuelst","goodlst","defectlst","lsllst","usllst","amount","stdValue"]
        Query_context = pd.DataFrame()
        for i in range(len(CapabilityCol)):
            Query_context[CapabilityCol[i]] = [item[i] for item in queryResult]
        # t = threading.Thread(target = apply_rules, args=(qResult['valuelst'],'all',2) ,daemon=True);t.start()
        # # SpcTable.drawchart2(original=datatables.valuelst) #draw and save the raw
        try:
            CapabilityResult = Calculator.calc(datatables = Query_context)
        except Exception as errors:
            raise f'Calcu Failure: %s{0}'.format(errors)
        return CapabilityResult

    def Nelsonfunc(beginTime,finalTime,wuuid,suuid):
        try:
            queryResult = SpcTable.queryfunc(startTime=beginTime, endTime=finalTime, wooh_uuid=wuuid, smpc_uuid=suuid)
        except Exception as errors:
            raise f'NelsonQuery Failure:{0}'.format(errors)
        CapabilityCol = ["valuelst","goodlst","defectlst","lsllst","usllst","amount","stdValue"]
        Query_context = pd.DataFrame()
        for i in range(len(CapabilityCol)):
            Query_context[CapabilityCol[i]] = [item[i] for item in queryResult]
        
        nelsonBool = apply_rules(original=Query_context.valuelst) # markup points after rules verified 
        df_list = nelsonBool.values.tolist()
        NelsonCol = ["data","rule1","rule2","rule3","rule4","rule5","rule6","rule7","rule8"]
        """
        Another parsing method requires to be mentioned.
         NelsonContext = pd.DataFrame()
         for j in range(len(NelsonCol)):
             NelsonContext[NelsonCol[j]] = [item[j] for item in df_list]
        """
        data = [item[0] for item in df_list]
        rule1 = [item[1] for item in df_list]
        rule2 = [item[2] for item in df_list]
        rule3 = [item[3] for item in df_list]
        rule4 = [item[4] for item in df_list]
        rule5 = [item[5] for item in df_list]
        rule6 = [item[6] for item in df_list]
        rule7 = [item[7] for item in df_list]
        rule8 = [item[8] for item in df_list]
        columnValue = [data,rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8]
        NelsonContext = dict(zip(NelsonCol,columnValue))
        # NelsonContext = json.loads(NelsonContext.to_json(orient="split"))
        return NelsonContext

  

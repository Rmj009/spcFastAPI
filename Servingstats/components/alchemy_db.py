from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
# from sqlalchemy import text
# from sqlalchemy.sql import text
class spc_measure_point_config(db.Model): #Sojourn 1
    __tablename__='spc_measure_point_config'
    uuid = db.Column(
        db.String(32),unique = True,  primary_key = True, nullable = False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)
    route_uuid = db.Column(
        db.String(50), unique=False, nullable=False)
    operation_uuid = db.Column(
        db.String(50), unique=False, nullable=False)
    route_operation_uuid = db.Column(
        db.String(50), unique=False, nullable=False)
    tenant_id = db.Column(
        db.String(50), unique=False, nullable=False)
    name = db.Column(
        db.String(50), unique=False, nullable=False)
    description = db.Column(
        db.String(255), nullable=False)
    unit = db.Column(
        db.String(8), unique=False, nullable=False)
    mode = db.Column(
        db.String(8), unique=False, nullable=False)
    std_value = db.Column(db.Float, nullable=False)
    usl = db.Column(db.Float, nullable=False)
    lsl = db.Column(db.Float, nullable=False)
    measure_amount = db.Column(db.Integer, nullable=False)
    range_spec = db.Column(db.Float, nullable=False)
    sample_number = db.Column(db.Float, nullable=False)
    rules = db.Column(
        db.String(64), nullable=False)

    def __init__(
        self,uuid,create_time,update_time,route_uuid,operation_uuid,
        route_operation_uuid,tenant_id,name,description,unit,mode,std_value,lsl,usl,
        measure_amount,range_spec,sample_number,rules):
        self.uuid = uuid
        self.create_time = create_time
        self.update_time = update_time
        self.route_uuid = route_uuid
        self.operation_uuid = operation_uuid
        self.route_operation_uuid = route_operation_uuid
        self.tenant_id = tenant_id
        self.name = name
        self.description = description
        self.unit = unit
        self.mode = mode
        self.std_value = std_value
        self.lsl = lsl
        self.usl = usl
        self.measure_amount = measure_amount
        self.range_spec = range_spec
        self.sample_number = sample_number
        self.rules = rules
class spc_measure_point_history(db.Model): #Sojourn 2
    __tablename__='spc_measure_point_history'
    uuid = db.Column(
        db.String(32),unique = True,  primary_key = True, nullable = False)
    work_order_op_history_uuid = db.Column(
        db.String(50), unique=False, nullable=False)
    tenant_id = db.Column(
        db.String(50), unique=False, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)
    worker_id = db.Column(
        db.String(50), unique=False, nullable=False)
    spc_measure_point_config_uuid = db.Column(
        db.String(50), unique=False, nullable=False)
    value = db.Column(db.Float, nullable=False) #float?
    measure_object_id = db.Column(db.Integer, nullable=False)
    spc_measure_instrument_uuid = db.Column(
        db.String(50), unique=False, nullable=False)
    
    def __init__(self,uuid,work_order_op_history_uuid,tenant_id,create_time,update_time,worker_id,spc_measure_point_config_uuid,value,measure_object_id,spc_measure_instrument_uuid):
        self.uuid = uuid
        self.work_order_op_history_uuid = work_order_op_history_uuid
        self.tenant_id = tenant_id
        self.create_time = create_time
        self.update_time = update_time
        self.worker_id = worker_id
        self.spc_measure_point_config_uuid = spc_measure_point_config_uuid
        self.value = value
        self.measure_object_id = measure_object_id
        self.spc_measure_instrument_uuid = spc_measure_instrument_uuid
        # self.state
class work_order_op_history(db.Model): #Sojourn 3
    __tablename__='work_order_op_history'
    uuid = db.Column(
        db.String(32),unique = True,  primary_key = True, nullable = False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)
    work_order_id = db.Column(
        db.String(32), unique=False, nullable=False)
    shift = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)
    producer_number = db.Column(
        db.String(50), unique=False, nullable=False)
    producer_name = db.Column(
        db.String(50), unique=False, nullable=False)
    qty = db.Column(db.Float, nullable=False)
    description = db.Column(
        db.String(255), nullable=False)
    device_name = db.Column(
        db.String(50), unique=False, nullable=False)
    good = db.Column(db.Float, nullable=False)
    defect = db.Column(db.Float, nullable=False)
    std_tp = db.Column(db.Float, nullable=False)
    std_ts = db.Column(db.Float, nullable=False)
    std_work_time = db.Column(db.Float, nullable=False)
    act_work_time = db.Column(db.Float, nullable=False)
    worker_id = db.Column(db.Integer, nullable=False)
    worker_name = db.Column(db.String(32), nullable=False)
    progress = db.Column(db.Integer, nullable=False)
    defect_reason = db.Column(
        db.String(255), nullable=False)
    op_code = db.Column(db.Integer, nullable=False)
    worker_uuid = db.Column(
        db.String(32), unique=False, nullable=False)
    work_order_uuid = db.Column(
        db.String(32), unique=False, nullable=False)
    operation_uuid = db.Column(
        db.String(32), unique=False, nullable=False)
    tenant_id = db.Column(
        db.String(32), unique=False, nullable=False)
    device_uuid = db.Column(
        db.String(32), unique=False, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    op_name = db.Column(db.Integer, nullable=False)
    
    
    def __init__(self,uuid,create_time,update_time,work_order_id,start_time,end_time,producer_number,producer_name,qty,description,device_name,good,defect,std_tp,std_ts,std_work_time,operation_uuid):
        self.uuid = uuid
        self.create_time = create_time
        self.update_time = update_time
        self.work_order_id = work_order_id
        # self.shift = shift
        self.start_time = start_time
        self.end_time = end_time
        self.producer_number = producer_number
        self.producer_name = producer_name
        self.qty = qty
        self.description = description
        self.device_name = device_name
        self.good = good
        self.defect = defect
        self.std_tp = std_tp
        self.std_ts = std_ts
        self.std_work_time = std_work_time
        # self.act_work_time = act_work_time
        # self.worker_id = worker_id
        # self.worker_name = worker_name
        # self.progress = progress
        # self.defect_reason = defect_reason
        # self.op_code = op_code
        # self.worker_uuid = worker_uuid
        # self.work_order_uuid = work_order_uuid
        self.operation_uuid = operation_uuid
        # self.tenant_id = tenant_id
        # self.device_uuid = device_uuid
        # self.status = status
        # self.op_name = op_name


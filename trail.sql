



SELECT 
    spc-history.uuid AS spc-history_uuid,
    spc-history.work_order_op_history_uuid AS spc-history_work_order_op_history_uuid, 
    spc-history.tenant_id AS spc-history_tenant_id, 
    spc-history.create_time AS spc-history_create_time, 
    spc-history.update_time AS spc-history_update_time, 
    spc-history.worker_id AS spc-history_worker_id, 
    spc-history.spc_measure_point_config_uuid AS spc-history_spc_measure_point_config_uuid, 
    spc-history.value AS spc-history_value, 
    spc-history.measure_object_id AS spc-history_measure_object_id, 
    spc-history.spc_measure_instrument_uuid AS spc-history_spc_measure_instrument_uuid 
FROM spc_measure_point_history AS spc-history 
JOIN spc_measure_point_config AS spc_measure_point_config_1 ON spc-history.spc_measure_point_config_uuid = spc_measure_point_config_1.uuid 
JOIN work_order_op_history AS work_order_op_history_1 ON work_order_op_history_1.uuid = spc-history.work_order_op_history_uuid


--------------
SELECT spc-history.uuid, 
spc-history.work_order_op_history_uuid, 
spc-history.tenant_id, spc-history.create_time, 
spc-history.update_time, spc-history.worker_id, 
spc-history.spc_measure_point_config_uuid, spc-history.value, 
spc-history.measure_object_id, 
spc-history.spc_measure_instrument_uuid 
FROM spc_measure_point_history AS spc-history, 
(SELECT spc-history.uuid AS spc-history_uuid, 
spc-history.work_order_op_history_uuid AS spc-history_work_order_op_history_uuid, 
spc-history.tenant_id AS spc-history_tenant_id, 
spc-history.create_time AS spc-history_create_time, 
spc-history.update_time AS spc-history_update_time, 
spc-history.worker_id AS spc-history_worker_id, 
spc-history.spc_measure_point_config_uuid AS spc-history_spc_measure_point_config_uuid, 
spc-history.value AS spc-history_value, 
spc-history.measure_object_id AS spc-history_measure_object_id, 
spc-history.spc_measure_instrument_uuid AS spc-history_spc_measure_instrument_uuid)

FROM spc_measure_point_history AS spc-history 
JOIN spc_measure_point_config AS spc_measure_point_config_1 ON spc-history.spc_measure_point_config_uuid = spc_measure_point_config_1.uuid 
JOIN work_order_op_history AS work_order_op_history_1 ON work_order_op_history_1.uuid = spc-history.work_order_op_history_uuid) AS anon_1

-----------------------

SELECT spc_measure_point_history_1.value AS spc_measure_point_history_1_value, 
work_order_op_history_1.good AS work_order_op_history_1_good, 
work_order_op_history_1.defect AS work_order_op_history_1_defect, 
spc_measure_point_config_1.usl AS spc_measure_point_config_1_usl, 
spc_measure_point_config_1.lsl AS spc_measure_point_config_1_lsl

FROM spc_measure_point_history AS spc_measure_point_history_1 
JOIN spc_measure_point_config AS spc_measure_point_config_1 ON spc_measure_point_history_1.spc_measure_point_config_uuid = spc_measure_point_config_1.uuid 
JOIN work_order_op_history AS work_order_op_history_1 ON work_order_op_history_1.uuid = spc_measure_point_history_1.work_order_op_history_uuid 
WHERE work_order_op_history_1.start_time > %(start_time_1)s AND work_order_op_history_1.end_time < %(end_time_1)s


--------------------------

SELECT spc_measure_point_history_1.value AS spc_measure_point_history_1_value, work_order_op_history_1.good AS work_order_op_history_1_good, work_order_op_history_1.defect AS work_order_op_history_1_defect, spc_measure_point_config_1.lsl AS spc_measure_point_config_1_lsl, spc_measure_point_config_1.usl AS spc_measure_point_config_1_usl 
FROM spc_measure_point_history AS spc_measure_point_history_1 JOIN spc_measure_point_config AS spc_measure_point_config_1 ON spc_measure_point_history_1.spc_measure_point_config_uuid = spc_measure_point_config_1.uuid JOIN work_order_op_history AS work_order_op_history_1 ON work_order_op_history_1.uuid = spc_measure_point_history_1.work_order_op_history_uuid 

WHERE work_order_op_history_1.start_time > %(start_time_1)s 
AND work_order_op_history_1.end_time < %(end_time_1)s 
AND (spc_measure_point_history_1.work_order_op_history_uuid IS NOT NULL OR spc_measure_point_history_1.spc_measure_point_config_uuid IS NOT NULL)



---------------4/22-----------------
SELECT spc_measure_point_history_1.value AS spc_measure_point_history_1_value, 
spc_measure_point_config_1.lsl AS spc_measure_point_config_1_lsl, 
spc_measure_point_config_1.usl AS spc_measure_point_config_1_usl, 
work_order_op_history_1.good AS work_order_op_history_1_good, 
work_order_op_history_1.defect AS work_order_op_history_1_defect 

FROM spc_measure_point_history AS spc_measure_point_history_1 
JOIN spc_measure_point_config AS spc_measure_point_config_1 ON spc_measure_point_history_1.spc_measure_point_config_uuid = spc_measure_point_config_1.uuid 
JOIN work_order_op_history AS work_order_op_history_1 ON work_order_op_history_1.uuid = %(uuid_1)s 

WHERE work_order_op_history_1.start_time > %(start_time_1)s AND 
work_order_op_history_1.end_time < %(end_time_1)s AND 
spc_measure_point_history_1.spc_measure_point_config_uuid = %(spc_measure_point_config_uuid_1)s


----------4/25-----------
-- 子查詢上使用
stmt = select(table_history).select_from(j1) #subquery
print("stmt:", stmt)
print(stmt)

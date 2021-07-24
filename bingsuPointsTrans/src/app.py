import json
import os
from uuid import uuid4
from .bingsuPointsTrans import PynamoBingsuPointsTrans
from datetime import datetime

def add_points_trans(event, context):
    item = event['arguments']
    points_trans_item = PynamoBingsuPointsTrans(
        transaction_id = str(uuid4()),
        user_id = item['user_id'],
        date_time = str(datetime.utcnow()).replace(' ','T')[0:19]+'+00:00',
        points_amount = item['points_amount'],
        company = item['company'],
        co2_amount = item['co2_amount']
    )
    points_trans_item.save()
    return {'status': 200}
def get_points_trans_by_id(event, context):
    item = event['arguments']
    transaction_id = item['transaction_id']
    iterator = PynamoBingsuPointsTrans.query(transaction_id)
    transaction_list = list(iterator)
    lst = []
    if len(transaction_list) > 0:
        for transaction in transaction_list:
            lst.append(transaction.returnJson())
    else:
        return {'status': 400}
    return {'status': 200,
            'data': lst}
    
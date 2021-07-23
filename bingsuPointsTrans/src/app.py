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

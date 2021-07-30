import json
import os
from uuid import uuid4
from .bingsuPointsTrans import PynamoBingsuPointsTrans, PynamoBingsuCarbonTotalSum
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

# input: user_id, points_amount, company, co2, restaurant, distance, item
def add_points_trans(event, context):
    item = event['arguments']
    points_trans_item = PynamoBingsuPointsTrans(
        transaction_id = str(uuid4()),
        user_id = item['user_id'],
        date_time = str(datetime.utcnow()).replace(' ','T')[0:19]+'+00:00',
        points_amount = item['points_amount'],
        company_name = item['company_name'],
        co2_amount = item['co2_amount'],
        restaurant_name = item['restaurant_name'],
        distance = item['distance'],
        item = item['item'],
        packaging_co2 = item.get('packaging_co2', None),
        packaging_amount = item.get('packaging_amount', None),
        packaging_flag = False
    )
    points_trans_item.save()
    return {'status': 200}

# input: transaction_id
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

# input: user_id
def get_all_points_trans_by_user_id(event, context):
    item = event['arguments']
    iterator = PynamoBingsuPointsTrans.user_id_index.query(item['user_id'])
    points_trans_list = list(iterator)
    lst = []
    if len(points_trans_list) > 0:
        for points_trans in points_trans_list:
            lst.append(points_trans.returnJson())
    else:
        return {'status': 400}
    return {'status': 200,
            'data': lst[0:20]}

# input: return total sum of company
def get_total_carbon_sum(event, context):
    company = {'foodpanda':0, 'grab':0, 'robinhood':0}
    for item in company:
        iterator = PynamoBingsuCarbonTotalSum.query(item)
        total_sum_list = list(iterator)
        lst = []
        if len(total_sum_list) > 0:
            for i in total_sum_list:
                lst.append(i.returnJson())
        else:
            return {'status': 400}
        company[item] = lst[0]['total_amount_co2']
    return {'status': 200, 'data': company}

# input: company, value
def add_total_carbon_sum(event, context):
    company = event['arguments']['company']
    value = event['arguments']['value']
    # get from db
    iterator = PynamoBingsuCarbonTotalSum.query(company)
    total_sum_list = list(iterator)
    lst = []
    if len(total_sum_list) > 0:
        for i in total_sum_list:
            lst.append(i.returnJson())
    else:
        return {'status': 400}
    old_value = lst[0]['total_amount_co2']
    new_value = old_value + value
    total_carbon_sum_item = PynamoBingsuCarbonTotalSum(
        company = company,
        total_amount_co2 = new_value
    )
    total_carbon_sum_item.save()
    return {'status': 200}

def update_points_trans_for_packaging(event, context):
    item = event['arguments']
    transaction_id = item['transaction_id']
    user_id = item['user_id']
    packaging_amount = item['packaging_amount']
    packaging_co2 = packaging_amount*35
    iterator = PynamoBingsuPointsTrans.query(transaction_id)
    transaction_list = list(iterator)
    lst = []
    if len(transaction_list) > 0:
        for transaction in transaction_list:
            lst.append(transaction.returnJson())
    else:
        return {'status': 400}
    current_dict = lst[0]
    transaction_item = PynamoBingsuPointsTrans(
        transaction_id = transaction_id,
        user_id = user_id,
        date_time = current_dict['date_time'],
        points_amount = current_dict['points_amount'],
        company_name = current_dict['company_name'],
        co2_amount = current_dict['co2_amount'],
        restaurant_name = current_dict['restaurant_name'],
        distance = current_dict['distance'],
        item = current_dict['item'],
        packaging_co2 = packaging_co2,
        packaging_amount = packaging_amount,
        packaging_flag = True
    )
    transaction_item.save()

    dynamodb = boto3.resource('dynamodb')
    client_lambda = boto3.client('lambda')

    user_table = dynamodb.Table('BingsuUser')
    response_user = user_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id))
    old_coins = int(response_user['Items'][0]['coins'])
    new_coins = old_coins + 2
    arguments = {
            "user_id": user_id,
            "coins": new_coins,
        }
    update_user_response = client_lambda.invoke(
        FunctionName = 'arn:aws:lambda:ap-southeast-1:405742985670:function:bingsuUser-UpdateUserFunction-9I54tc4Xyb2h',
        InvocationType = 'RequestResponse',
        Payload = json.dumps({'arguments': arguments})
    )

    return {'status': 200}
    
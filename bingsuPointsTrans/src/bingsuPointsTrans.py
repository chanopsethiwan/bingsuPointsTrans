from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
import os

class PynamoBingsuPointsTrans(Model):
    ''' database to store user '''
    class Meta:
        table_name = os.environ.get('BINGSU_POINTS_TRANS_TABLE_NAME')
        region = 'ap-southeast-1'
    transaction_id = UnicodeAttribute(hash_key = True)
    user_id = UnicodeAttribute()
    date_time = UnicodeAttribute()
    points_amount = NumberAttribute()
    company = UnicodeAttribute()
    co2_amount = NumberAttribute()
    
    def returnJson(self):
        return vars(self).get('attribute_values')
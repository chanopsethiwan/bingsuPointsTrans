from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
import os

class UserIdIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        index_name = 'user_id'
        read_capacity_units = 1
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    user_id = UnicodeAttribute(hash_key=True)

class PynamoBingsuPointsTrans(Model):
    ''' database to store user '''
    class Meta:
        table_name = os.environ.get('BINGSU_POINTS_TRANS_TABLE_NAME')
        region = 'ap-southeast-1'
    transaction_id = UnicodeAttribute(hash_key = True)
    user_id = UnicodeAttribute()
    date_time = UnicodeAttribute()
    points_amount = NumberAttribute()
    company_name = UnicodeAttribute()
    co2_amount = NumberAttribute()
    restaurant_name = UnicodeAttribute()
    distance = NumberAttribute()
    item = NumberAttribute()
    packaging_co2 = NumberAttribute(null=True)
    packaging_amount = NumberAttribute(null=True)
    
    user_id_index = UserIdIndex()
    
    def returnJson(self):
        return vars(self).get('attribute_values')

class PynamoBingsuCarbonTotalSum(Model):
    ''' database to store user '''
    class Meta:
        table_name = os.environ.get('BINGSU_TOTAL_CARBON_SUM_TABLE_NAME')
        region = 'ap-southeast-1'
    company = UnicodeAttribute(hash_key = True)
    total_amount_co2 = NumberAttribute()
    
    def returnJson(self):
        return vars(self).get('attribute_values')
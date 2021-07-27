from mongoengine import *
import datetime
class fans(Document):
    user_id = StringField(primary_key=True)
    update_time = DateTimeField()
    attention_user_distributed_tags= ListField() #用户分布
    attention_user_feature_tags= ListField() #用户特征
    age_distributions = ListField() #年龄分布
    sax_distributions = ListField() #性别分布
    top_region_distributions = ListField() #地区分布
    device_distributions = ListField() #设备分布

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(fans, self).save(*args, **kwargs)

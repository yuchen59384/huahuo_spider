from mongoengine import *
import datetime

date = str(datetime.date.today()).replace('-', '')
connect(host="mongodb://localhost:27017/%s" % date, connect=False)

class Distribution(EmbeddedDocument):
    name = StringField()
    value = FloatField()

class FansPortrait(EmbeddedDocument):
    update_time = DateTimeField()
    attention_user_distributed_tags= ListField(StringField()) #用户分布
    attention_user_feature_tags= ListField(StringField()) #用户特征
    age_distributions = ListField(EmbeddedDocumentField(Distribution)) #年龄分布
    sax_distributions = ListField(EmbeddedDocumentField(Distribution)) #性别分布
    top_region_distributions = ListField(EmbeddedDocumentField(Distribution)) #地区分布
    device_distributions = ListField(EmbeddedDocumentField(Distribution)) #设备分布

class kol(Document):
    user_id = StringField(primary_key=True)
    mcn_id = StringField()
    update_time = DateTimeField()
    fans_like_num = IntField()  # 粉丝获赞
    fans_num = IntField()  # 粉丝数
    gender_desc = StringField()  # 性别
    head_img = StringField()  # 头像
    nickname = StringField()  # 名称
    partition_name = StringField()  # 分区
    second_partition_name = StringField()
    signature = StringField()  # 签名
    tags = ListField()
    mcn_company_name=StringField()

    # upper_prices = ListField()  # 服务报价
    # 定制
    custom_platform_price = FloatField()
    custom_discount_price = FloatField()
    # 植入
    implant_platform_price = FloatField()
    implant_discount_price = FloatField()
    # 直发动态
    direct_message_platform_price = FloatField()
    direct_message_discount_price = FloatField()
    # 转发动态
    forward_message_platform_price = FloatField()
    forward_message_discount_price = FloatField()

    average_barrage_cnt = IntField()  # 平均弹幕数
    average_collect_cnt = IntField()  # 平均收藏数
    average_comment_cnt = IntField()  # 平均评论数
    average_interactive_rate = FloatField()  # 作品互动率
    average_like_cnt = IntField()  # 平均点赞数
    average_play_cnt = IntField()  # 平均播放数
    # trend
    user_total_trend = ListField()  # 用户总量趋势
    user_Increment_trend = ListField()  # 用户增量趋势
    note_play_trend = ListField()  # 稿件播放量趋势
    note_interact_trend = ListField()  # 稿件互动量趋势
    fansPortrait=EmbeddedDocumentField(FansPortrait) #粉丝画像

    # list
    # 个人作品
    personal_note = ListField()
    # 商业作品
    commercial_note = ListField()

    meta = {
        'indexes': [
            {'fields': ['gender_desc']},
            {'fields': ['partition_name']},
            {'fields': ['tags']}
        ]
    }
    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(kol, self).save(*args, **kwargs)

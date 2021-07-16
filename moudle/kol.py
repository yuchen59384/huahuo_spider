from mongoengine import *
class kol(document):
    user_id = StringField(unique=True)
    fans_like_num = IntField() #粉丝获赞
    fans_num = IntField() #粉丝数
    gender_desc = StringField() #性别
    head_img = StringField() #头像
    nickname = StringField() #名称
    partition_name = StringField() #分区
    second_partition_name = StringField()
    signature = StringField() #签名
    tags = ListField()
    upper_prices = ListField() #服务报价

    average_barrage_cnt = IntField()  # 平均弹幕数
    average_collect_cnt = IntField()  # 平均收藏数
    average_comment_cnt = IntField()  # 平均评论数
    average_interactive_rate = IntField()  # 作品互动率
    average_like_cnt = IntField()  # 平均点赞数
    average_play_cnt = IntField()  # 平均播放数
    # trend
    user_total_trend = ListField()  # 用户总量趋势
    user_Increment_trend = ListField()  # 用户增量趋势
    note_play_trend = ListField()  # 稿件播放量趋势
    note_interact_trend = ListField()  # 稿件互动量趋势

    # list
    # 个人作品
    personal_note = ListField()
    # 商业作品
    commercial_note = ListField()

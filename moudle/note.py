from mongoengine import *
import datetime
connect(host="mongodb://localhost:27017/c_note", connect=False)
# class Comment(Document):#评论存储
#     note_id = StringField(unique=True)
#     bvid = StringField()
#     top = ListField(StringField())
#     replies = ListField(StringField())
#
#     meta = {
#         'indexes': [
#             {'fields': ['note_id'], 'unique': True},
#             {'fields': ['bvid']}
#         ]
#     }

class note(Document):
    note_id = StringField(primary_key=True)
    bvid = StringField()
    user_id = StringField()
    cid = StringField()
    create_time = DateTimeField()
    update_time = DateTimeField()
    title = StringField()
    head_photo = StringField()
    desc = StringField()
    type = StringField()  #
    category = StringField()  # 主题
    # tags = ListField(StringField())
    # topics = ListField(StringField())#
    his_rank = IntField()  # 全站历史最高排名
    publish_time = DateTimeField()
    # mentioned_brands = ListField(StringField())
    # dm_hot_words = SortedListField(EmbeddedDocumentField(DmWords), ordering='count')
    # title_tags = ListField(StringField())#

    # 互动数据
    # video_comment = IntField(default=0)  # 弹幕
    # comment = IntField(default=0)  # 评论数
    # view = IntField(default=0)  # 播放量
    # share = IntField(default=0)  # 转发次数
    # collect = IntField(default=0)  # 收藏人数
    # like = IntField(default=0)  # 点赞人数
    # # dislike = IntField(default=0)  # 讨厌人数 失效
    # coin = IntField(default=0)  # 硬币数
    # fans_view = FloatField(default=0.0)    # 粉播率

    # 商业数据
    # is_business = BooleanField(default=False)
    upper_comment=StringField()
    # brands = ListField(ReferenceField(Brand))
    cooperation_brand = StringField()
    # cpm = IntField()
    # qiafan = BooleanField(default=False)

    # meta = {
    #     'indexes': [
    #         # {'fields': ['note_id'], 'primary_key': True},
    #         {'fields': ['bvid']},
    #         {'fields': ['user_id']},
    #         {'fields': ['type']},
    #         {'fields': ['category']},
    #         {'fields': ['tags'], 'sparse': True},
    #         # {'fields': ['title_tags'], 'sparse': True},
    #         {'fields': ['view']},
    #         {'fields': ['share']},
    #         # {'fields': ['topics']},
    #         {'fields': ['collect']},
    #         {'fields': ['like']},
    #         {'fields': ['coin']},
    #         {'fields': ['comment']},
    #         {'fields': ['video_comment']},
    #         {'fields': ['publish_time']},
    #         {'fields': ['category', 'publish_time']}
    #     ]
    # }

    # def save(self, *args, **kwargs):
    #     now = datetime.datetime.now()
    #     if not self.create_time:
    #         self.create_time = now
    #     self.update_time = now
    #     return super(note, self).save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     self.update_time = datetime.datetime.now()
    #     return super(note, self).save(*args, **kwargs)





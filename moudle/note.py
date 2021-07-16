from mongoengine import *
class note(document):
    #Overview

    # 提及品牌
    mentioned_brands = ListField(StringField())

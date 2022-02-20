from mongoengine_goodjson import Document
from mongoengine.fields import DateTimeField, StringField


class RevokedToken(Document):
    jti = StringField(null=False, default=None)
    created_at = DateTimeField(null=False, default=None)

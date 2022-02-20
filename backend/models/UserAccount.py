from mongoengine_goodjson import Document
from mongoengine.fields import EmailField, StringField


class UserAccount(Document):
    email = EmailField(unique=True, null=False, default=None)
    hash = StringField(unique=False, null=False, default=None)

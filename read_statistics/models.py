from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING) #外键，指向模型
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') #统一一下上面的变成外键

class ReadNumExpandMethod():
    def get_read_num(self):

        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except:
            return 0
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # 外键，指向模型
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  # 统一一下上面的变成外键

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    class Meta:
        ordering = ['-comment_time']

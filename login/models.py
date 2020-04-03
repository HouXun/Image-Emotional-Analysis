from django.db import models

# Create your models here.


class User(models.Model):
    '''用户表'''

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    email = models.EmailField(max_length=64,unique=True)
    sex = models.CharField(max_length=8, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'



class IMG(models.Model):
    img = models.ImageField(max_length=64,upload_to='upload',verbose_name=u'图片链接')
    label=models.CharField(max_length=16,default='',verbose_name=u'情感标签')
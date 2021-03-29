from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class PRODUCT_TYPE(models.Model):
    title = models.CharField(max_length=150, null=False)
    
    def __str__(self):
        return str(self.title)

class PRODUCT(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE, related_name='pro_owner')
    name = models.CharField(max_length=150, null=False)
    pmodel = models.CharField(max_length=50, null=False)
    pbattery = models.IntegerField(default=0)
    q_rating = models.IntegerField(default=0)
    p_rating = models.IntegerField(default=0)
    pimage = models.FileField(upload_to='images')
    ptype = models.ForeignKey(PRODUCT_TYPE,on_delete=models.CASCADE, related_name='pro_type')
    o_review = models.TextField(default='NA')
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    unliked = models.ManyToManyField(User, default=None, blank=True, related_name='unliked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name +"  - "+ self.pmodel)
    
    @property
    def num_likes(self):
        return self.liked.all().count()
    
    @property
    def num_unlikes(self):
        return self.unliked.all().count()

class COMMENTS(models.Model):
    cmt_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment_by")
    pro_cmt = models.ForeignKey(PRODUCT,on_delete=models.CASCADE,related_name="pro_comment")
    cmt_desc = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
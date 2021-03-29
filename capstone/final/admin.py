from django.contrib import admin
from .models import User,PRODUCT,PRODUCT_TYPE,COMMENTS
# Register your models here.

admin.site.register(User)
admin.site.register(PRODUCT)
admin.site.register(PRODUCT_TYPE)
admin.site.register(COMMENTS)
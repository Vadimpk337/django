from django.contrib import admin
from .models import User, Phone, Message, Information, Phone_operator, Comment

admin.site.register(User)
admin.site.register(Phone)
admin.site.register(Message)
admin.site.register(Information)
admin.site.register(Phone_operator)
admin.site.register(Comment)

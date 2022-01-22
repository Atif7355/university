from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,level,question_type,exam_detail,question_bank,option,answer,registration,result


# Register your models here.
class UserModel(UserAdmin):
	pass


admin.site.register(CustomUser, UserModel)
admin.site.register(level)
admin.site.register(question_type)
admin.site.register(exam_detail)
admin.site.register(question_bank)
admin.site.register(option)
admin.site.register(answer)
admin.site.register(registration)
admin.site.register(result)


from django.contrib import admin

from .models import (
    Test, Section, Question, Choice, Blank, BlankChoice
)

# Register your models here.

admin.site.register(Test)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Blank)
admin.site.register(BlankChoice)


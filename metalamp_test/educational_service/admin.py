from django.contrib import admin

from educational_service.models import *


class AmdinAnswer(admin.StackedInline):
    model = Answer


class AdminQuestion(admin.ModelAdmin):
    inlines = [AmdinAnswer]
    list_display = ('theme', 'question')


# admin.site.register(WrongAnswer)
admin.site.register(Theme)
admin.site.register(Question, AdminQuestion)
# admin.site.register(Answer)
# admin.site.register(RightAnswer)

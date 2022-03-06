from django.contrib import admin
from django.contrib.auth.models import Group

from educational_service.models import *


class AdminAnswer(admin.StackedInline):
    model = Answer


class AmdinQuestion(admin.StackedInline):
    model = Question


class AdminRightAnswer(admin.StackedInline):
    model = RightAsnwer
    max_num = 1


class AdminThemeQuestionAnswers(admin.ModelAdmin):
    inlines = [AdminAnswer, AdminRightAnswer]
    list_display = ('theme', 'question')
    search_fields = ('theme__title', 'question',)
    list_display_links = ('theme', 'question',)


class AdminRightQuestionExtraField(admin.ModelAdmin):
    model = Question
    list_display = ('theme', 'question', 'id')


class AdminThemeSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class AdminQuizComplitionInfo(admin.ModelAdmin):
    list_display = ('theme_id',)


class UserProfileRequiredFields(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser',)


class AdminMailThemeSeccess(admin.ModelAdmin):
    list_display = ('email', 'theme', 'success_percent',)
    readonly_fields = ('email', 'theme', 'success_percent',)


admin.site.register(Theme, AdminThemeSlug)
admin.site.register(UserProfile, UserProfileRequiredFields)
admin.site.register(Question, AdminThemeQuestionAnswers)
admin.site.register(MailThemeSuccess, AdminMailThemeSeccess)
admin.site.unregister(Group)

# admin.site.register(WrongAnswer)
# admin.site.register(UserProfile)
# admin.site.register(Answer)
# admin.site.register(RightAsnwer, AdminRightQuestionExtraField)
# admin.site.register(QuizComplitionInfo, AdminQuizComplitionInfo)

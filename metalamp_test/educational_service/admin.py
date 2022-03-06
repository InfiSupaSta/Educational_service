from django.contrib import admin

from educational_service.models import *


class AmdinAnswer(admin.StackedInline):
    model = Answer


class AmdinRightAnswer(admin.StackedInline):
    model = RightAsnwer


class AdminQuestion(admin.ModelAdmin):
    inlines = [AmdinAnswer, AmdinRightAnswer]
    list_display = ('theme', 'question')


class AdminRightQuestionExtraField(admin.ModelAdmin):
    model = Question
    list_display = ('theme', 'question', 'id')


class AdminThemeSlug(admin.ModelAdmin):
    # inlines = [AdminTheme]
    prepopulated_fields = {'slug': ('title',)}


class AdminQuizComplitionInfo(admin.ModelAdmin):
    list_display = ('theme_id',)


# class AmdinRightQuestion(admin.StackedInline):
#     model = Question
#
#
# class RightAnswerQuestion(admin.ModelAdmin):
#     inlines = [AmdinRightQuestion]
#
class UserProfileRequiredFields(admin.ModelAdmin):
    # model = UserProfile
    list_display = ('email', 'is_staff', 'is_superuser', )


# admin.site.register(WrongAnswer)
admin.site.register(Theme, AdminThemeSlug)
# admin.site.register(UserProfile)
admin.site.register(UserProfile, UserProfileRequiredFields)
admin.site.register(Question, AdminQuestion)
# admin.site.register(Answer)
admin.site.register(RightAsnwer, AdminRightQuestionExtraField)
admin.site.register(QuizComplitionInfo, AdminQuizComplitionInfo)

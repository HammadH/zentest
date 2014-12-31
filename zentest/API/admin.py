from django.contrib import admin

from API.models import QuestionSet, Question, Choice



class ChoiceInline(admin.StackedInline):
	model = Choice

class QuestionInline(admin.StackedInline):
	model = Question

	

class QuestionAdmin(admin.ModelAdmin):
	inlines = [ChoiceInline]

class QuestionSetAdmin(admin.ModelAdmin):
	inlines = [QuestionInline]

admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(Question, QuestionAdmin)


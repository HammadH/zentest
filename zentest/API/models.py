from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib import admin

#class Teacher(AbstractUser):



#





class QuestionSet(models.Model):
	name = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.name

class Question(models.Model):
	question = models.TextField()
	question_set = models.ForeignKey(QuestionSet, null=True)

	def __unicode__(self):
		return self.question

	def get_answer_id(self):
		try:
			return self.choices.filter(is_answer=1)[0].id
		except:
			return None

class Choice(models.Model):
	question = models.ForeignKey(Question, related_name='choices', null=True)
	value = models.CharField(max_length=225)
	is_answer = models.BooleanField(blank=False, default=False) 

	def __unicode__(self):
		return self.value

class Answer(models.Model):
	question = models.ForeignKey(Question, null=True)
	#student = 
	answer = models.ForeignKey(Choice, null=True)

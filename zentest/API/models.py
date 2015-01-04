from django.db import models

from django.contrib.auth.models import User 
from django.contrib import admin
from django.utils.text import slugify
from django.core.urlresolvers import reverse



class QuestionSet(models.Model):
	name = models.CharField(max_length=100, blank=True, unique=True)
	slug = models.SlugField(max_length=150, blank=True, unique=True)
	author = models.ForeignKey(User, blank=False, null=True)
	is_private = models.NullBooleanField(default=False, null=True)
	requires_login = models.NullBooleanField(default=False, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(QuestionSet, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('test_details_view', args=(self.slug,))

	def questions_count(self):
		return self.questions.count()

	def add_question(self):
		return reverse('add_question', args=(self.slug,))

	def start_test(self):
		return reverse('start_test', args=(self.slug,))

class Question(models.Model):
	question = models.TextField()
	question_set = models.ForeignKey(QuestionSet, null=True, related_name='questions')
	author = models.ForeignKey(User, blank=True, null=True)

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

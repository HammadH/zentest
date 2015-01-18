import simplejson
import random
import hashlib

from django.views.generic import View, FormView, TemplateView
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from API.models import *
from API.forms import *
from API.serializers import *


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

FORTUMO_IP_ADDRESSES = ['79.125.125.1', '79.125.5.205',
      '79.125.5.95', '54.72.6.126', '54.72.6.27', '54.72.6.17', '54.72.6.23']

FORTUMO_SECRET = 'e8e4239e4e3b470566cc8e1666dabc2c'


class LoginRequiredMixin(object):

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


### User Views ###

class Login(FormView):
	template_name = "login.html"
	form_class = AuthenticationForm

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(self.request, user)
			return HttpResponseRedirect(self.request.GET['next'])
		else: ## this is unchecked
			return HttpResponseRedirect(reverse('login', kwargs={'next':self.request.GET.get('next'), 
					'message':'Username or Password was incorrect!'}))

	def get_context_data(self, **kwargs):
		context = super(Login, self).get_context_data(**kwargs)
		context['next'] = self.request.GET.get('next', '/')
		return context

	
class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect(reverse('home'))

class UserRegistration(FormView):
	template_name = 'user_registration.html'
	form_class = UserRegistrationForm

	def form_valid(self, form):
		form.save()
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		login(self.request, user)
		return HttpResponseRedirect(self.request.GET['next'])

	def get_context_data(self, **kwargs):
		context = super(UserRegistration, self).get_context_data(**kwargs)
		context['next'] = self.request.GET['next']
		return context



#####################

class IndexView(View):
	def get(self, request, *args, **kwargs):
		questionSets = QuestionSet.objects.all()
		return render_to_response('home.html', {'questionsets': questionSets, 'next': '/'}, RequestContext(request))

index = IndexView.as_view()



class LoadQuestions(APIView):
	
	renderer_classes = (JSONRenderer,)

	def get(self, request, *args, **kwargs):
		_questions = Question.objects.filter(question_set__slug=kwargs.get('slug'))
		serialized_questions = QuestionSerializer(_questions, many=True)
		questions = serialized_questions.data
		random.shuffle(questions)
		
		# answer_forms =  [AnswerForm(instance=question) for question in _questions]

		# questions_and_choices = 1
		# questions = dict(zip(_questions.data, [choice for choice in serialized_choices if ))
	
		return Response(questions)

	def post(self, request, *args, **kwargs):
		post_data = simplejson.loads(self.request.POST.keys()[0])
		correct = []
		wrong = []
		#creating question objects with answer keys
		question_objs_with_keys = []
		
		for item in post_data:
			question_objs_with_keys.append({'answer':item['answer'], 'question_obj':Question.objects.get(id=item['question'])})

		for item in question_objs_with_keys:
			if item['question_obj'].get_answer_id() == int(item['answer']):
				correct.append(item['question_obj'])
			else:
				wrong.append({'question':item['question_obj'].question, 'answer':item['question_obj'].get_answer()})

		# 	Question.objects.filter(id__in=[item['question'] for item in post_data])
		# for question in answered_questions:
		# 	if Question.objects.get(id=item['question']).get_answer_id() == int(item['answer']):
		# 		correct.append

		
		result = {
		'correct': len(correct),
		'wrong': wrong,
		'total': len(post_data)
		} 

		return Response(simplejson.dumps(result))

class LoadTestPage(LoginRequiredMixin, TemplateView):
	template_name = 'testpage.html'

	def get_context_data(self, **kwargs):
		context = super(LoadTestPage, self).get_context_data(**kwargs)
		context['slug'] = kwargs['slug']
		return context

class TestDetails(View):
	def get(self, request, *args, **kwargs):
		questionSet = QuestionSet.objects.filter(slug=kwargs.get('slug'))[0]
		return render_to_response('test_detail.html', {'test': questionSet})


class CreateNewQuestionSet(LoginRequiredMixin, FormView):
	login_url = '/login/'
	form_class = NewQuestionSetForm
	template_name = 'new_questionset.html'

	def form_valid(self, form):
		self.object = form.save()
		return super(CreateNewQuestionSet, self).form_valid(form)

	def get_success_url(self):
		return reverse('add_question', args=(self.object.slug,))

createQuestionSet = CreateNewQuestionSet.as_view()


class AddQuestion(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		forms = {
		'questionForm': QuestionForm(),
		'choiceForm_1': ChoiceForm(prefix='choice_1'),
		'choiceForm_2': ChoiceForm(prefix='choice_2'),
		'choiceForm_3' :ChoiceForm(prefix='choice_3'),
		'choiceForm_4': ChoiceForm(prefix='choice_4'),
		}
		slug = kwargs['slug']
		return render_to_response('new_question.html', {'forms':forms, 'slug':slug}, RequestContext(request))

	def post(self, request, *args, **kwargs):
		questionForm = QuestionForm(request.POST)
		choiceForm_1 = ChoiceForm(request.POST, prefix='choice_1')
		choiceForm_2 = ChoiceForm(request.POST, prefix='choice_2')
		choiceForm_3 = ChoiceForm(request.POST, prefix='choice_3')
		choiceForm_4 = ChoiceForm(request.POST, prefix='choice_4')
		if all([questionForm.is_valid(), choiceForm_1.is_valid(), choiceForm_2.is_valid(),
			choiceForm_3.is_valid(), choiceForm_4.is_valid()]):
			questionSetSlug = kwargs.get('slug')
			question = Question.objects.create(
				question=questionForm.cleaned_data['question'],
				question_set=QuestionSet.objects.get(slug=questionSetSlug),
				)
			choice_1 = Choice.objects.create(question=question, 
				value=choiceForm_1.cleaned_data['value'],
				is_answer=choiceForm_1.cleaned_data['is_answer'])
			choice_2 = Choice.objects.create(question=question, 
				value=choiceForm_2.cleaned_data['value'],
				is_answer=choiceForm_2.cleaned_data['is_answer'])
			choice_3 = Choice.objects.create(question=question, 
				value=choiceForm_3.cleaned_data['value'],
				is_answer=choiceForm_3.cleaned_data['is_answer'])
			choice_4 = Choice.objects.create(question=question, 
				value=choiceForm_4.cleaned_data['value'],
				is_answer=choiceForm_4.cleaned_data['is_answer'])
			return HttpResponseRedirect(reverse('add_question', args=(questionSetSlug,)))
		else:
			forms = {
			'questionForm': QuestionForm(request.POST),
			'choiceForm_1': ChoiceForm(request.POST, prefix='choice_1'),
			'choiceForm_2': ChoiceForm(request.POST, prefix='choice_2'),
			'choiceForm_3': ChoiceForm(request.POST, prefix='choice_3'),
			'choiceForm_4': ChoiceForm(request.POST, prefix='choice_4'),

			}
			return render('new_question.html', {'forms':forms}, RequestContext(request))

### SMS PAYMENT VIEWS ###

def wrong_signature(params):
	sorted_param_keys = sorted(params)
	concat_str = ''
	for key in sorted_param_keys:
		if key != 'sig':
			concat_str += key + '=' + params[key]
	concat_str += FORTUMO_SECRET
	sig = hashlib.md5(concat_str).hexdigest()
	if params['sig'] != sig:
		return True
	else:
		return False

class SMSPayment(View):
	def get(self, request, *args, **kwargs):
		"""
		make security checks (validate IP addresses, check the signature) 
		to validate that the request came from Fortumo
		"""

		
		if request.META['REMOTE_ADDR'] not in FORTUMO_IP_ADDRESSES:
			return HttpResponseForbidden()

		if wrong_signature(request.GET):
			return HttpResponseForbidden()

		sender = request.GET['sender']
		message = request.GET['message']
		message_id = request.GET['message_id']

		# hint:use message_id to log your messages
  		# additional parameters: country, price, currency, operator, keyword, shortcode
  		# do something with sender and message

  		reply = "Thank you for making payment"

  		status = request.GET['status']

  		if status in ['OK', 'pending']:
  			return HttpResponse(reply)

  		else:
  			return HttpResponse('status failed')






# class SMSBilling(View):
# 	def get(self, request, *args, **kwargs):
# 		pass

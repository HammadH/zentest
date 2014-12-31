import simplejson
import random

from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext



from API.models import *
from API.forms import *
from API.serializers import *


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

class HomeView(APIView):
	
	renderer_classes = (JSONRenderer,)

	def get(self, request, *args, **kwargs):
		_questions = Question.objects.all()
		serialized_questions = QuestionSerializer(_questions, many=True)
		questions = serialized_questions.data
		random.shuffle(questions)
		
		# answer_forms =  [AnswerForm(instance=question) for question in _questions]

		# questions_and_choices = 1
		# questions = dict(zip(_questions.data, [choice for choice in serialized_choices if ))
	
		return Response(questions)

	def post(self, request, *args, **kwargs):
		post_data = simplejson.loads(self.request.POST.keys()[0])
		correct = 0
		#questions = Question.objects.filter(id__in=[item['question'] for item in post_data])
		
		for item in post_data:
			if Question.objects.get(id=item['question']).get_answer_id() == int(item['answer']):
				correct = correct+1
			
		result = {
		'correct': correct,
		'total': len(post_data)
		} 

		
		return Response(simplejson.dumps(result))



class IndexView(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('testpage.html')

index = IndexView.as_view()


from django import forms

from API.models import *


class AnswerForm(forms.ModelForm):
	answer = forms.ModelChoiceField(queryset=Choice.objects.all(), widget=forms.RadioSelect())
	class Meta:
		model = Answer
		fields = ('answer',)

	def __init__(self, *args, **kwargs):
		super(AnswerForm, self).__init__(*args, **kwargs)
		self.question = kwargs['instance']
		self.fields['answer'].queryset = Choice.objects.filter(question=self.question)	


class NewQuestionSetForm(forms.ModelForm):
	class Meta:
		model = QuestionSet
		fields = ('name',)

class QuestionForm(forms.ModelForm): 
	class Meta:
		model = Question
		fields = ('question',)

class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ('value', 'is_answer')

	# def __init__(self, id, *args, **kwargs):
	# 	super(ChoiceForm, self).__init__(*args, **kwargs)
	# 	import pdb;pdb.set_trace()
	# 	self.fields['is_answer'].widget.attrs = {'name':kwargs.get('id')}
	
	




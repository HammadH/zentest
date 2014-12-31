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



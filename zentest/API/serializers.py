from rest_framework import serializers

from API.models import *

class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Choice
		fields = ('pk', 'value')


class QuestionSerializer(serializers.ModelSerializer):
	choices = ChoiceSerializer(many=True)
	class Meta:
		model = Question
		fields = ('question','choices','pk')

class AnswerSerializer(serializers.ModelSerializer):
	def get_fields(self, *args, **kwargs):
		fields = super(AnswerSerializer, self).get_fields(*args, **kwargs)
		fields['answer'].queryset = Choice.objects.filter(question=kwargs['question']) 
		return fields

	class Meta:
		model = Answer
		fields = ('answer',)

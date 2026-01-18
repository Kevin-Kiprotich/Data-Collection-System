from rest_framework import serializers
from .models import Questionnaire, Question, SkipLogic, FilterLogic, Submission, Answer

class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'
    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class SkipLogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkipLogic
        fields = '__all__'

class FilterLogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterLogic
        fields = '__all__'
        
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
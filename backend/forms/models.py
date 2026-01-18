import uuid
from django.contrib.gis.db import models

# Create your models here.
class Questionnaire(models.Model):
    id= models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    creator = models.ForeignKey('accounts.User', related_name='questionnaires', on_delete=models.DO_NOTHING, null=False)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    # is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    id=models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    questionnaire = models.ForeignKey(Questionnaire, related_name='questions', on_delete=models.CASCADE)
    question= models.CharField(max_length=500, null=False)
    question_type = models.CharField(max_length=50,null=False, choices=[
        ('TEXT', 'Text'),
        ('NUMBER', 'Number'),
        ('FILE', 'File'),
        ('GEOMETRY', 'Geometry'),
        ('CHOICE', 'Choice'),
        
    ], default='TEXT'),
    answer_type=models.CharField(max_length=50,null=False, choices=[
        ('SHORT_TEXT', 'Short Text'),
        ('LONG_TEXT', 'Long Text'),
        ('PHONE_NUMBER', 'Phone Number'),
        ('EMAIL', 'Email'),
        ('TIMESTAMP', 'Timestamp'),
        ('LINK', 'Link'),
        ('INTEGER', 'Integer'),
        ('DECIMAL', 'Decimal'),
        ('POINT', 'Point'),
        ('LINE', 'Line'),
        ('POLYGON', 'Polygon'),
        ('SINGLE_CHOICE', 'Single Choice'),
        ('MULTI_CHOICE', 'Multiple Choice'),
        ('IMAGE', 'Image'),
        ('DOCUMENT', 'Document'),
        ('VIDEO', 'Video'),
        ('AUDIO', 'Audio'),
    ], default='SHORT_TEXT')
    is_required = models.BooleanField(default=False),
    required_text = models.CharField(max_length=200, null=True, blank=True)
    options= models.TextField(null=True, blank=True, help_text="Comma-separated options for CHOICE type questions")
    placeholder = models.CharField(max_length=200, null=True, blank=True)
    hint = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.question

class SkipLogic(models.Model):
    id=models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.ForeignKey(Question, related_name='skip_logics', on_delete=models.CASCADE)
    answer_value = models.CharField(max_length=5000, null=False)
    display_question = models.ForeignKey(Question, related_name='skipped_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"If answer is {self.answer_value}, show {self.display_question.question}"

class FilterLogic(models.Model):
    id=models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.ForeignKey(Question, related_name='filter_choice_logics', on_delete=models.CASCADE)
    source_question = models.ForeignKey(Question, related_name='filtered_by', on_delete=models.CASCADE)
    mapping = models.TextField(null=False, help_text="Mapping in the format 'source_value1:choice1,choice2;source_value2:choice3,choice4'")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Filter choices of '{self.question.question}' based on '{self.source_question.question}'"

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    questionnaire = models.ForeignKey(Questionnaire, related_name='submissions', on_delete=models.CASCADE, null=False)
    enumerator=models.ForeignKey('accounts.User', related_name='submissions', on_delete=models.DO_NOTHING, null=False)
    fill_duration = models.DurationField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.questionnaire.title}"
       
class Answer(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    long_text_answer = models.TextField(null=True, blank=True)
    short_text_answer = models.CharField(max_length=500, null=True, blank=True)
    link_answer = models.URLField(null=True, blank=True)
    phone_number_answer = models.CharField(max_length=20, null=True, blank=True)
    email_answer = models.EmailField(null=True, blank=True)
    timestamp_answer = models.DateTimeField(null=True, blank=True)
    integer_answer = models.IntegerField(null=True, blank=True)
    decimal_answer = models.DecimalField(max_digits=100, decimal_places=6, null=True, blank=True)
    single_choice_answer = models.CharField(max_length=200, null=True, blank=True)
    multi_choice_answer = models.TextField(null=True, blank=True, help_text="Comma-separated values for multiple choices")
    line_answer = models.LineStringField(null=True, blank=True)
    point_answer = models.PointField(null=True, blank=True)
    polygon_answer = models.PolygonField(null=True, blank=True)
    document_answer = models.FileField(upload_to='documents/', null=True, blank=True)
    image_answer = models.ImageField(upload_to='images/', null=True, blank=True)
    video_answer = models.FileField(upload_to='videos/', null=True, blank=True)
    audio_answer = models.FileField(upload_to='audio/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
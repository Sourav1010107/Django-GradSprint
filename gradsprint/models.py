from django.db import models
from django.conf import settings 

from .choices import (TYPE_CHOICES, TEST_SUBTOPIC_CHOICES ,TEST_TOPIC_CHOICES, 
                      DIFFICULTIES)


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Section(models.Model):
    test = models.ForeignKey(Test, on_delete= models.CASCADE, related_name="sections")
    name = models.CharField(max_length=200)
    time = models.IntegerField()
    order = models.IntegerField()

    class Meta:
            ordering = ["order"]

    def __str__(self):
        return f"{self.test.name} - {self.name}"



class Question(models.Model):

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="questions")

    #question behavior- student model property
    topic = models.CharField(max_length=100, choices= TEST_TOPIC_CHOICES, blank=True, null=True)
    subtopic = models.CharField(max_length=100, choices=TEST_SUBTOPIC_CHOICES, blank=True, null=True)
    expected_time_seconds = models.PositiveIntegerField(default=90, blank=True, null=True)

    question_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    difficulty = models.CharField(max_length=50, choices=DIFFICULTIES)
    image = models.ImageField(upload_to="question_images/", blank=True, null=True)
    question = models.TextField()
    quantity_a = models.TextField(null=True, blank=True)
    quantity_b = models.TextField(null=True, blank=True)
    instruction = models.TextField()
    passage = models.TextField(blank=True, null=True)
    passage_ref = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="linked_questions")
    explanation = models.TextField(blank=True)
    order = models.IntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.section.name} - Q{self.order}"



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.TextField()
    order = models.IntegerField()
    is_correct = models.BooleanField(default= False) 

    class Meta:
            ordering = ["order"]

    def __str__(self):
        return self.text



class Blank(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="blanks")
    order = models.IntegerField()

    class Meta:
            ordering = ["order"]

    def __str__(self):
        return f"Blank {self.order}"



class BlankChoice(models.Model):
    blank = models.ForeignKey(Blank, on_delete=models.CASCADE, related_name="choices")
    text = models.TextField()
    order = models.IntegerField()
    is_correct = models.BooleanField(default= False)  

    class Meta:
            ordering = ["order"]

    def __str__(self):
        return self.text

class NumericValue(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="numeric_value")
    correct_value = models.DecimalField(max_digits=12, decimal_places=2, default= 0 )

    def __str__(self):
        return str(self.correct_value)

    

class StudentAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="student_answers")

    selected_answer = models.JSONField(default=list, blank=True)
    is_correct = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - Question {self.question_id}"


class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_results")
    test = models.ForeignKey("Test", on_delete=models.CASCADE, related_name="test_results")

    verbal_score = models.PositiveIntegerField(default=130)
    quant_score = models.PositiveIntegerField(default=130)
    total_score = models.PositiveIntegerField(default=260)

    correct_answers = models.PositiveIntegerField(default=0)
    total_attempted_question = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    @property
    def accuracy(self):
        if self.total_attempted_question == 0:
            return 0
        return round(
            (self.correct_answers/self.total_attempted_question)*100, 1
        )
    def __str__(self):
        return f"{self.user} - {self.total_score}"
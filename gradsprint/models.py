from django.db import models

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

    def __str__(self):
        return f"{self.test.name} - {self.name}"



class Question(models.Model):
    TYPE_CHOICES = [
        ("text-completion", "Text Completion"),
        ("text-completion-double", "Text Completion Double"),
        ("text-completion-triple", "Text Completion Triple"),
        ("sentence-equivalence", "Sentence Equivalence"),
        ("reading-single", "Reading Single"),
        ("reading-multiple", "Reading Multiple"),
    ]
    DIFFICULTIES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("very-hard", "Very Hard"),
    ]

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="questions")

    question_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    difficulty = models.CharField(max_length=50, choices=DIFFICULTIES)

    question = models.TextField()
    instruction = models.TextField()
    passage = models.TextField(blank=True, null=True)
    passage_ref = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="passage_questions")
    max_selections = models.IntegerField(default=1, blank=True, null=True)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.section.name} - Q{self.order}"



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.TextField()
    order = models.IntegerField()
    is_correct = models.BooleanField(default= False) 

    def __str__(self):
        return self.text



class Blank(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="blanks")
    order = models.IntegerField()

    def __str__(self):
        return f"Blank {self.order}"



class BlankChoice(models.Model):
    blank = models.ForeignKey(Blank, on_delete=models.CASCADE, related_name="choices")
    text = models.TextField()
    order = models.IntegerField()
    is_correct = models.BooleanField(default= False)    
    def __str__(self):
        return self.text
    

from django.db import models
######### Entities of the database being used #########
######### Must makemigrations and migrate when and if any changes are made #########
class Page(models.Model):
    page_id = models.AutoField(primary_key=True)
    prev_page = models.PositiveSmallIntegerField(default=0)
    next_page = models.PositiveSmallIntegerField(default=0)
    text = models.TextField(max_length=1000)
    step = models.PositiveSmallIntegerField(default=0)
    page_score = models.PositiveSmallIntegerField(default=0)

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    imgname = models.CharField(max_length=100)

class Quote(models.Model):
    quote_id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

class Title(models.Model):
    title_id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

class Button(models.Model):
    button_id = models.AutoField(primary_key=True)
    next_page = models.ForeignKey(Page, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

class ButtonAction(models.Model):
    button_action_id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    button = models.ForeignKey(Button, on_delete=models.CASCADE)

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=50)
    worth_points = models.BooleanField(default=False)

class MultichoiceAnswer(models.Model):
    multichoice_answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    next_page = models.ForeignKey(Page, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

class CheckboxAnswer(models.Model):
    checkbox_answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    correct = models.BooleanField(default=False)

class Score(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    current_score = models.PositiveSmallIntegerField(default=0)
    current_step = models.PositiveSmallIntegerField(default=0)
    nextqp = models.PositiveSmallIntegerField(default=0)

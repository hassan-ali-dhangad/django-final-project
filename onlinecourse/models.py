from django.db import models

class Question(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=True)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True)
        selected_correct = all_answers.filter(id__in=selected_ids)
        if selected_correct.count() == all_answers.count() and len(selected_ids) == all_answers.count():
            return True
        return False

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, null=True)
    choices = models.ManyToManyField(Choice)

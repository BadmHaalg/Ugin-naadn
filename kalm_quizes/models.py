from django.db import models

# Create your models here.


class Quiz(models.Model):
    quiz_number = models.IntegerField(default=0)
    quiz_name = models.CharField(max_length=150)

    def __str__(self):
        return self.quiz_name

    def single_choice_count(self):
        count = self.singlechoice_set.count()
        return count

    def multiple_choice_count(self):
        count = self.multiplechoice_set.count()
        return count

    def put_in_order_count(self):
        count = self.putinorder_set.count()
        return count

    def get_count_all(self):
        count_all = self.single_choice_count() + self.multiple_choice_count() + self.put_in_order_count()
        return count_all

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class SingleChoice(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.IntegerField(default=0)
    question_text = models.TextField(unique=True)
    right_answer = models.CharField(max_length=100)
    wrong_answer_1 = models.CharField(max_length=100)
    wrong_answer_2 = models.CharField(max_length=100)
    wrong_answer_3 = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.question_number}. {self.question_text}'

    class Meta:
        verbose_name = 'Вопрос с одним вариантом ответа'
        verbose_name_plural = 'Вопросы с одним вариантом ответа'


class MultipleChoice(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.IntegerField(default=0)
    question_text = models.TextField(unique=True)

    def __str__(self):
        return f'{self.question_number}. {self.question_text}'

    class Meta:
        verbose_name = 'Вопрос с несколькими вариантами ответа'
        verbose_name_plural = 'Вопросы с несколькими вариантами ответа'


class PutInOrder(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.IntegerField(default=0)
    question_text = models.TextField(default='')
    text_for_ordering = models.TextField(default='')

    def __str__(self):
        return f'{self.question_number}. {self.question_text}'

    class Meta:
        verbose_name = 'Задание на порядок слов'
        verbose_name_plural = 'Задания на порядок слов'


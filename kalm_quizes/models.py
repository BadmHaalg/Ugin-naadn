from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Quiz(models.Model):
    quiz_number = models.IntegerField(default=0)
    quiz_name = models.CharField(max_length=150)

    def __str__(self):
        return self.quiz_name

    def single_choice_count(self):
        count = self.singlechoice_set.count()
        return count

    def put_in_gaps_count(self):
        count = self.putingaps_set.count()
        return count

    def put_in_order_count(self):
        count = self.putinorder_set.count()
        return count

    def get_count_all(self):
        count_all = self.single_choice_count() + self.put_in_order_count() + self.put_in_gaps_count()
        return count_all

    def get_all_related(self): #Можно ли QuerySet перевести в список?
        single_choice_list = [obj for obj in self.singlechoice_set.all()]
        put_in_order_list = [obj for obj in self.putinorder_set.all()]
        put_in_gaps_list = [obj for obj in self.putingaps_set.all()]
        return single_choice_list + put_in_order_list + put_in_gaps_list

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

    def type(self):
        return 'SingleChoice'

    def url(self):
        url = "{% url 'kalm_quizes:single_choice_page' 1 1 %}"
        return url

    class Meta:
        verbose_name = 'Вопрос с одним вариантом ответа'
        verbose_name_plural = 'Вопросы с одним вариантом ответа'


class PutInGaps(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.IntegerField(default=0)
    question_text = models.TextField(unique=True)
    right_answer = models.CharField(max_length=225, default='')
    choices_list = models.CharField(max_length=225, default='')

    def __str__(self):
        return f'{self.question_number}. {self.question_text}'

    def type(self):
        return 'PutInGaps'

    class Meta:
        verbose_name = 'Задание на заполнение пропусков'
        verbose_name_plural = 'Задания для заполнения пропусков'


class PutInOrder(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.IntegerField(default=0)
    question_text = models.TextField(default='')
    text_for_ordering = models.TextField(default='')

    def __str__(self):
        return f'{self.question_number}. {self.question_text}'

    def type(self):
        return 'PutInOrder'

    class Meta:
        verbose_name = 'Задание на порядок слов'
        verbose_name_plural = 'Задания на порядок слов'


class UserCourseProfile(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserCourseAnswers(models.Model):
    user = models.IntegerField()
    quiz = models.IntegerField()
    question = models.IntegerField(default=0)
    result = models.IntegerField(default=0)









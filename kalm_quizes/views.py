from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.shortcuts import get_object_or_404, render
# Create your views here.
from .forms import RegisterUserForm
from .models import *

from random import shuffle

menu = ['Главная', 'Курсы', 'Глоссарий', 'О проекте', 'Список задач', 'Войти']  # через список словарей удобней


def index_page(request):
    title = 'Список курсов'
    quizes_list = Quiz.objects.all()
    context = {
        'title': title,
        'menu': menu,
        'quizes_list': quizes_list
    }
    return render(request, 'kalm_quizes/index.html', context)


def about_page(request):
    title = 'О проекте'
    text = 'Здесь будет размещаться информация о проекте, планы и прочее'
    context = {
        'title': title,
        'text': text,
    }
    return render(request, 'kalm_quizes/about.html', context)


def glossary_page(request):
    text = """Планируем здесь сделать грамматический справочник,
            который будет расширяться по мере добавления курсов.
            Глоссарий и курсы должны дополнять друг друга, содержать взаимные ссылки.
            То есть глоссарий - раздел с теорией, а курсы - практическое её освоение.
            Глоссарий необязательно подает информацию в текстовом варианте - любые формы
            (аудио, видео в разных подачах) приветствуются.
                """
    title = 'Глоссарий'
    context = {
        'title': title,
        'text': text,
    }

    return render(request, 'kalm_quizes/glossary.html', context)


def get_quiz_stat(request):
    """счетчик прогресса
    по сути по каждому вопросу для каждого
    пользователя в каждом курсе хранится результат
    0 - неправильно или ответ не дан
    1 - правильно"""
    if request.user.is_authenticated:
        quizes_stat = []
        user_profile_records = request.user.usercourseprofile_set.all()
        for rec in user_profile_records:
            right_answers_count = len(UserCourseAnswers.objects.filter(user=rec.user_id,
                                                                       quiz=rec.quiz_id,
                                                                       result=1))
            quiz = Quiz.objects.get(pk=rec.quiz_id)
            quizes_stat.append((quiz, right_answers_count))
    else:
        quizes_stat = None

    return quizes_stat


def profile_page(request):
    context = {
        'request': request,
        'quizes_stat': get_quiz_stat(request),
    }
    return render(request, 'kalm_quizes/profile_page.html', context)


def user_profile_decorator(func):
    """создает обьект UserCourseProfile(т.е. записывает
     пользователя на курс), когда пользователь заходит
      на страницу курса. Желательно вывести в отдельную
      кнопку ЗАПИСАТЬСЯ НА КУРС"""
    def quiz_page_wrapper(request, quiz_id):
        user_pk = request.user.pk
        profile = None
        if request.user.is_authenticated:
            try:
                profile = UserCourseProfile.objects.get(user_id=user_pk, quiz_id=quiz_id)
            except UserCourseProfile.DoesNotExist:
                profile = UserCourseProfile.objects.create(quiz_id=quiz_id, user_id=user_pk)
        return func(request, quiz_id, profile)

    return quiz_page_wrapper


def answer_decorator(question_page):
    """отвечает за изменение счетчика прогресса при нажатии кнопки ОТВЕТИТЬ"""
    def question_wrapper(request, quiz_id, question_id):
        user_pk = request.user.pk
        answer_status = None
        if request.user.is_authenticated:
            try:
                answer_status = UserCourseAnswers.objects.get(user=user_pk,
                                                              quiz=quiz_id,
                                                              question=question_id)
            except UserCourseAnswers.DoesNotExist:
                answer_status = UserCourseAnswers.objects.create(user=user_pk,
                                                                 quiz=quiz_id,
                                                                 question=question_id)
        return question_page(request, quiz_id, question_id, answer_status)
    return question_wrapper


@user_profile_decorator
def quiz_page(request, quiz_id, profile):
    """страница курса"""
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    single_choices_list = quiz.singlechoice_set.all()
    put_in_gaps_list = quiz.putingaps_set.all()
    put_in_order_list = quiz.putinorder_set.all()
    context = {
        'menu': menu,
        'quiz': quiz,
        'single_choices_list': single_choices_list,
        'put_in_order_list': put_in_order_list,
        'put_in_gaps_list': put_in_gaps_list,
        'profile': profile,
        'quizes_stat': get_quiz_stat(request)

    }

    return render(request, 'kalm_quizes/quiz_page_template.html', context)


# @answer_decorator
# def one_big_function(request, quiz_id, question_id, answer_status):
#     quiz = get_object_or_404(Quiz, pk=quiz_id)
#     question = [obj for obj in quiz.get_all_related()
#                 if obj.question_number == question_id]
#
#     context = {
#         'menu': menu,
#         'quiz': quiz,
#         'question': question,
#         'single_choice_count': quiz.single_choice_count,  # это кажется можно заменить
#         'put_in_order_count': quiz.put_in_order_count,
#         'put_in_gaps_count': quiz.put_in_gaps_count,
#         'sum': quiz.get_count_all,
#         'answer_status': answer_status,
#         'quizes_stat': get_quiz_stat(request),
#     }
#
#     if question.type() == 'SingleChoice':
#         answers_set = [question.right_answer, question.wrong_answer_1,
#                        question.wrong_answer_2, question.wrong_answer_3]
#         context['answers_set'] = answers_set
#         pass
#     elif question.type() == 'PutInOrder':
#         pass
#     elif question.type() == 'PutInGaps':
#         pass

#
# def prosloika(request, quiz_id, question_id):
#     quiz = get_object_or_404(Quiz, pk=quiz_id)
#     question = [obj for obj in quiz.get_all_related() if obj.question_number == question_id][0]
#     if question.type == 'SingleChoice':
#         return single_choice_page(request, quiz_id, question_id)
#     elif question.type == 'PutInOrder':
#         return put_in_order_page(request, quiz_id, question_id)
#     elif question.type == 'PutInGaps':
#         return put_in_gaps_page(request, quiz_id, question_id)


@answer_decorator
def single_choice_page(request, quiz_id, question_id, answer_status):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.singlechoice_set.get(question_number=question_id)#отличается
    answers_set = [question.right_answer, question.wrong_answer_1,
                   question.wrong_answer_2, question.wrong_answer_3]
                    #можно просто написать, get_asnwers_set?
    shuffle(answers_set)
    context = {
        'menu': menu,
        'quiz': quiz,
        'question': question,
        'answers_set': answers_set,
        'single_choice_count': quiz.single_choice_count, #это кажется можно заменить
        'put_in_order_count': quiz.put_in_order_count,
        'put_in_gaps_count': quiz.put_in_gaps_count,
        'sum': quiz.get_count_all,
        'answer_status': answer_status,
        'quizes_stat': get_quiz_stat(request)
    }
    if request.method == 'POST':
        try:
            selected_answer = request.POST['answer']
            context['selected_answer'] = selected_answer
            if selected_answer == question.right_answer:
                context['message'] = 'Правильно!'
                if request.user.is_authenticated:
                    answer_status.result = '1'
                    answer_status.save()
            else:
                context['message'] = 'Пока неправильно, пробуйте еще!'
        except MultiValueDictKeyError:
            context['message'] = 'Вы не выбрали ответ!'

    return render(request, 'kalm_quizes/single_choice_template.html', context)


@answer_decorator
def put_in_order_page(request, quiz_id, question_id, answer_status):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.putinorder_set.get(question_number=question_id)
    words_set = question.text_for_ordering.split()
    shuffle(words_set)
    context = {
        'menu': menu,
        'quiz': quiz,
        'question': question,
        'text': words_set,
        'range': range(len(words_set)),
        'request': request,
        'single_choice_count': quiz.single_choice_count,
        'put_in_order_count': quiz.put_in_order_count,
        'put_in_gaps_count': quiz.put_in_gaps_count,
        'sum': quiz.get_count_all,
        'answer_status': answer_status,
        'quizes_stat': get_quiz_stat(request)
    }
    if request.method == 'POST':
        words_list = []
        for selected_word in request.POST:
            if selected_word != 'csrfmiddlewaretoken':
                words_list.append(request.POST[selected_word])
        context['range'] = words_list
        if words_list == question.text_for_ordering.split():
            context['message'] = 'Верно!'
            if request.user.is_authenticated:
                answer_status.result = '1'
                answer_status.save()
        elif 'none' in words_list:
            context['message'] = 'Заполните все ячейки!'
        else:
            context['message'] = 'Пока неправильно, пробуйте еще!'

    return render(request, 'kalm_quizes/order_template.html', context)


@answer_decorator
def put_in_gaps_page(request, quiz_id, question_id, answer_status):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.putingaps_set.get(question_number=question_id)
    choices_list = question.choices_list.split()
    shuffle(choices_list)
    context = {
        'menu': menu,
        'quiz': quiz,
        'question': question,
        'choices_list': choices_list,
        'text_split': question.question_text.split(),
        'request': request,
        'single_choice_count': quiz.single_choice_count,
        'put_in_order_count': quiz.put_in_order_count,
        'put_in_gaps_count': quiz.put_in_gaps_count,
        'sum': quiz.get_count_all,
        'answer_status': answer_status,
        'quizes_stat': get_quiz_stat(request)
    }

    if request.method == 'POST':
        words_list = []
        words_dict = {}
        for selected_word in request.POST:
            if selected_word != 'csrfmiddlewaretoken':
                words_list.append(request.POST[selected_word])
                words_dict[selected_word] = request.POST[selected_word]
        context['words_dict'] = words_dict
        if words_list == question.right_answer.split():
            context['message'] = 'Верно!'
            if request.user.is_authenticated:
                answer_status.result = '1'
                answer_status.save()
        elif 'none' in words_list:
            context['message'] = 'Заполните все пропуски!'
        else:
            context['message'] = 'Неверно!'

    return render(request, 'kalm_quizes/put_in_gaps_template.html', context)


class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

#попробуем написать функцию прослойку?
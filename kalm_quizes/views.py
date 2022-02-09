from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.shortcuts import get_object_or_404, render
# Create your views here.

from .models import *


class IndexView(generic.ListView):
    template_name = 'kalm_quizes/index.html'
    context_object_name = 'quizes_list'

    def get_queryset(self):
        return Quiz.objects.all()


def quiz_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    single_choices_list = quiz.singlechoice_set.all()
    multiple_choices_list = quiz.multiplechoice_set.all()
    put_in_order_list = quiz.putinorder_set.all()
    context = {
        'quiz': quiz,
        'single_choices_list': single_choices_list,
        'multiple_choices_list': multiple_choices_list,
        'put_in_order_list': put_in_order_list,
    }

    return render(request, 'kalm_quizes/quiz_page_template.html', context)


def put_in_order_page(request, quiz_id, put_in_order_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.putinorder_set.get(question_number=put_in_order_id)
    words_set = set(question.text_for_ordering.split())
    context = {'quiz': quiz,
               'question': question,
               'text': words_set,
               'range': range(len(words_set))}

    return render(request, 'kalm_quizes/order_template.html', context)


def put_in_order_check(request, quiz_id, put_in_order_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.putinorder_set.get(question_number=put_in_order_id)
    words_set = set(question.text_for_ordering.split())
    rr = [i for i in range(len(words_set))]
    context = {'quiz': quiz,
               'question': question,
               'text': words_set,
               'range': rr,
               }
    words_list = []
    for i in range(len(words_set)):
        name = f'word{i}'
        selected_word = request.POST[name]
        words_list.append(selected_word)
    if words_list == question.text_for_ordering.split():
        context['message'] = 'Верно!'
    elif 'none' in words_list:
        context['message'] = 'Заполните все ячейки!'
    else:
        context['message'] = 'Пока неправильно, пробуйте еще!'

    return render(request, 'kalm_quizes/order_template.html', context)


# def single_choice_page(request, quiz_id, single_choice_id):
#     quiz = get_object_or_404(Quiz, pk=quiz_id)
#     question = quiz.singlechoice_set.get(question_number=single_choice_id)
#     answers_set = {question.right_answer, question.wrong_answer_1, question.wrong_answer_2, question.wrong_answer_3}
#     context = {
#         'quiz': quiz,
#         'question': question,
#         'answers_set': answers_set,
#     }
#
#     return render(request, 'kalm_quizes/single_choice_template.html', context)


def single_choice_page(request, quiz_id, single_choice_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.singlechoice_set.get(question_number=single_choice_id)
    answers_set = {question.right_answer, question.wrong_answer_1, question.wrong_answer_2, question.wrong_answer_3}
    context = {
        'quiz': quiz,
        'question': question,
        'answers_set': answers_set,
    }
    if request.method == 'POST':
        try:
            selected_answer = request.POST['answer']
            if selected_answer == question.right_answer:
                context['message'] = 'Правильно!'
                context['selected_answer'] = selected_answer
            else:
                context['message'] = 'Пока неправильно, пробуйте еще!'
                context['selected_answer'] = selected_answer
        except MultiValueDictKeyError:
            context['message'] = 'Вы не выбрали ответ!'
    else:
        return render(request, 'kalm_quizes/single_choice_template.html', context)

    return render(request, 'kalm_quizes/single_choice_template.html', context)
    # 1. Кстати да, можно перенаправлять на эту же страницу (_template), но с сообщением (как в случае)
    # с незаполненной формой. Только вот эти вот штуки про повторную отправку формы нужно реализовать
    # и про сохранение заполненной информации
    # 2. Также сделать навигацию (вперед-назад по вопросам, и уже навигацию по сайту от базового шаблона )
    # ТЕПЕРЬ РЕАЛИЗОВАТЬ С СОХРАНЕНИЕМ ЗАПОЛНЕННОЙ ФОРМЫ!!!

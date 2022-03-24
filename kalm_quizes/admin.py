from django.contrib import admin

# Register your models here.
from .models import *


class SingleChoiceInline(admin.StackedInline):
    model = SingleChoice
    extra = 0


class PutInGapsInline(admin.StackedInline):
    model = PutInGaps
    extra = 0


class PutInOrderInline(admin.StackedInline):
    model = PutInOrder
    extra = 0


class QuizAdmin(admin.ModelAdmin):
    fields = ['quiz_number', 'quiz_name']
    inlines = [SingleChoiceInline, PutInOrderInline, PutInGapsInline]
    list_display = ('quiz_number', 'quiz_name')
    list_filter = ['quiz_number']


admin.site.register(Quiz, QuizAdmin)


from django.contrib import admin

# Register your models here.
from .models import Question, Choice

# admin.site.register(Question)


# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']  # 表单中的排序方式

# class ChoiceInline(admin.StackedInline):   # StackedInline,TabularInline 不同的表单样式
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    list_display = ('question_text', 'pub_date', 'was_published_recently')


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')  # 展示列表
    list_filter = ['pub_date']  # 过滤器
    search_fields = ['question_text']  # 查找器


admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
from django import forms
from video.models import Video, Classification


class VideoPublishForm(forms.ModelForm):
    title = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': '至少4个字符',
                                  'max_length': '不能多于200个字符',
                                  'required': '标题不能为空'
                              },
                              widget=forms.TextInput(attrs={'placeholder': '请输入内容'}))
    desc = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': '至少4个字符',
                                  'max_length': '不能多于200个字符',
                                  'required': '描述不能为空'
                              },
                              widget=forms.Textarea(attrs={'placeholder': '请输入内容'}))
    cover = forms.ImageField(required=True,
                             error_messages={
                                 'required': '封面不能为空'
                             },
                             widget=forms.FileInput(attrs={'class' : 'n'}))
    status = forms.CharField(min_length=1, max_length=1, required=False,
                             widget=forms.HiddenInput(attrs={'value':'0'}))
    class Meta:
        model = Video
        fields = ['title', 'desc','status', 'cover', 'classification']



class VideoEditForm(forms.ModelForm):
    title = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': '至少4个字符',
                                  'max_length': '不能多于200个字符',
                                  'required': '标题不能为空'
                              },
                              widget=forms.TextInput(attrs={'placeholder': '请输入内容'}))
    desc = forms.CharField(min_length=4, max_length=200, required=True,
                              error_messages={
                                  'min_length': '至少4个字符',
                                  'max_length': '不能多于200个字符',
                                  'required': '描述不能为空'
                              },
                              widget=forms.Textarea(attrs={'placeholder': '请输入内容'}))
    cover = forms.ImageField(required=True,
                             error_messages={
                                 'required': '封面不能为空'
                             },
                             widget=forms.FileInput(attrs={'class' : 'n'}))

    status = forms.CharField(min_length=1,max_length=1,required=False,
                             widget=forms.HiddenInput())

    # classification = forms.ModelChoiceField(queryset=Classification.objects.all())
    # classification = forms.CharField(min_length=1,max_length=1,required=False,
    #                          widget=forms.HiddenInput())

    class Meta:
        model = Video
        fields = ['title', 'desc', 'status', 'cover','classification']


class ClassificationAddForm(forms.ModelForm):
    title = forms.CharField(min_length=2, max_length=30, required=True,
                            error_messages={
                                'min_length': '至少2个字符',
                                'max_length': '不能多于30个字符',
                                'required': '不能为空'
                            },
                            widget=forms.TextInput(attrs={'placeholder': '请输入分类名称'}))
    class Meta:
        model = Classification
        fields = ['title', 'status' ]


class ClassificationEditForm(forms.ModelForm):
    title = forms.CharField(min_length=2, max_length=30, required=True,
                              error_messages={
                                  'min_length': '至少2个字符',
                                  'max_length': '不能多于30个字符',
                                  'required': '不能为空'
                              },
                              widget=forms.TextInput(attrs={'placeholder': '请输入分类名称'}))

    class Meta:
        model = Classification
        fields = ['title','status']

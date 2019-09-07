# -*- coding: utf-8 -*-
__author__ = 'yf'
__date__ = '2019/7/9 16:39'

from django import forms
from .models import Users, News, Category, Review


class NewsAddModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入标题'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'cols': 100, 'rows': 21, 'placeholder': '请输入您要发布的内容'}),
            'category': forms.Select(attrs={'class': 'btn btn-default dropdown-toggle'}),
        }

    def __init__(self, *args, **kwargs):
        super(NewsAddModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = '标题'
        self.fields['content'].label = '内容'
        self.fields['category'].label = '类别'
        self.fields['attachment'].label = '封面图片'


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'cols': 80, 'rows': 3, 'placeholder': '请输入您要评论的内容'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewModelForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = '添加评论：'

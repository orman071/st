from django import forms
from django.contrib.auth.models import User
from .models import *

class AskForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):
    question = forms.IntegerField(widget=forms.HiddenInput())
    text = forms.CharField(widget=forms.Textarea)

    def clean_question(self):
        return Question.objects.get(pk=int(self.cleaned_data['question']))

    def save(self):
        ans = Answer(**self.cleaned_data)
        ans.save()
        return ans


class SignupForm(forms.Form):
    username = forms.CharField(label='Name')
    email = forms.EmailField(label='Mail')
    password = forms.CharField(widget=forms.PasswordInput())

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Name')
    password = forms.CharField(widget=forms.PasswordInput())

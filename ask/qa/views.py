from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *


def index(request):
    questions = Question.objects.last()
    page = paginate(request, questions)
    questions = page.object_list
    return render(request, 'qa/index.html', {'page': page ,'questions': questions})

def popular(request):
    questions = Question.objects.popular()
    page = paginate(request, questions)
    questions = page.object_list
    return render(request, 'qa/index.html', {'page': page ,'questions': questions})

def show(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(initial={'question': question.id})
    return render(request, 'qa/show.html', {'q': question, 'form': form})


def create_question(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            question = form.save()
            return redirect('show', question.id)
    else:
        form = AskForm()
    return render(request, 'qa/create_question.html', {'form': form})

@require_POST
def create_answer(request):
    form = AnswerForm(request.POST)
    form._user = request.user
    print(request.POST)
    if form.is_valid():
        ans = form.save()
        return redirect('show', ans.question.id)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                # Return a 'disabled account' error message
                return render(request, 'login.html',
                {'form': form, 'message': 'disabled account'})
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html',
            {'form': form, 'message': 'invalid login'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def test(request):
    return HttpResponse("That's Ok!")


#shortcut
def paginate(request, qs):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, 10)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page

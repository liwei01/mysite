#coding=utf=8

from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Article, Comment, Poll, NewUser
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.template import RequestContext
import markdown2, urlparse
#分页用
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(req):
    midware = Article.object.query_by_time()
    print midware
    midware_review=[1,2,3]
    limit = 20
    page_midware=Paginator(midware,limit)
    page_midware_review=Paginator(midware_review,limit)
    page=req.GET.get('page')
    table=req.GET.get('table','none')
    try:
        if table=='1':
            midware=page_midware.page(page)
        else:
            midware=page_midware.page(1)
    except PageNotAnInteger:
        midware=page_midware.page(1)
    except EmptyPage:
        midware=page_midware.page(page_midware.num_pages)
    try:
        if table=='2':
            midware_review=page_midware_review.page(page)
        else:
            midware_review=page_midware_review.page(1)
    except PageNotAnInteger:
        midware_review=page_midware_review.page(1)
    except EmptyPage:
        midware_review=page_midware_review.page(page_midware_review.num_pages)
    loginform = LoginForm()
    context = {'latest_article_list': midware, 'loginform':loginform}
    return render_to_response('index.html',context,context_instance=RequestContext(req))
    '''
    loginform = LoginForm()
    context = {'latest_article_list': latest_article_list, 'loginform':loginform}
    return render_to_response('index.html',context)
    '''
#分页面
# def test(request, list_id):
#     loginform = LoginForm()
#     Article_list = Article.object.query_by_time() # Get released blogs
#     paginator = Paginator(Article_list, 10)
#     try:
#         Article_list = paginator.page(list_id)
#     except PageNotAnInteger:
#         Article_list = paginator.page(1)
#     except EmptyPage:
#         Article_list = paginator.page(paginator.num_pages)
#     #print paginator.num_pages
#     return render_to_response('test.html', {'article_list': Article_list, 'loginform':loginform, 'paginator': paginator})

def test(request):
    contacts = Article.object.all()
    return render_to_response('test.html',{'object_list':contacts},context_instance=RequestContext(request))

#测试分页面2
def middleware_review(req):
    midware = Article.object.query_by_time()
    print midware
    midware_review=[1,2,3]
    limit = 100
    page_midware=Paginator(midware,limit)
    page_midware_review=Paginator(midware_review,limit)
    page=req.GET.get('page')
    table=req.GET.get('table','none')
    try:
        if table=='1':
            midware=page_midware.page(page)
        else:
            midware=page_midware.page(1)
    except PageNotAnInteger:
        midware=page_midware.page(1)
    except EmptyPage:
        midware=page_midware.page(page_midware.num_pages)
    try:
        if table=='2':
            midware_review=page_midware_review.page(page)
        else:
            midware_review=page_midware_review.page(1)
    except PageNotAnInteger:
        midware_review=page_midware_review.page(1)
    except EmptyPage:
        midware_review=page_midware_review.page(page_midware_review.num_pages)
    return render_to_response('middleware-review.html',{'midware':midware,'midware_review':midware_review},context_instance=RequestContext(req))



def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.POST.get('source_url','/focus')
                return redirect(url)
            else:
                return render(request,'login.html', {'form':form, 'error': "password or username is not ture!"})

        else:
            return render(request, 'login.html', {'form': form})

@login_required
def log_out(request):

    url = request.POST.get('source_url', '/focus/')
    logout(request)
    return redirect(url)


def article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    content = markdown2.markdown(article.content, extras=["code-friendly",
        "fenced-code-blocks", "header-ids", "toc", "metadata"])
    commentform = CommmentForm()
    loginform = LoginForm()
    comments = article.comment_set.all
    print comments
    return render(request, 'article_page.html', {
        'article': article,
        'loginform':loginform,
        'commentform':commentform,
        'content': content,
        'comments': comments
        })



@login_required
def comment(request, article_id):
    form  = CommmentForm(request.POST)
    url = urlparse.urljoin('/focus/', article_id)
    if form.is_valid():
        user = request.user
        article = Article.object.get(id=article_id)
        new_comment = form.cleaned_data['comment']
        c = Comment(content=new_comment, article_id=article_id)  # have tested by shell
        c.user = user
        c.save()
        article.comment_num += 1
    return redirect(url)

@login_required
def get_keep(request, article_id):
    logged_user = request.user
    article = Article.object.get(id=article_id)
    articles = logged_user.article_set.all()
    if article not in articles:
        article.user.add(logged_user)  # for m2m linking, have tested by shell
        article.keep_num += 1
        article.save()

        return redirect('/focus/')
    else:
        url = urlparse.urljoin('/focus/', article_id)
        return redirect(url)

@login_required
def get_poll_article(request,article_id):
    logged_user = request.user
    article = Article.object.get(id=article_id)
    #polls = logged_user.poll_set.all()
    polls = logged_user
    articles = []
    for poll in polls:
        articles.append(poll.article)

    if article in articles:
        url = urlparse.urljoin('/focus/', article_id)
        return redirect(url)
    else:
        article.poll_num += 1
        article.save()
        poll = Poll(user=logged_user, article=article)
        poll.save()
        data = {}
        return redirect('/focus/')


def register(request):
    error1 = "this name is already exist"
    valid = "this name is valid"

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username', 'erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':  # if ajax
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'register.html', {'form': form, 'msg': valid})
            else:
                return render(request, 'register.html', {'form': form, 'msg': error1})

        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request, 'register.html', {'form': form, 'msg': "two password is not equal"})
                else:
                    user = NewUser(username=username, email=email, password=password1)
                    user.save()
                    # return render(request, 'login.html', {'success': "you have successfully registered!"})
                    return redirect('/focus/login')
            else:
                return render(request, 'register.html', {'form': form})

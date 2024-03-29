from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from blog.models import Article, Category, Comment, User
from blog.forms.CommentForm import CommentForm

# Create your views here.

class ArticleIndexView(View):

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-created_on')
        context = {
            'articles': articles
        }
        return render(request, 'article_index.html', context)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['author', 'body']

    def form_valid(self, form):
        article = Article.objects.get(id=self.kwargs['pk'])
        Comment.objects.create(
            article=article,
            created_by=self.request.user,
            **form.cleaned_data
        )
        return redirect(reverse_lazy("article_detail", kwargs={"pk": self.kwargs['pk']}))


class ArticleDetailsView(View):

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs['pk'])
        comments = Comment.objects.filter(article=article)
        form = CommentForm()

        context = {
            'article': article,
            'comments': comments,
            'form': form
        }
        return render(request, 'article_detail.html', context)


class CategoryIndexView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'category_index.html', context)


class ArticleByCategoryIndexView(View):
    
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk=self.kwargs['category_pk'])
        articles = Article.objects.filter(category=category).order_by('-created_on')
        context = {
            'articles': articles,
            'category_name': category.name
        }
        return render(request, 'article_index.html', context)


class RegisterView(CreateView):
    template_name= 'register.html'
    form_class = UserCreationForm
    model = User

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(username=data['username'],
                                        password=data['password1'])
        return redirect('article_index')


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self):
        form = AuthenticationForm()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'],
                                password=data['password'])
            login(request, user)
            return redirect('article_index')
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('article_index')


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['body']
    pk_url_kwarg = 'pk_comment'
    template_name = 'comment_update.html'

    def form_valid(self, form):
        comment = Comment.objects.get(pk=self.kwargs['pk_comment'])
        comment.body = form.cleaned_data['body']
        comment.save()
        return redirect("my_comments")

class MyCommentsIndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(created_by=self.request.user).order_by('-created_on')
        context = {
            'comments': comments
        }
        return render(request, 'comment_index.html', context)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "comment_delete.html"
    model = Comment
    pk_url_kwarg = 'pk_comment'

    def get_success_url(self):
        return reverse_lazy("my_comments")
        
#coding=utf-8
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.contrib import admin
from django.utils import timezone

import datetime

#普通用户的数据模型
@python_2_unicode_compatible
class NewUser(User):
    profile = models.CharField('profile', default='',max_length=256,)

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'newuser'
        verbose_name_plural = '普通用户newuser'


#column字段是文章所属的分类，文章和分类是多对一的关系。我们构建一个Column数据模型
@python_2_unicode_compatible
class Column(models.Model):
    name = models.CharField( '分类名称', max_length=256,)
    intro = models.TextField('介绍', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'column'
        verbose_name_plural = '分类'
        ordering = ['name']

#Article模型的管理器，在models.py中加入以下代码(需写在class Article前面
class ArticleManager(models.Manager):
    def query_by_column(self, column_id):
        query = self.get_queryset().filter(column_id=column_id)

    def query_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        article_list = user.article_set.all()
        return article_list

    def query_by_polls(self):
        query = self.get_queryset().order_by('poll_num') #order_by查询结果排序
        return query

    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date') # 在 column name 前加一个负号，可以实现倒序
        return query

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query

#创建文章(article)这个数据模型
@python_2_unicode_compatible
class Article(models.Model):
    column = models.ForeignKey(Column, blank=True, null=True, verbose_name='belong to')
    title = models.CharField(max_length=256)
    author = models.ForeignKey('Author')
    user = models.ManyToManyField('NewUser')
    content = models.TextField('content')
    pub_date = models.DateTimeField('pub_date', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    published = models.BooleanField('notDraft', default=True)
    poll_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    keep_num = models.IntegerField(default=0)

    object = ArticleManager()
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = '文章(article)'

#评论的数据模型
@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey('NewUser', null=True)
    article = models.ForeignKey(Article, null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    poll_num = models.IntegerField(default=0)

    def __str__(self):
        return self.content
    class Meta:
        verbose_name = 'commen'
        verbose_name_plural = '评论'

#作者的数据模型
@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=256)
    profile = models.CharField('profile', default='',max_length=256)
    password = models.CharField('password', max_length=256)
    register_date = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = '作者'

#点赞的数据模型
#@python_2_unicode_compatible
class Poll(models.Model):
    user = models.ForeignKey('NewUser', null=True)
    article = models.ForeignKey(Article, null=True)
    comment = models.ForeignKey(Comment, null=True)

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = '点赞'

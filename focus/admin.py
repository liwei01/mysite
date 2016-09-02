#coding=utf-8
from django.contrib import admin
import xadmin
from .models import *

xadmin.site.register(NewUser)
xadmin.site.register(Column)
xadmin.site.register(Article)
xadmin.site.register(Comment)
xadmin.site.register(Author)
xadmin.site.register(Poll)
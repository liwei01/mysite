#coding=utf=8
import xadmin
import xadmin.views as xviews
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from .models import Post




xadmin.site.register(Post)




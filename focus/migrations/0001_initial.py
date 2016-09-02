# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-02 02:11
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('content', models.TextField(verbose_name=b'content')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'pub_date')),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('published', models.BooleanField(default=True, verbose_name=b'notDraft')),
                ('poll_num', models.IntegerField(default=0)),
                ('comment_num', models.IntegerField(default=0)),
                ('keep_num', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': '\u6587\u7ae0(article)',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('profile', models.CharField(default=b'', max_length=256, verbose_name=b'profile')),
                ('password', models.CharField(max_length=256, verbose_name=b'password')),
                ('register_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': '\u4f5c\u8005',
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb\xe5\x90\x8d\xe7\xa7\xb0')),
                ('intro', models.TextField(default=b'', verbose_name=b'\xe4\xbb\x8b\xe7\xbb\x8d')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'column',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('poll_num', models.IntegerField(default=0)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.Article')),
            ],
            options={
                'verbose_name': 'commen',
                'verbose_name_plural': '\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile', models.CharField(default=b'', max_length=256, verbose_name=b'profile')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.Article')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.Comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.NewUser')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.NewUser'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='focus.Author'),
        ),
        migrations.AddField(
            model_name='article',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.Column', verbose_name=b'belong to'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ManyToManyField(to='focus.NewUser'),
        ),
    ]
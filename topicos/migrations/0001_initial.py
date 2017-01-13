# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User
from topicos.models import Topico


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topico',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('id_usuario', models.ForeignKey(User)),
            ],
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('conteudo', models.CharField(max_length=256)),
                ('data', models.DateField(auto_now=False, auto_now_add=True)),
                ('id_topico', models.ForeignKey(Topico)),
                ('id_usuario', models.ForeignKey(User)),
            ],
        )
    ]

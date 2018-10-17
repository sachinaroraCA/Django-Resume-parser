# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import time
from math import ceil
from django.db.models import *
from django.contrib.auth.models import User

today = datetime.datetime.today()
now = datetime.datetime.now()

last_month = (today - datetime.timedelta(days=10)).strftime('%Y-%m-%d')



# Create your models here.

class ParseData(models.Model):
    added_on = models.DateTimeField(auto_now_add = True)
    name = models.CharField(max_length = 30,null = True, blank = True)
    email = models.CharField(max_length = 100,null = True,blank = True)
    mobile = models.CharField(max_length = 20, null = True, blank = True)
    date_of_birth = models.CharField(max_length = 20, null = True, blank = True)
    address = models.CharField(max_length = 20, null = True, blank = True)
    education = models.CharField(max_length = 20, null = True, blank = True)
    experience = models.CharField(max_length = 50, null = True, blank = True)
    parsed_resume = models.CharField(max_length = 100,null = True,blank = True)
    shinghles = models.CharField(max_length = 100, null = True,blank = True)

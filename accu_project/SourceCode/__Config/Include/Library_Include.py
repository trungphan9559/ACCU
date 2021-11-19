# import base64
# import ast
import os
# import sys
# import requests
import time
# import math
# import json  
# import copy
# import pdfkit
# import folium  
# import currency
import random
# import string
# import collections
# import workdays
# import jpholiday
# import mammoth

from _io import BytesIO
# from bs4 import BeautifulSoup
# from selenium import webdriver 
# from selenium.webdriver.chrome.options import Options

from django import forms
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse,JsonResponse,Http404,HttpResponseRedirect,HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView, DetailView, ListView, View
from django.utils.deprecation import MiddlewareMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission


from calendar import monthrange
from random import randrange
from celery import Celery
from xml.dom import minidom  
from pprint import pprint
from itertools import chain
from collections import defaultdict  
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from multiprocessing.pool import ThreadPool,threading
# from rest_framework.decorators import api_view

from pptx import Presentation
from pptx.dml.color import RGBColor
from django.utils import timezone
import pyotp
import re
import json
from urllib.request import urlopen
from urllib import parse

from django.contrib.auth.views import redirect_to_login
from django.conf import settings


from pptx import Presentation
import msoffcrypto
from zipfile import BadZipFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import io
from dateutil.relativedelta import relativedelta
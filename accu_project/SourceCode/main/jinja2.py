from jinja2 import Environment
from jinja2 import contextfunction
from django.urls import reverse
from django.templatetags.static import static
from django.utils.html import format_html
from datetime import datetime
from crispy_forms.utils import render_crispy_form

@contextfunction
def __crispy(context, form):
  crispy_form = render_crispy_form(form, context=context)
  crispy_form = crispy_form.replace('</form>','')
  crispy_form = format_html(crispy_form)
  return crispy_form

@contextfunction
def __crispy_file(context, form):
  crispy_form = render_crispy_form(form, context=context)
  return crispy_form

def pre_month(str_format=''):
  date_now = datetime.now()
  date_month = date_now.month
  date_year = date_now.year

  if date_month == 1:
    date_year = date_now.year - 1
    date_month = 12
  else:
    date_month = date_now.month-1

  str_date_year = str(date_year)
  str_date_month = '0{0}'.format(date_month) if date_month < 10 else str(date_month)

  return '{0}-{1}-01'.format(str_date_year, str_date_month)

def environment(**options):
  env = Environment(**options)
  env.globals.update({
      'static': static,
      'url': reverse,
      'crispy_file': __crispy_file,
      'crispy': __crispy,
  })

  env.filters['pre_month'] = pre_month
  env.filters['commafy'] = lambda v: "{:,}".format(v)
  return env
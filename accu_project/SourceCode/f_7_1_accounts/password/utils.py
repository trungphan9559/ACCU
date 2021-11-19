from __Config.Include.Common_Include import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from f_1_1_customers.models import Customer
from django.contrib.auth.models import User
# from f_7_1_accounts.models import AccountUserSession

def sent_token(emailTarget, token, email=None, username=None,):
  assert email is not None or username is not None, 'Email and Username are None'
  last_name = company_name = []
  if email is not None:
    users = User.objects.filter(email=email)
    customers = Customer.objects.filter(user__in=users)
    company_name = [customer.name for customer in customers]
    last_name = [user.last_name for user in users]
  elif username is not None:
    user = User.objects.get(username=username)
    customer = Customer.objects.filter(user=user)[0]
    company_name = [customer.name]
    last_name = [user.last_name]

  strToEncode = 'email='+email if email is not None else 'username='+username
  strEncode =  urlsafe_base64_encode(force_bytes(strToEncode))
  url = settings.CURRENT_URL+'/accounts/set-password/'+strEncode+'/'+token
  print('URL RESET PASSWORD : ---> ',url)
  domain = settings.CURRENT_URL
  domain = domain.replace('http://', '')
  domain = domain.replace('https://', '')  
  strLastName = ''.join(last_name) if len(last_name) == 1 else ','.join(last_name)
  strCompanyName = ''.join(company_name) if len(company_name) == 1 else ','.join(company_name)
  strCompanyName = until.remove_channel_name(strCompanyName)
  expiry_date = datetime.now() + timedelta(1)
  #str_expiry_date = expiry_date.strftime('%Y年%m月%d日%H時%M分')
  str_expiry_date = str(expiry_date.year)+'年'+str(expiry_date.month)+'月'+str(expiry_date.day)+'日'+str(expiry_date.hour)+'時'+str(expiry_date.minute)+'分'

  data = {
          'domain' : domain,
          'company_name' : strCompanyName,
          'last_name' : strLastName,
          'expiry_date': str_expiry_date,
          'url' : url,
      }
  body = render_to_string('email/password_forgot.html',data)
  send_mail(
      '[ACCU TOOL] パスワード再発行のご案内',
      '',
      settings.OSCAR_FROM_EMAIL ,
      [emailTarget],
      html_message = body,
  )

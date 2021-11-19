from __Config.Include.Common_Include import *
from f_7_1_accounts.models import AccountUserSession
from datetime import timedelta
import random
def __session_is_expired(user_id):
    if AccountUserSession.objects.filter(user_id=user_id).exists():
      user_session = AccountUserSession.objects.get(user_id=user_id)
    else:
      param_secret_key = pyotp.random_base32()
      user_session = AccountUserSession(user_id=user_id,secret_key=param_secret_key,is_verified=1)
      user_session.save()
      user_session = AccountUserSession.objects.get(user_id=user_id)

    expire_seconds = getattr(
          settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
        )
    logout_time = datetime.utcnow().replace(tzinfo=None) - user_session.last_updated.replace(tzinfo=None)
    session_is_expired = logout_time.total_seconds() > expire_seconds
    return session_is_expired

def __get_token_2fa(user_id):
  #1)Dữ liệu
  #1.1)Kiểm tra có phải superuser không
  user = User.objects.get(pk=user_id)
  if user.is_superuser:
    return 0

  #1.2)Lấy list session của user
  if AccountUserSession.objects.filter(user_id=user_id).exists():
    secret_key = pyotp.random_base32()
    user_session = AccountUserSession.objects.get(user_id=user_id)
    user_session.secret_key = secret_key
    user_session.save()
  else:
    secret_key = settings.DEFAULT_SCRET_KEY
    user_session = AccountUserSession(user_id=user_id,secret_key=secret_key)
    user_session.save()
  
  totp = pyotp.TOTP(secret_key, interval=300)
  totp.time = 0
  token = totp.now()

  #user_session.last_token = token
  user_session.is_verified = 0
  user_session.save()

  print('secret_key',secret_key,'sent_times','token : ',token, datetime.now())

  return token

def check_ms_group(user):
  if user.groups.filter(name='MS_User').exists():
    return True
  return False

def sent_token(request):
  if hasattr(request, 'user'):
    token = __get_token_2fa(request.user.id)
    today = datetime.now() + timedelta(minutes=5)
    strDate = str(today.year)+'年'+str(today.month)+'月'+str(today.day)+'日'+str(today.hour)+'時'+str(today.minute)+'分'
    if type(token) == str :
      data = {
          'user_name' : request.user.username,
          'token' : token,
          'date' : strDate,
          'url_confirm' : '',
      }
      body = render_to_string('email/verify_2fa.html',data)
      send_mail(
          '[ACCU TOOL] セキュリティコードのご連絡',
          '',
          settings.OSCAR_FROM_EMAIL ,
          [request.user.email],
          html_message = body,
      )
    return token
  else:
    return False

def check_token(user_id, token):
  if AccountUserSession.objects.filter(user_id=user_id).exists():
    user_session = AccountUserSession.objects.get(user_id=user_id)
  else:
    secret_key = settings.DEFAULT_SCRET_KEY
    user_session = AccountUserSession(user_id=user_id,secret_key=secret_key,is_verified=1)
    user_session.save()
    user_session = AccountUserSession.objects.get(user_id=user_id)

  #đoạn này check đã hết hạn hay chưa:
  print('Check token with {0}'.format(user_session.secret_key))
  is_valid_otp = pyotp.TOTP(user_session.secret_key, interval=300)

  if is_valid_otp.verify(token):
    user_session.is_verified = 1
    user_session.save()
    
    return True

  return False

def send_email_verify(email, username, company_name, last_name, uid, token):
  url_confirm = settings.CURRENT_URL+'/accounts/verify/'+uid+'/'+token
  print('URL CONFIRM : ---> ',url_confirm)

  expiry_date = datetime.now() + timedelta(7)
  #str_expiry_date = expiry_date.strftime('%Y年%m月%d日%H時%M分')
  str_expiry_date = str(expiry_date.year)+'年'+str(expiry_date.month)+'月'+str(expiry_date.day)+'日'+str(expiry_date.hour)+'時'+str(expiry_date.minute)+'分'
  company_name = until.remove_channel_name(company_name)
  data = {
      'company_name' : company_name,
      'last_name' : last_name,
      'username' : username,
      'url_confirm' : url_confirm,
      'expiry_date' : str_expiry_date,
  }
  body = render_to_string('email/activate_account.html',data)
  send_mail(
      'ID発行のお知らせ【リードプラス マイクロソフトメディア運営事務局】',
      '',
      settings.OSCAR_FROM_EMAIL ,
      [email],
      html_message = body,
  )

def send_email_remind_active_expried(email, username, company_name, last_name, uid, token, renew_expiry_date=''):
  url_confirm = settings.CURRENT_URL+'/accounts/verify/'+uid+'/'+token
  print('URL CONFIRM : ---> ',url_confirm)

  str_expiry_date = renew_expiry_date
  if str_expiry_date == '':
    expiry_date = datetime.now() + timedelta(7)
    #str_expiry_date = expiry_date.strftime('%Y年%m月%d日%H時%M分')
    str_expiry_date = str(expiry_date.year)+'年'+str(expiry_date.month)+'月'+str(expiry_date.day)+'日'+str(expiry_date.hour)+'時'+str(expiry_date.minute)+'分'
  
  company_name = until.remove_channel_name(company_name)
  data = {
      'company_name' : company_name,
      'last_name' : last_name,
      'username' : username,
      'url_confirm' : url_confirm,
      'expiry_date' : str_expiry_date,
  }
  body = render_to_string('email/remind_activate_account_expried_v2.html',data)
  send_mail(
      '重要：アカウント有効化のお願い【リードプラス マイクロソフトメディア運営事務局】',
      '',
      settings.OSCAR_FROM_EMAIL ,
      [email],
      html_message = body,
  )

def send_email_remind_active(email, username, company_name, last_name, uid, token, renew_expiry_date=''):
  url_confirm = settings.CURRENT_URL+'/accounts/verify/'+uid+'/'+token
  print('URL CONFIRM : ---> ',url_confirm)

  str_expiry_date = renew_expiry_date
  if str_expiry_date == '':
    expiry_date = datetime.now() + timedelta(7)
    #str_expiry_date = expiry_date.strftime('%Y年%m月%d日%H時%M分')
    str_expiry_date = str(expiry_date.year)+'年'+str(expiry_date.month)+'月'+str(expiry_date.day)+'日'+str(expiry_date.hour)+'時'+str(expiry_date.minute)+'分'
  
  company_name = until.remove_channel_name(company_name)
  data = {
      'company_name' : company_name,
      'last_name' : last_name,
      'username' : username,
      'url_confirm' : url_confirm,
      'expiry_date' : str_expiry_date,
  }
  body = render_to_string('email/remind_activate_account.html',data)
  send_mail(
      '重要：アカウント有効化のお願い【リードプラス マイクロソフトメディア運営事務局】',
      '',
      settings.OSCAR_FROM_EMAIL ,
      [email],
      html_message = body,
  )

def send_email_notify_added(email, username, company_name, last_name):
  company_name = until.remove_channel_name(company_name)
  data = {
      'company_name' : company_name,
      'last_name' : last_name,
      'username' : username,
      'url_login' : settings.CURRENT_URL,
  }
  body = render_to_string('email/notify_added.html',data)
  send_mail(
      'ID発行のお知らせ【リードプラス マイクロソフトメディア運営事務局】',
      '',
      settings.OSCAR_FROM_EMAIL ,
      [email],
      html_message = body,
  )

from __Config.Include.Common_Include import *
from f_7_1_accounts.models import AccountUserSession
from f_7_1_accounts.authentication import utils
from django.utils.deprecation import MiddlewareMixin


SESSION_TIMEOUT_KEY = "_session_init_timestamp_"
class SessionTimeoutMiddleware(MiddlewareMixin):
  def process_request(self, request):
    if not hasattr(request, "user") or not hasattr(request, "session") or request.session.is_empty():
      return

    init_time = request.session.setdefault(SESSION_TIMEOUT_KEY, time.time())

    expire_seconds = getattr(
      settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
    )

    session_is_expired = time.time() - init_time > expire_seconds
    user_id = request.user.id
    is_ms_group = utils.check_ms_group(request.user)
    if session_is_expired and not request.user.is_superuser and not is_ms_group and user_id is not None:
      if AccountUserSession.objects.filter(user_id=user_id).exists():
        user_session = AccountUserSession.objects.get(user_id=user_id)
        user_session.is_verified = 0
        user_session.save()
      else:
        param_secret_key = pyotp.random_base32()
        user_session = AccountUserSession(user_id=user_id,secret_key=param_secret_key,is_verified=1)
        user_session.save()

class LoginCodeMiddleware(MiddlewareMixin):
  def process_request(self, request):
    if not hasattr(request, "user"):
      return None
    user_id = request.user.id
    list_black_list = [reverse_lazy('logout'), reverse_lazy('authentication')]

    if user_id != None and request.path not in list_black_list and request.user.is_superuser != 1 and "accounts/resend-code" not in str(request.path):

      if AccountUserSession.objects.filter(user_id=user_id).exists():
        user_session = AccountUserSession.objects.get(user_id=user_id)
      else:
        param_secret_key = pyotp.random_base32()
        user_session = AccountUserSession(user_id=user_id,secret_key=param_secret_key,is_verified=1)
        user_session.save()
        user_session = AccountUserSession.objects.get(user_id=user_id)

      if user_session.is_verified == 0 and user_session.sent_times < 100:
        return redirect('authentication')

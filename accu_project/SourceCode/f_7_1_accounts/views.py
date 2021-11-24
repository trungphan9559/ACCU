from __Config.Include.Common_Include import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm, SetPasswordForm
from f_7_1_accounts.authentication import utils as auth_utils
from f_7_1_accounts.forms import LoginCodeForm, PasswordForgotForm
from .forms import CustomUserCreationForm, SignUpForm, CustomPasswordChangeForm,ChangePasswordForm
from .tokens import account_activation_token, account_reset_password_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from f_7_1_accounts.models import AccountUserSession
from f_1_1_customers.models import Customer, CustomerGroup, CustomerContract, CustomerGroupPlanOption
from f_1_1_customers.user_permissions import user_permissions
from django.contrib.auth.models import User
import copy 
from f_1_2_sites.models import Site
from f_7_1_accounts.until import draw_excel


class AuthenticationPageView(LoginRequiredMixin, FormView):
  template_name ='apps/f_7_1_accounts/authentication.html'
  form_class = LoginCodeForm
  success_url = reverse_lazy('select_customer')
  # reverse_lazy('home')
  
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs.update({'user': self.request.user})
    return kwargs

class CustomAuthenticationForm(AuthenticationForm):
  username = UsernameField(
    label='Email',
    widget=forms.TextInput(attrs={'autofocus': True})
  )

class LoginView(FormView):
  form_class = CustomAuthenticationForm
  template_name = 'registration/login.html'
  success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

  def form_valid(self, form):
    #1)Login
    user = form.get_user()
    login(self.request, user)
    if not user.is_superuser:
      # Kiểm tra userSession có phải đang login bằng Admin hay không 
      user_session = AccountUserSession.objects.get(user=user)
      if user_session.sent_times >= 100:
        user_session.sent_times = user_session.sent_times % 100
        user_session.save()
    thread = threading.Thread(target=auth_utils.sent_token,args=(self.request,))
    thread.start()

    return super().form_valid(form)
  
  def get_success_url(self):
    if self.request.user.is_superuser:  
      self.request.session['current_revision'] = settings.CURRENT_REVISION
      self.request.session['database_name'] = settings.DB_NAME
      self.request.session['type_environment'] = settings.CONFIG_ENV_TYPE
      return reverse_lazy('home')
    else:

      return super().get_success_url()

class UserListView(PermissionRequiredMixin,ListView):
  model = User
  permission_required = ['user.view_user']
  template_name = 'apps/f_7_1_accounts/user_list.html'
  context_object_name = 'list_users'
  ordering = ['email']

  def get_queryset(self):
    #1)Dữ liệu
    qs = super().get_queryset()
    list_data_queryset = []

    #1.2)Dữ liệu từ request
    if self.request.GET:
      group_id = int(self.request.GET.get('group', -1))
      customer_id = int(self.request.GET.get('customer', -1))
      status = int(self.request.GET.get('status', 2)) # 1 : active, 0 : waiting, -1 : locked, 2 : all
      site_id = int(self.request.GET.get('site',-1))
      print('****************')
      print('group_id : ',group_id,'customer_id : ',customer_id,'status : ',status,'search : ')
      print('****************')

      if group_id != -1:
        if customer_id == -1:
          if site_id == -1:
            list_customers = Customer.objects.filter(customer_group = group_id)
          else:
            list_customers = Customer.objects.filter(customer_group = group_id, site=site_id)
        else:
          if site_id == -1:
            list_customers = Customer.objects.filter(pk=customer_id)
          else:
            list_customers = Customer.objects.filter(pk=customer_id, site=site_id)
          
      else:
        if customer_id == -1:
          if site_id == -1:
            list_customers = Customer.objects.all()
          else:
            list_customers = Customer.objects.filter(site=site_id)
        else:
          if site_id == -1:
            list_customers = Customer.objects.filter(pk=customer_id)
          else:
            list_customers = Customer.objects.filter(pk=customer_id, site=site_id)

      #gom data
      print(list_customers)
      for customer in list_customers:
        if status == 1:
          list_user = [i for i in customer.user.all() if i.is_active == True ]

        elif status == 0:
          list_user = [i for i in customer.user.all() if  i.is_active == False and i.last_login == None ]
        
        elif status == -1:
          list_user = [i for i in customer.user.all() if i.is_active == False and i.last_login is not None ]
        else:
          list_user = [i for i in customer.user.all() ]
        
        for i in list_user:
          setattr(i, 'customer_name', customer.name)
          setattr(i, 'customer_code', customer.code)
          list_data_queryset.append(i)

      print("trungg")
      return list_data_queryset

    else:
      customer_id = int(self.request.GET.get('customer', -1))
      for user in qs:
        customer = Customer.objects.filter(user=user)
        if len(customer) > 0:
          setattr(user, 'customer_name', customer[0].name)
          setattr(user, 'customer_code', customer[0].code)
        else:
          setattr(user, 'customer_name', 'None')
          setattr(user, 'customer_code', 'None')
      return qs
  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()
    customer_group_id = self.request.GET.get('group',-1)
    site_id = int(self.request.GET.get('site',-1))
    customer_id = int(self.request.GET.get('customer', -1))

    #2)Xử lý
    list_groups = CustomerGroup.objects.all()
    # try:
    #   customer_group = CustomerGroup.objects.get(pk=customer_group_id)
    #   list_customers = Customer.objects.filter(customer_group=customer_group)
    # except CustomerGroup.DoesNotExist:
    #   list_customers = []
    #   pass
    list_sites = []

    if site_id == -1:
      list_sites = Site.objects.all()
      list_customers = Customer.objects.filter(customer_group=customer_group_id)
    else:
      list_customers = Customer.objects.filter(customer_group=customer_group_id , site = site_id)

    if customer_id == -1:
      list_sites = Site.objects.all()
    else:
      try:
        list_sites = Customer.objects.get(pk=customer_id).site.all()
      except Customer.DoesNotExist:
        list_sites = []
    
    #filter theo group
    if str(customer_group_id) != '-1':
      customer_group = CustomerGroup.objects.get(pk=customer_group_id)
      list_site_group = customer_group.site.all()
      
      #khi group được chọn thì chỉ filter các site thuộc group đó thôi
      list_sites = list(filter(lambda site: site in list_site_group, list_sites))

      
    #3)Trả về
    data['list_groups'] = list_groups
    data['list_customers'] = list_customers
    data['list_sites'] = list_sites
    return data

class SignUpView(SuccessMessageMixin, FormView):
  form_class = SignUpForm
  template_name = 'apps/f_7_1_accounts/signup.html'
  success_message = 'Create %(email)s success'

  def get_success_url(self):
    return reverse_lazy('signup',kwargs={'group_id':self.kwargs['group_id'],'customer_id':self.kwargs['customer_id']})

  # def get_success_message(self, cleaned_data):
  #   try:
  #     user = User.objects.get(username=cleaned_data["email"], email=cleaned_data["email"])
  #     customer = Customer.objects.get(id=cleaned_data['customer'])
  #     if user and customer.user.filter(id=user.id):
  #       return 'Email {email} is readly exist in customer {customer}'.format(email=user.email, customer= customer.name)
  #   except User.DoesNotExist:
  #     pass

  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    group_id = self.kwargs.get('group_id')
    customer_id = self.kwargs.get('customer_id')

    group_obj = CustomerGroup.objects.get(id=group_id)
    customer_obj = Customer.objects.get(id=customer_id)
    form.fields['group'].choices = ([(group_obj.id,group_obj.name),])
    form.fields['group'].initial = group_id
    form.fields['group'].disabled = True
    form.fields['customer'].choices = ([(customer_obj.id,customer_obj.name),])
    form.fields['customer'].initial = customer_id
    form.fields['customer'].disabled = True
    
    list_email_domain = []
    if hasattr(customer_obj, "email_domain"):
      try:
        list_email_domain = json.loads(customer_obj.email_domain)
      except ValueError as err:
        list_email_domain = []
    print('list_email_domain : ',list_email_domain)
    form.fields['domain'].widget = forms.HiddenInput()
    form.fields['domain'].initial  = list_email_domain
    return form

  def form_valid(self, form):
    #1)Dữ liệu
    group_id = form.fields['group'].initial
    customer_id = form.fields['customer'].initial
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    email = form.cleaned_data['email']

    #2)Xử lý
    #2.1)Lưu user
    print('Form Valid : group_id : ',group_id,'customer_id :  ',customer_id, 'first_name : ',first_name,'last_name : ',last_name)
    username = email
    password = 'Lp123456'

    is_exist = False
    #Kiểm tra đã có bảng ghi của user chưa
    try:
      user = User.objects.get(username=username, email=email)
      print("trunggggg")

      is_exist = True
    except User.DoesNotExist:
      print(username , email, "errorrrrrrrrrrrrrrr",User.objects.filter(username=username, email=email) )
      user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
      user.is_active = 0
      user.save()

    #Tạo bảng ghi session
    account_user_session = AccountUserSession.objects.filter(user_id=user.id)
    if not account_user_session:
      user_session = AccountUserSession(user_id=user.id,secret_key="",is_verified=1,  last_verify_token="").save()

    user_id = user.id
    
    
    #2.2)Thêm user vào trong customer
    customer = Customer.objects.get(id=customer_id)
    customer.user.add(user)

    #2.3)Thêm quyền cho user
    user_permissions.add_user_to_customer(customer_id,user_id)
    
    #2.4)Gửi email xác nhận
    if is_exist:
      #2.4.1)Gởi mail thông báo đã được add vào  customer này
      # auth_utils.send_email_notify_added(email, username, customer.name, last_name)
      pass
    else:
      user = User.objects.get(username=username)
      token = account_activation_token.make_token(user)
      auth_utils.send_email_verify(email, username, customer.name, last_name, urlsafe_base64_encode(force_bytes(user.pk)), token)

      #Lưu token vừa gởi vào lại db
      account_user_session = AccountUserSession.objects.get(user_id=user.id)
      account_user_session.last_verify_token = token
      account_user_session.save()

      

    return super().form_valid(form)

class UserChangePassWord(SuccessMessageMixin,FormView): 

  form_class = ChangePasswordForm
  template_name = 'apps/f_7_1_accounts/user_password_update.html'
  success_message = 'パスワード変更が完了しました。'

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs.update({'user': self.request.user})
    return kwargs

  def get_success_url(self):
    return reverse("update_password", args=(self.kwargs['pk'],))  
  
  def form_valid(self, form):
    password = form.cleaned_data["new_password1"]
    user = User.objects.get(id = self.request.user.id)

    user.set_password(password)
    user.save()

    login(self.request, user)

    return super().form_valid(form)

def verify(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None
  if user is not None and account_activation_token.check_token(user, token):
    if request.method == 'POST':
      form = CustomPasswordChangeForm(user, request.POST)
      if form.is_valid():
        user.is_active = True
        user.save()
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        param_secret_key = pyotp.random_base32()

        account_user_session = AccountUserSession.objects.filter(user_id=user.id)
        if not account_user_session:
          print("tạo cái mơiiiiiiiiiiiiiiii")
          user_session = AccountUserSession(user_id=user.id,secret_key=param_secret_key,is_verified=0, last_verify_token="")
          user_session.save()
        else:
          print(" Update cai cu tạo cái mơiiiiiiiiiiiiiiii")

          account_user_session[0].secret_key = param_secret_key
          account_user_session[0].is_verified = 0
          account_user_session[0].save()
        
        # login(request, user)
        messages.success(request, 'パスワード設定が完了しました。')
        return redirect('login')
      else:
        messages.error(request, "The two password fields didn't match.")
    else:
      form = CustomPasswordChangeForm(user)
    return render(request, 'apps/f_7_1_accounts/set_password.html', {'form': form,'email': user.email})
  else:
    return HttpResponse('Invalid token')

class UserDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
  model = User
  permission_required = ['auth.delete_user']
  template_name = 'apps/f_7_1_accounts/user_delete.html'
  success_url = reverse_lazy('user_list')
  success_message = 'Delete User successed'
  context_object_name = 'data_user'

  def delete(self, request, *args, **kwargs):
    messages.success(self.request, self.success_message)
    return super().delete(request, *args, **kwargs)

class UserUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView): 
  model = User
  permission_required = ['f_7_1_accounts.change_user']
  template_name = 'apps/f_7_1_accounts/user_update.html'
  fields = ['email', 'last_name', 'first_name', 'is_active']
  success_message = 'Update %(first_name)s %(last_name)s successed'
  context_object_name = 'data_user'

  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    form.fields['email'].disabled = True
    form.fields['last_name'].required = True
    return form

  def get_success_url(self):
    return reverse("user_update", args=(self.kwargs['pk'],))  

class CustomerUserView(PermissionRequiredMixin,ListView):
  model = Customer
  permission_required = ['auth.view_user']
  template_name = 'apps/f_7_1_accounts/user/customer_user.html'
  context_object_name = 'customer_user'

  def get_queryset(self):
    return Customer.objects.filter(user = self.request.user.id)
  
  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()

    customer_plan = None
    sort_plan = None
    list_options = []
  
    customer_obj = Customer.objects.filter(id=self.request.session['customer_id'])[0]

    # customer_contract = CustomerContract.objects.filter(customer_id = customer_obj, is_active = True )
    customer_contract = CustomerContract.objects.filter(customer_id = customer_obj, start_date__lte = datetime.now().date(), end_date__gte = datetime.now().date())
    if customer_contract:
      customer_contract = customer_contract[0]

      #2)Xử lý
      try:
        customer_plan = customer_contract.plan
      except CustomerGroup.DoesNotExist:
        customer_plan = None

      try:
        list_options = customer_contract.option.all()
      except CustomerGroup.DoesNotExist:
        list_options = []
    
      #3)Trả về
      obj_customer_plan_option_auth = CustomerGroupPlanOption.objects.filter(auth_group=customer_plan)
      try:
        sort_plan = CustomerGroupPlanOption.objects.get(auth_group=customer_plan).sort
      except Exception as inst:
        sort_plan = None


    data['plan'] = customer_plan
    data['sort_plan'] = sort_plan
    data['list_options'] = list_options
    data['customer_data'] = customer_obj
    data['customer_contract'] = customer_contract

    return data

class AdminUserView(PermissionRequiredMixin,ListView):
  model = Customer
  permission_required = ['auth.view_user']
  template_name = 'apps/f_7_1_accounts/admin/admin_user.html'
  context_object_name = 'admin_user'

  def get_queryset(self):
    #1) biến lấy từ frontend    
    qs = super().get_queryset()

    param_group_id = self.request.GET.get('group',-1)
    param_site_id = self.request.GET.get('site',-1)

    list_customers = Customer.objects.all()

    #2.2) Filter theo customer
    if str(param_group_id) != "-1":
      qs = qs.filter(customer_group=param_group_id)

    #2.2) Filter theo site
    if str(param_site_id) != "-1":
      qs = qs.filter(site = param_site_id)

    
    return qs
  
  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()

    param_group_id = int(self.request.GET.get('group',-1)) 
    param_site_id = int(self.request.GET.get('site',-1))

    #2)Xử lý
    list_customer_groups = CustomerGroup.objects.all()
    list_sites = []

    data['customer_id'] = param_group_id
    data['site_id'] = param_site_id

    data['list_customer_groups'] = list_customer_groups

    if str(param_group_id) != '-1':
      customer_group = CustomerGroup.objects.get(pk=param_group_id)
      list_sites = customer_group.site.all()
    
    data["list_sites"] = list_sites

    return data

class UserDeleteBulkView(SuccessMessageMixin, PermissionRequiredMixin, View): 
  permission_required = ['auth.delete_user']

  def post(self, request):
    #1)Dữ liệu
    list_id = self.request.POST['list_id'].split(',')
    
    #2)Xử lý
    if list_id[0] != '':
      User.objects.filter(pk__in=list_id).delete()

    return HttpResponse(1)

@csrf_exempt
def loginUser(request, user_id):
  print('loginUser user_id: ',user_id)
  user = User.objects.get(pk=user_id)
  # Kiểm tra last_login của user
  isResetLastLogin = False
  if user.last_login == None:
    isResetLastLogin = True
  # Kiểm tra userSession đã tồn tại hay chưa
  if not AccountUserSession.objects.filter(user_id=user_id).exists():
    param_secret_key = pyotp.random_base32()
    user_session = AccountUserSession(user_id=user_id,secret_key=param_secret_key,is_verified=1)
    user_session.save()
  # + userSession thêm 100 để cheat qua middleware
  user_session = AccountUserSession.objects.get(user_id=user_id)
  print('user_session : ',user_session,'sent_times',user_session.sent_times)
  user_session.sent_times = 100 + (user_session.sent_times % 100)
  user_session.save()
  login(request, user)
  if isResetLastLogin:
    user.last_login = None
    user.save()
  
  print("trunggggggggggggggggggggg")
  return redirect(reverse_lazy("select_customer"))
  

def download_data_user(request):
  qs = User.objects.all()
  if request.GET:
    group_id = int(request.GET.get('group', -1))
    customer_id = int(request.GET.get('customer', -1))
    status = int(request.GET.get('status', 2)) # 1 : active, 0 : waiting, -1 : locked, 2 : all
    if group_id != -1:
      if customer_id == -1:
        qs_tmp1 = []
        list_customers = Customer.objects.filter(customer_group=group_id)
        for customer in list_customers:
          list_pk = [user.pk for user in customer.user.all()]
          if len(list_pk) > 0:
            qs_tmp2 = qs.filter(pk__in=list_pk)
            for i in qs_tmp2:
              setattr(i, 'customer_name', customer.name)
            qs_tmp1.extend(qs_tmp2)
        qs = qs_tmp1 if len(qs_tmp1) > 0 else qs
      else:
        customer = Customer.objects.get(pk=customer_id)
        qs = customer.user.all()
        for i in qs:
          setattr(i, 'customer_name', customer.name)
    else:
      for user in qs:
        customer = Customer.objects.filter(user=user)
        if len(customer) > 0:
          setattr(user, 'customer_name', customer[0].name)
        else:
          setattr(user, 'customer_name', 'None')

    if status == 1:
      qs = [i for i in qs if i.is_active == True and i.last_login is not None]
    elif status == 0:
      qs = [i for i in qs if i.is_active == False and i.last_login == None]
    elif status == -1:
      qs = [i for i in qs if i.is_active == False and i.last_login is not None]
    
  else:
    for user in qs:
      customer = Customer.objects.filter(user=user)
      if len(customer) > 0:
        setattr(user, 'customer_name', customer[0].name)
      else:
        setattr(user, 'customer_name', 'None')
    
  #Tạo file excel
  reponse = draw_excel.draw_list_user(qs)
  
  return reponse

class PasswordChangeView(LoginRequiredMixin, FormView):
  template_name = 'registration/password_change_form.html'
  form_class = PasswordChangeForm
  success_message = 'パスワード変更が完了しました。'
  success_url = reverse_lazy('change_password')


  def get_form_kwargs(self):
    kwargs = super(PasswordChangeView, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def form_valid(self, form):
    form.save()
    messages.success(self.request, "パスワード変更が完了しました。")
    return super(FormView, self).form_valid(form)

def reSendCode(request):
  return HttpResponse(auth_utils.sent_token(request))

def verifyError(request):
  return render(request,('apps/f_7_1_accounts/verify_error.html'))

def resetError(request):
  return render(request,('apps/f_7_1_accounts/reset_error.html'))

class VerifyV2(FormView):
  template_name = 'apps/f_7_1_accounts/set_password.html'
  form_class = SetPasswordForm
  success_message = 'パスワード設定が完了しました。'

  def __init__(self): 
    user_id = None

  def get_success_url(self):
    return reverse_lazy('set_password_done',kwargs={'user_id':self.user_id})

  def get_form_kwargs(self):
    uidb64 = self.kwargs.get('uidb64')
    token = self.kwargs.get('token')
    user = None
    try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):

      # return super(VerifyV2,).dispatch(request, *args, **kwargs)
      raise Exception("User invalid")
    assert account_activation_token.check_token(user, token), 'Token invalid'
    # if not account_activation_token.check_token(user, token):
    #   return super(VerifyV2,).dispatch(request, *args, **kwargs)

    kwargs = super(VerifyV2, self).get_form_kwargs()
    kwargs['user'] = user
    return kwargs

  def dispatch(self, request, *args, **kwargs):
    uidb64 = self.kwargs.get('uidb64')
    token = self.kwargs.get('token')

    try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      return redirect('verifyError')

    if not account_activation_token.check_token(user, token):
      return redirect('verifyError')
    
    return super(VerifyV2, self).dispatch(request, *args, **kwargs)




  def get_context_data(self, **kwargs):
    data = super().get_context_data(**kwargs)
    uidb64 = self.kwargs.get('uidb64')
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    data['username'] = user.username
    return data

  def form_valid(self, form):
    user = form.save()
    user.is_active = True
    user.save()
    update_session_auth_hash(self.request, user)  # Important!
    param_secret_key = pyotp.random_base32()
    account_user_session = AccountUserSession.objects.filter(user_id=user.id)
    if not account_user_session:
      user_session = AccountUserSession(user_id=user.id,secret_key=param_secret_key,is_verified=0, last_verify_token="")
      user_session.save()
    else:
      account_user_session[0].secret_key = param_secret_key
      account_user_session[0].is_verified = 0
      account_user_session[0].save()

    # login(request, user)
    self.user_id = user.id
    return super(FormView, self).form_valid(form)

def verifyDone(request, user_id):
  if User.objects.filter(pk=user_id).exists():
    user = User.objects.get(pk=user_id)

    customer = Customer.objects.filter(user=user)
    company_name = ""
    if customer:
      customer = customer[0]
      company_name = customer.name

    company_name = until.remove_channel_name(company_name)
    data = {
        'company_name' : company_name,
        'last_name' : user.last_name,
        'user_name' : user.username,
        'email': user.email,
        'url_login' : settings.CURRENT_URL,
    }

    body = render_to_string('email/verify_success.html',data)
    email = EmailMultiAlternatives(
        "アカウント登録完了のご連絡【リードプラス マイクロソフトメディア運営事務局】",
        'htmlBody',
        settings.OSCAR_FROM_EMAIL ,
        [user.email],

    )
    email.attach_alternative(body, "text/html")
    email.send()

  data_done_email ={
        'user_name' : user.username,
        'email': user.email,
  }
  return render(request,('apps/f_7_1_accounts/user_set_password_done.html'),data_done_email)
class UserPasswordForgot(FormView):
  template_name = 'apps/f_7_1_accounts/user_password_reset.html'
  form_class = PasswordForgotForm
  success_message = 'Thanh cong'
  success_url = 'done'

def passwordResetDone(request):
  return render(request,('apps/f_7_1_accounts/user_password_reset_done.html'))

class UserSetPassword(FormView):
  template_name = 'apps/f_7_1_accounts/reset_password.html'
  form_class = SetPasswordForm
  success_message = 'パスワード設定が完了しました。'
  success_url = reverse_lazy('reset_password_done')

  def _processUidb64(self, uidb64):
    strDecode = force_text(urlsafe_base64_decode(uidb64))
    listSplit = strDecode.split('=')
    # assert len(listSplit) == 2, 'Invalid uidb64'
    if not len(listSplit) == 2:
      return super(FormView,).dispatch(request, *args, **kwargs)
    return {listSplit[0]: listSplit[1]}

  def dispatch(self, request, *args, **kwargs):
    uidb64 = self.kwargs.get('uidb64')
    token = self.kwargs.get('token')
    param = self._processUidb64(self.kwargs.get('uidb64'))
    user = None

    if 'email' in param:
      users = User.objects.filter(email=param['email'])
      assert len(users) > 0
      user = users[0]
    elif 'username' in param:
      user = User.objects.get(username=param['username'])

    if not account_reset_password_token.check_token(user, token):
      return redirect('resetError')

    return super(UserSetPassword, self).dispatch(request, *args, **kwargs)

  def get_form_kwargs(self):
    uidb64 = self.kwargs.get('uidb64')
    token = self.kwargs.get('token')
    param = self._processUidb64(self.kwargs.get('uidb64'))
    user = None
    if 'email' in param:
      users = User.objects.filter(email=param['email'])
      assert len(users) > 0
      user = users[0]
    elif 'username' in param:
      user = User.objects.get(username=param['username'])
    assert account_reset_password_token.check_token(user, token), 'Token invalid'    
    kwargs = super(UserSetPassword, self).get_form_kwargs()
    kwargs['user'] = user
    return kwargs

  def get_context_data(self, **kwargs):
    data = super().get_context_data(**kwargs)
    param = self._processUidb64(self.kwargs.get('uidb64'))
    data.update(param)
    return data

  def form_valid(self, form):
    user = form.save()
    password = form.cleaned_data["new_password1"]
    param = self._processUidb64(self.kwargs.get('uidb64'))
    if 'email' in param:
      listUsers = User.objects.filter(email=param['email'])
      for user in listUsers:
        if user.is_active == 1:
          user.set_password(password)
          user.save()
    return super(FormView, self).form_valid(form)

def setPassworDone(request):
  return render(request,('apps/f_7_1_accounts/user_reset_password_done.html'))


# class UserRemindBulkView(SuccessMessageMixin, PermissionRequiredMixin, View): 
class UserRemindBulkView(SuccessMessageMixin, View): 
  # permission_required = ['auth.delete_user']

  def post(self, request):
    #1)Dữ liệu
    list_id = self.request.POST['list_id'].split(',')

    #2)Xử lý
    if list_id[0] != '':
      for user_id in list_id:
        #Lấy token cũ của nó ra
        account_user_session = AccountUserSession.objects.get(user_id=user_id)

        user = User.objects.get(id = user_id)

        # if not account_activation_token.check_token(user, account_user_session.last_verify_token):
        #   #Tạo token mới
        #   token = account_activation_token.make_token(user)

        #   #Update lại giá trị
        #   account_user_session.last_verify_token = token
        #   account_user_session.save()
        # else:
        #   #Vẫn dùng token cũ nè
        #   token = account_user_session.last_verify_token

        #Tạo token mới
        token = account_activation_token.make_token(user)

        #Update lại giá trị
        account_user_session.last_verify_token = token
        account_user_session.save()

        
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        #bắt đầu gởi lại email remind
        #Lấy customer đầu tiên mà user đó đc add vào vì nếu đã verify thì không cần remind nữa
        customer = Customer.objects.get(user = user)

        auth_utils.send_email_remind_active(user.email, user.username, customer.name, user.last_name, urlsafe_base64_encode(force_bytes(user.pk)), token)


    return HttpResponse(1)
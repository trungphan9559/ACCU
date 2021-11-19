from django import forms
from f_7_1_accounts.authentication import utils as auth_utils
from f_7_1_accounts.password import utils as password_utils
from django.contrib.auth import get_user_model
from django.contrib.auth.forms  import UserCreationForm, UserChangeForm
from f_1_1_customers.models import Customer, CustomerGroup
from django.contrib.auth.models import User
from django.contrib import messages
from .tokens import account_reset_password_token

class LoginCodeForm(forms.Form):
  code = forms.CharField(max_length=6, label="セキュリティコード")
  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user',None)
    super().__init__(*args, **kwargs)

  def clean_code(self):
    is_valid = auth_utils.check_token(self.user.id, self.cleaned_data['code'])
    if not is_valid:
      raise forms.ValidationError("セキュリティコードが正しくありません。ご確認の上、再度入力してください。")

class CustomUserCreationForm(UserCreationForm):
  class  Meta:
    model = get_user_model()
    fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = get_user_model()
    fields = ('email','username',)

class SignUpForm(forms.Form):
  class Meta:
    model = get_user_model()
    fields = ('group', 'customer', 'email', 'last_name', 'first_name', 'domain',)
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=False, label="メールアドバイス")
  group = forms.ChoiceField(required=False, label="グループ")
  customer = forms.ChoiceField(required=False, label="顧客名")
  last_name = forms.CharField(max_length=60, label="姓")
  first_name = forms.CharField(required=False,max_length=50, label="名", initial='')
  domain = forms.CharField(max_length=2550, label="ドメイン")

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
  # def clean_email(self):
  #   email = self.cleaned_data.get('email')
  #   if len(User.objects.filter(email=email)) > 0:
  #     raise forms.ValidationError("Email is exist")
  #   return email
  
class CustomPasswordChangeForm(forms.Form):
  new_password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput, required=True)
  new_password2 = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput, required=True)

  field_order = ['new_password1', 'new_password2']

  def __init__(self, user, *args, **kwargs):
    self.user = user
    super().__init__(*args, **kwargs)

  def clean_new_password2(self):
    if self.is_valid():
      password1 = self.cleaned_data.get('new_password1')
      password2 = self.cleaned_data.get('new_password2')
      if password1 != password2:
        raise forms.ValidationError("The two password fields didn't match")

      return password2

  def save(self, commit=True):
    password = self.cleaned_data["new_password1"]
    self.user.set_password(password)
    if commit:
      self.user.save()
    return self.user

class ChangePasswordForm(forms.Form):

  current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput, required=True)
  new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=True)
  new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=True)

  field_order = ['current_password', 'new_password1', 'new_password2']

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user',None)
    super().__init__( *args, **kwargs)

  def clean_current_password(self):
    if self.is_valid():
      current_password = self.cleaned_data.get('current_password')
      valid_current_password = self.user.check_password(current_password)
      if not valid_current_password:
        raise forms.ValidationError("Current password is incorrect!")

      return current_password

  def clean_new_password2(self):
    if self.is_valid():
      password1 = self.cleaned_data.get('new_password1')
      password2 = self.cleaned_data.get('new_password2')
      if password1 != password2:
        raise forms.ValidationError("The two password fields didn't match!")
      return password2
  
  

  def save(self, commit=True):
    password = self.cleaned_data["new_password1"]
    self.user.set_password(password)
    if commit:
      self.user.save()
    return self.user

class PasswordForgotForm(forms.Form):
  inputfield = forms.CharField(max_length=50, label="メールアドレス")
  def clean_inputfield(self):
    inputfield = self.cleaned_data['inputfield']
    '''
    if '@' in inputfield:
      users = User.objects.filter(email=inputfield)
      assert len(users) > 0
      user = users[0]
      if len(users) == 1:
        if user.is_active == 0:
          if user.last_login is None:
            raise forms.ValidationError("User is activating. Please confirm first")
          else:
            raise forms.ValidationError("User is locked. Can't reset password")
      token = account_reset_password_token.make_token(user)
      # Send email with email
      password_utils.sent_token(inputfield, token, email=inputfield)
    else:
    '''
    if User.objects.filter(username=inputfield).exists():
      user = User.objects.get(username=inputfield)
      if user.is_active == 0:
        if user.last_login is None:
          raise forms.ValidationError("ユーザーがまだアクティベーションされていません。")
        else:
          raise forms.ValidationError("ユーザーがロックされています。")
      else:
        # Send email with username
        token = account_reset_password_token.make_token(user)
        password_utils.sent_token(user.email, token, username=inputfield)
    else:
      raise forms.ValidationError("メールアドレスが見つかりませんでした。")

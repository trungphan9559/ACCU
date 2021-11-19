# accounts/urls.py
from django.conf.urls import url, include
from f_7_1_accounts import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
   url(r'^verifyError$', views.verifyError, name='verifyError'),
   url(r'^resetError$', views.resetError, name='resetError'),
   url(r'^login/$', views.LoginView.as_view(), name='login'),
   url(r'^authentication/$', views.AuthenticationPageView.as_view(), name='authentication'),
   path('signup/<int:group_id>/<int:customer_id>/', views.SignUpView.as_view(), name='signup'),
   url(r'^user-list/$', views.UserListView.as_view(), name='user_list'),
   # path('verify/<str:uidb64>/<str:token>/', views.verify, name='verify'),
   path('verify/<str:uidb64>/<str:token>/', views.VerifyV2.as_view(), name='verify'),
   path('verify-done/<int:user_id>/', views.verifyDone, name='set_password_done'),
   path('<int:pk>/update-password', views.UserChangePassWord.as_view(), name='update_password'),
   path('<int:pk>/update', views.UserUpdateView.as_view(), name='user_update'),
   path('<int:pk>/delete', views.UserDeleteView.as_view(), name='user_delete'),
   path('customer-user', views.CustomerUserView.as_view(), name='customer_user'),
   path('admin-user', views.AdminUserView.as_view(), name='admin_user'),
   path('delete-bulk', views.UserDeleteBulkView.as_view(), name='user_delete_bulk'),
   path('login-user/<int:user_id>/', views.loginUser, name='login_user'),
   path('resend-code/', views.reSendCode, name='resend_code'),

   # url(r'^password/$', views.change_password, name='change_password'),
   path('change_password/', views.PasswordChangeView.as_view() ,name = 'change_password'),
   # path('password_reset/', auth_views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_html_email.html'), name = 'password_reset'),
   path('user-list/download-user/', views.download_data_user, name='download_data_user'),

   path('password_reset/', views.UserPasswordForgot.as_view(), name='password_reset'),
   path('password_reset/done', views.passwordResetDone),
   path('set-password/<str:uidb64>/<str:token>/', views.UserSetPassword.as_view(), name='set_password'),
   path('set-password/done', views.setPassworDone, name='reset_password_done'),
   path('remind-bulk', views.UserRemindBulkView.as_view(), name='user_remind_bulk'),

]

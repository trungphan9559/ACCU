from django.urls import path
from f_7_2_pages import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  
    path('select-function/<int:customer_id>/<int:site_id>', views.SelectFunctionView.as_view(), name='select_function'),
    path('select-function-ms', views.SelectFunctionMSView.as_view(), name='select_function_ms'),
    path('select-site', views.SelectSiteView.as_view(), name='select_site'),
    path('select-customer', views.SelectCustomerView.as_view(), name='select_customer'),
    path('select-account/<int:customer_id>/', views.AfterSelectAccountView.as_view(), name='after_select_account'),  
    path('after-select-site/<int:site_id>', views.AfterSelectSiteView.as_view(), name='after_select_site'),
    path('select-group', views.SelectGroupView.as_view(), name='select_group'),
    path('auth/<str:site_id>', views.AuthView.as_view(), name='auth'),
    path('auth-hub', views.AuthHubView.as_view(), name='auth_hub'),
    path('auth-ga', views.AuthGAView.as_view(), name='auth_ga'),
    path('auth-gsc', views.AuthGSCView.as_view(), name='auth_gsc'),
]  
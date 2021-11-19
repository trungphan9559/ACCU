from django.urls import path
from django.conf.urls import url, include

from accu_dashboard import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  
    path('index', views.IndexDashBoard.as_view(), name='index_dashboard'),  
    url(r'^get-data-summary$', views.get_data_summary),


    
]  
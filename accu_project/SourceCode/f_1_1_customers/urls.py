# blog/urls.py
from django.urls import path
from f_1_1_customers import views
from django.conf.urls import url, include


urlpatterns = [
    path('', views.CustomerListView.as_view(), name='customer_list'),      
    path('create', views.CustomerCreateView.as_view(), name='customer_create'),      
    # path('<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),    
    path('<int:pk>/update', views.CustomerUpdateView.as_view(), name='customer_update'),    
    path('<int:pk>/delete', views.CustomerDeleteView.as_view(), name='customer_delete'),    
    path('delete-bulk', views.CustomerDeleteBulkView.as_view(), name='customer_delete_bulk'),    

    path('contract/<int:customer_group_id>-<int:customer_id>/create', views.CustomerContractCreateView.as_view(), name='customer_contract_create'),  
    path('contract', views.CustomerContractListView.as_view(), name = 'customer_contract_list'),
    path('contract/<int:pk>/delete', views.CustomerContractDeleteView.as_view(), name='customer_contract_delete'),
    path('contract/<int:pk>/update', views.CustomerContractUpdateView.as_view(), name='customer_contract_update'),
    path('contract/delete-bulk', views.ContractDeleteBulkView.as_view(), name='contract_delete_bulk'),
        # path('customer-user', views.CustomerUserView.as_view(), name='customer_user'),      
    
    url(r'^ajax-load-customer-setting$', views.ajax_load_customer_setting),
    url(r'^ajax-save-customer-setting$', views.ajax_save_customer_setting),
    url(r'^download-customer-list$', views.download_customer_list),
    url(r'^download-customer-contract-list$', views.download_customer_contract_list),

    url(r'^test$', views.test),


]
  
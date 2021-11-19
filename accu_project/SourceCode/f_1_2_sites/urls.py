# blog/urls.py
from django.conf.urls import url
from django.urls import path

from f_1_2_sites import views

urlpatterns = [
  url(r'^$', views.SiteListView.as_view(), name='site_list'),
  path('<int:site_id>/setting-property', views.SiteSettingPropertyView.as_view(), name='site_setting_property'),
  url(r'^create$', views.SiteCreateViewV2.as_view(), name='site_create'),
  path('<int:site_id>/<str:type>/site-property-create', views.SitePropertyCreateView.as_view(), name='site_property_create'),
  
  url(r'^(?P<pk>\d+)/$', views.SiteDetailView.as_view(), name='site_detail'),
  url(r'^(?P<pk>\d+)/update', views.SiteUpdateView.as_view(), name='site_update'),

  path('<int:pk>/delete', views.SiteDeleteView.as_view(), name='site_delete'),    
  path('delete-bulk', views.SiteDeleteBulkView.as_view(), name='site_delete_bulk'),    

  url(r'^ajax/load-data-f21-property$', views.load_data_f21_property),
  url(r'^ajax/load-data-f22-property$', views.load_data_f22_property),
  url(r'^ajax/load-data-f23-property$', views.load_data_f23_property),
  url(r'^ajax/load-data-f24-property$', views.load_data_f24_property),
  url(r'^ajax/update-notify-email$', views.update_notify_email),

  path('site-property/<int:pk>/<str:type>/update', views.SitePropertyUpdateView.as_view(), name='site_property_update'),    
  path('site-property/<int:pk>/<str:type>/delete', views.SitePropertyDeleteView.as_view(), name='site_property_delete'),    
  path('delete-property-bulk', views.SitePropertyDeleteBulkView.as_view(), name='site_property_delete_bulk'),    
  url(r'^ajax/load-save-property-setting$', views.load_save_property_setting),
  url(r'^ajax/save-property-setting$', views.save_property_setting),
  url(r'^ajax/load-update-property-setting$', views.load_update_property_setting),
  url(r'^ajax/update-property-setting$', views.update_property_setting),
  # setting page group
  path('<int:site_id>/setting-group-page', views.SiteSettingGroupPageView.as_view(), name='site_setting_group_page'),
  path('<int:site_id>/setting-group-page-create', views.SiteSettingGroupPageCreateView.as_view(), name='setting_group_page_create'),
  url(r'^site-group-page/(?P<pk>\d+)/update', views.SiteSettingGroupPageUpdateView.as_view(), name='site_group_page_update'),
  url(r'^site-group-page/(?P<pk>\d+)/delete', views.SiteSettingGroupPageDeleteView.as_view(), name='site_group_page_delete'),    
  path('delete-group-page-bulk', views.SiteGroupPageDeleteBulkView.as_view(), name='site_group_page_delete_bulk'),    
  url(r'^ajax/load-update-group-page-setting$', views.load_update_group_page_setting),
  url(r'^ajax/save-update-group-page-setting$', views.save_update_group_page_setting),
  url(r'^ajax/load-save-group-page-setting$', views.load_save_group_page_setting),
  url(r'^ajax/save-group-page-setting$', views.save_group_page_setting),

  #setting cta group
  path('<int:site_id>/setting-group-cta', views.SiteSettingGroupCTAView.as_view(), name='site_setting_group_cta'),
  url(r'^site-group-cta/(?P<pk>\d+)/delete', views.SiteSettingGroupCTADeleteView.as_view(), name='site_group_cta_delete'),    
  path('delete-group-cta-bulk', views.SiteGroupCTADeleteBulkView.as_view(), name='site_group_cta_delete_bulk'),    
  url(r'^ajax/load-update-group-cta-setting$', views.load_update_group_cta_setting),
  url(r'^ajax/save-update-group-cta-setting$', views.save_update_group_cta_setting),
  url(r'^ajax/load-save-group-cta-setting$', views.load_save_group_cta_setting),
  url(r'^ajax/save-group-cta-setting$', views.save_group_cta_setting),

  #Test
  url(r'^test$', views.test),

]
  
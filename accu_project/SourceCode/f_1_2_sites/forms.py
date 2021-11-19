from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from f_1_2_sites.models import Site,SitePropertySetting,SiteGroupPageSetting


class CreateSiteForm(forms.Form):
  # fields = ['id','name', 'url', 'logo', 'type', 'asana_project_id', 'person_in_charge', 'person_in_charge_management']

	name = forms.CharField(label='Name', max_length=30, required=True)
	url = forms.CharField(label='URL',max_length=50, required=True)
	logo = forms.CharField(label='Logo',max_length=200,required=True)

	type = forms.ChoiceField(label='Type', required=True)
	en_name = forms.CharField(label='En-Name',max_length=255 ,required=True)
	asana_project_id = forms.CharField(label='Asana Project Id',max_length=50, required=True)
	person_in_charge = forms.ChoiceField(label='Persion in change', required=True)
	person_in_charge_management = forms.ChoiceField(label='Persion in change management', required=True)


	def clean_name(self):
		name = self.cleaned_data.get('name')
		if len(Site.objects.filter(name=name)) > 0:
			raise forms.ValidationError("Name is exist")
		return name
	
	def clean_url(self):
		url = str(self.cleaned_data.get('url')).replace("https://","").replace("http://","").replace("www.","")
		if len(Site.objects.filter(url__contains=url)) > 0:
			raise forms.ValidationError("Url is exist")
		return url

class CreateSiteGroupPageSettingForm(forms.Form):
  	
	group_name = forms.CharField(label='Group name', max_length=255, required=True)
	resource_top_page_id = forms.CharField(label='Resource Top Page', max_length=255, required=True)

	hb_list_master_id = forms.CharField(label='Hubspot List Master', max_length=255, required=True)
	hb_list_name_default = forms.CharField(label='Hubspot List Name Default', max_length=255, required=True)
	is_common = forms.BooleanField(label='Is common', required=False)
	site = forms.IntegerField(label="Site",widget=forms.HiddenInput)

	def clean_group_name(self):
		if(self.is_valid):
			group_name = self.cleaned_data.get('group_name')
			# self.data lấy được hết giá trị của model
			site_id = int(self.data["site"])
			
			if len(SiteGroupPageSetting.objects.filter(group_name=group_name,is_active=1,site=site_id)) > 0:
				raise forms.ValidationError("Group Name is exist")
			
			return group_name

class UpdateSiteGroupPageSettingForm(forms.Form):
  	
	group_name = forms.CharField(label='Group name', max_length=255, required=True)
	resource_top_page_id = forms.CharField(label='Resource Top Page', max_length=255, required=True)
	is_common = forms.BooleanField(label='Is common', required=False)
	site = forms.IntegerField(label="Site",widget=forms.HiddenInput)
	id = forms.IntegerField(label="id",widget=forms.HiddenInput)
	
	def clean_group_name(self):
		if(self.is_valid):
			group_name = self.cleaned_data.get('group_name')
			# self.data lấy được hết giá trị của model
			site_id = int(self.data["site"])
			group_page_id = int(self.data["id"])

			list_obj_group_page_setting_update = SiteGroupPageSetting.objects.filter(group_name=group_name,is_active=1,site=site_id)
			group_name_exist = False

			for item in list_obj_group_page_setting_update:
				if item.id != group_page_id:
					group_name_exist = True

			if group_name_exist:
				raise forms.ValidationError("Group Name is exist")
			
			return group_name
	
	def clean_is_common(self):
		is_common = self.cleaned_data.get('is_common')
		return is_common


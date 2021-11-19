from __Config.Include.Common_Include import *
from f_1_2_sites.models import Site, TYPE_CHOICES,SitePropertySetting,SiteAuth,SiteGroupPageSetting,SiteGroupCTASetting
from f_1_2_sites.forms import CreateSiteForm,CreateSiteGroupPageSettingForm,UpdateSiteGroupPageSettingForm
from django.contrib.auth import get_user_model
from f_1_1_customers.models import CustomerGroup

class SiteListView(PermissionRequiredMixin, ListView):
  model = Site
  permission_required = ['f_1_2_sites.view_site']
  template_name = 'apps/f_1_2_sites/site_list.html'
  context_object_name = 'list_site'
  ordering = ['name']

  def get_queryset(self):
    #1)Dữ liệu
    qs = super().get_queryset()
    
    # #1.2)Dữ liệu từ request
    if self.request.GET:
      param_type = str(self.request.GET.get('type',-1))
      param_status = int(self.request.GET.get('status',-1))
      param_group = int(self.request.GET.get('group',-1))
    else:
      return qs

    #2.0) Filter theo status
    if param_group != -1:
      obj_customer_group = CustomerGroup.objects.get(pk=param_group)
      qs = obj_customer_group.site.all()

    #2.1)Filter theo type
    if param_type != '-1':
      qs = qs.filter(type=param_type)


    #2.2) Filter theo status
    if param_status != -1:
      qs = qs.filter(is_active=param_status)
    

    #3)Trả về
    return qs
  
  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()

    list_customer_groups = CustomerGroup.objects.all()
    data['list_customer_groups'] = list_customer_groups
    return data


class SiteSettingPropertyView(PermissionRequiredMixin, ListView):
  model = Site
  permission_required = ['f_1_2_sites.view_site']
  template_name = 'apps/f_1_2_sites/site_setting_property.html'
  context_object_name = 'site_setting_property'
  # ordering = ['name']

  def get_context_data(self, **kwargs):
    
    #1)Dữ liệu
    data = super().get_context_data()
    list_sites = Site.objects.all()

    #3)Trả về
    data["list_sites"] = list_sites
    
    return data

  def get_queryset(self):
    #1)Dữ liệu
    qs = super().get_queryset()
    
    # #1.2)Dữ liệu từ request
    if self.kwargs['site_id']:
      param_site_id = int(self.kwargs['site_id'])
      
    else:
      
      return qs

    #2.1)Filter theo site
    if param_site_id != -1:
      qs = qs.filter(id=param_site_id)

    #3)Trả về
    data = {
            "site_id" : param_site_id
            }
    return data
  
class SiteDetailView(PermissionRequiredMixin, DetailView):
  model = Site
  permission_required = ['f_1_2_sites.view_site']
  template_name = 'apps/f_1_2_sites/site_detail.html'

class SiteUpdateView(SuccessMessageMixin ,PermissionRequiredMixin, UpdateView):
  model = Site
  permission_required = ['f_1_2_sites.change_site']
  template_name = 'apps/f_1_2_sites/site_update.html'
  fields = ['name', 'url', 'logo', 'is_active', 'type', 'en_name','asana_project_id', 'person_in_charge', 'person_in_charge_management']
  
  success_message = 'Update %(name)s successed'

  def get_form(self, form_class=None):
    form = super().get_form(form_class)  
    # form.fields['domain'].disabled = True
    # form.fields['customer_group'].disabled = True
    return form

  def get_success_url(self):
    return reverse("site_update", args=(self.kwargs['pk'],))  
  
  

class SiteDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
  model = Site
  permission_required = ['f_1_2_sites.delete_site']
  template_name = 'apps/f_1_2_sites/site_delete.html'
  fields = ['id','name', 'url', 'logo', 'type', 'en_name', 'asana_project_id', 'person_in_charge', 'person_in_charge_management']

  # success_url = reverse_lazy('site_list')
  success_message = 'Delete  %(name)s successed'

  # def delete(self, request, *args, **kwargs):
  #   messages.success(self.request, self.success_message)
  #   return super().delete(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    data = super().get_context_data()
    site_id = self.kwargs['pk']
    obj_site = Site.objects.get(pk=site_id)

    data["name"] = obj_site.name
    data['pk'] = site_id
    
    return data
    
  def delete(self, request, *args, **kwargs):
    site_id = self.kwargs['pk']
    
    obj_site = Site.objects.get(pk=site_id)
    Site(
      id = site_id,
      is_active= 0,
      name= obj_site.name,
      url= obj_site.url,
      logo= obj_site.logo,
      created_date=obj_site.created_date,
      last_updated= obj_site.last_updated,
      contract_start_date = obj_site.contract_start_date,
      type = obj_site.type,
      en_name = obj_site.en_name,
      asana_project_id = obj_site.asana_project_id,
      person_in_charge = obj_site.person_in_charge,
      person_in_charge_management = obj_site.person_in_charge_management
    ).save()

    messages.success(self.request, self.success_message)

    return HttpResponseRedirect(self.get_success_url())
      
  def get_success_url(self):
    return reverse("site_list") 

class SiteDeleteBulkView(SuccessMessageMixin, PermissionRequiredMixin, View):
  model = Site
  permission_required = ['f_1_2_sites.delete_site']
  template_name = 'apps/f_1_2_sites/site_delete.html'
  success_url = reverse_lazy('site_list')

  def post(self, request):
    #1)Dữ liệu
    list_id = self.request.POST['list_id'].split(',')
    #2)Xử lý, Ko xóa mà chỉ có inactive nó thôi
    Site.objects.filter(pk__in=list_id).update(is_active=0)

    #2.1) Xoa luon chư khong inactive 
    # Site.objects.filter(pk__in=list_id).delete()

    return HttpResponse(1)

class SiteCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView, forms.Form):
  model = Site
  permission_required = ['f_1_2_sites.add_site']
  template_name = 'apps/f_1_2_sites/site_create.html'
  fields = ['id','name', 'url', 'logo', 'type', 'en_name', 'asana_project_id', 'person_in_charge', 'person_in_charge_management']
  success_url = reverse_lazy('site_create')
  success_message = 'Site %(name)s was created.'

  def get_form(self, form_class=None):
    #1)Lấy form
    form = super().get_form(form_class)

    #2)Tạo code mặc định
    form.fields['id'].widget = forms.HiddenInput()
    form.fields['id'].initial  = random.randint(100000,999999)
    return form

  def form_valid(self, form):
    while Site.objects.filter(id=form.instance.id):
      form.instance.id = random.randint(100000,999999)
    return super().form_valid(form)

class SiteCreateViewV2(SuccessMessageMixin, PermissionRequiredMixin, FormView):
  form_class = CreateSiteForm
  permission_required = ['f_1_2_sites.add_site']
  template_name = 'apps/f_1_2_sites/site_create.html'
  # fields = ['id','name', 'url', 'logo', 'type', 'asana_project_id', 'person_in_charge', 'person_in_charge_management']
  success_url = reverse_lazy('site_create')
  success_message = 'Site %(name)s was created.'

  def get_form(self, form_class=None):
    #1)Lấy form
    form = super().get_form(form_class)

    #2)Tạo data cho các trường Type
    form.fields['type'].choices = TYPE_CHOICES

    #2)Tạo data cho các Persion in change
    list_user = get_user_model().objects.all()
    PERSON_IN_CHANGE_CHOICES = ((i.id,i.username) for i in list_user )
    PERSON_IN_CHANGE_MANAGEMENT_CHOICES = ((i.id,i.username) for i in list_user )
    form.fields['person_in_charge'].choices = PERSON_IN_CHANGE_CHOICES
    form.fields['person_in_charge_management'].choices = PERSON_IN_CHANGE_MANAGEMENT_CHOICES

    return form
  
  def form_valid(self, form):
    #1)Dữ liệu
    id = random.randint(100000,999999)
    while Site.objects.filter(id=id):
      id = random.randint(100000,999999)

    name = form.cleaned_data['name']
    url = form.cleaned_data['url']
    logo = form.cleaned_data['logo']
    type = form.cleaned_data['type']
    en_name = form.cleaned_data['en_name']
    asana_project_id = form.cleaned_data['asana_project_id']
    person_in_charge = form.cleaned_data['person_in_charge']
    person_in_charge_management = form.cleaned_data['person_in_charge_management']

    #Lấy obj_user
    user_person_in_charge = User.objects.get(id=person_in_charge)
    user_person_in_charge_management = User.objects.get(id=person_in_charge_management)

    site_obj = Site( id=id, name=name, url=url, logo=logo, 
                     type=type, asana_project_id = asana_project_id,
                      person_in_charge = user_person_in_charge,
                       person_in_charge_management= user_person_in_charge_management,
                       en_name = en_name)
    site_obj.save()
    return super().form_valid(form)


def load_data_f21_property(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_site_id = request.POST["site_id"]
    obj_setting_f21 = F21PropertySetting.objects.filter(site=param_site_id)
    list_email = ""
    if obj_setting_f21:
      list_email = ",".join((json.loads(obj_setting_f21[0].email)))

    obj_setting_site_property = SitePropertySetting.objects.filter(type="f21",site=param_site_id)
    
    list_property = []
    if obj_setting_site_property:
      list_property = obj_setting_site_property

    #3) dữ liệu trả về  
    data = {
      "list_email" : list_email,
      "list_property": list_property,
      "site_id" : param_site_id
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_property/f21_setting_property_table.html'

    return render(request, tmp_file_path, data)

def load_data_f22_property(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_site_id = request.POST["site_id"]
    obj_setting_f22 = F22PropertySetting.objects.filter(site=param_site_id)
    list_email = ""
    if obj_setting_f22:
      list_email = ",".join((json.loads(obj_setting_f22[0].email)))

    obj_setting_site_property = SitePropertySetting.objects.filter(type="f22",site=param_site_id)
    list_property = []
    if obj_setting_site_property:
      list_property = obj_setting_site_property

    #3) dữ liệu trả về  
    data = {
      "list_email" : list_email,
      "list_property": list_property,
      "site_id" : param_site_id
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_property/f22_setting_property_table.html'

    return render(request, tmp_file_path, data)

def load_data_f23_property(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_site_id = request.POST["site_id"] 
    obj_setting_site_property = SitePropertySetting.objects.filter(type="f23",site=param_site_id)
    list_property = []
    if obj_setting_site_property:
      list_property = obj_setting_site_property

    #3) dữ liệu trả về  
    data = {
      "list_property": list_property,
      "site_id" : param_site_id
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_property/f23_setting_property_table.html'

    return render(request, tmp_file_path, data)


def load_data_f24_property(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_site_id = request.POST["site_id"] 
    obj_setting_site_property = SitePropertySetting.objects.filter(type="f24",site=param_site_id)
    list_property = []
    if obj_setting_site_property:
      list_property = obj_setting_site_property

    #3) dữ liệu trả về  
    data = {
      "list_property": list_property,
      "site_id" : param_site_id
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_property/f24_setting_property_table.html'

    return render(request, tmp_file_path, data)

class SitePropertyCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView):
  
  model = SitePropertySetting
  permission_required = ['f_1_2_sites.add_sitepropertysetting']
  template_name = 'apps/f_1_2_sites/setting_property/site_property_create.html'
  fields = ["property_label","property_internal_name","sort","site","type"]
  success_message = 'Site Property %(property_internal_name)s was created.'


  def get_success_url(self): 
    return reverse("site_property_create" ,args=(self.kwargs['site_id'],self.kwargs['type']))

  def get_form(self, form_class=None):
    #1)Lấy form
    form = super().get_form(form_class)
    
    site_id = self.kwargs['site_id']
    type_function = self.kwargs['type']
    
    form.fields['site'].widget = forms.HiddenInput()
    form.fields['site'].initial  = int(site_id)
    form.fields['type'].widget = forms.HiddenInput()
    form.fields['type'].initial  = type_function

    #2)Tạo data cho các trường Type
    list_property = []
    site_auth_obj = SiteAuth.objects.filter(site=site_id)
    if site_auth_obj:
      hub_authen  = site_auth_obj[0].last_hub_refresh_token
      if hub_authen != "-1":
        list_property = HubspotHandleContactPropertiesAPI(site_id=site_id).get_all_properties()
    
    form.fields['property_internal_name'] = forms.ChoiceField(required=True,label="Internal name")
    #2.1) Loai bo cac property da co
    obj_site_setting = SitePropertySetting.objects.filter(site=site_id, type=type_function)
    list_property_internal_name = []
    for i in obj_site_setting:
      list_property_internal_name.append(i.property_internal_name) 

    list_property_choices = []
    for _property in list_property:
      if _property["internal_name"] not in list_property_internal_name:
        list_property_choices.append((_property["internal_name"],_property["internal_name"]))

    form.fields['property_internal_name'].choices = (list_property_choices)
    
    # #2)Tạo data cho các Persion in change
    # form.fields['property_internal_name'].choices = ((i.internal_name,i.internal_name) for i in list_property )

    return form
  
  def get_context_data(self, **kwargs):
    data = super().get_context_data()
    data['site_id'] = self.kwargs['site_id']
    data['type'] = self.kwargs['type']
    list_property = []
    site_auth_obj = SiteAuth.objects.filter(site=self.kwargs['site_id'])
    if site_auth_obj:
      hub_authen  = site_auth_obj[0].last_hub_refresh_token
      if hub_authen != "-1":
        list_property = HubspotHandleContactPropertiesAPI(site_id=self.kwargs['site_id']).get_all_properties()
    data['list_contact_property'] = list_property
    
    dict_property = {x["internal_name"] : x for x in list_property}
    dict_property_check = {}
    for key,value in dict_property.items():
      options = value["options"]
      list_options = []
      for option in options:
        list_options.append({option["value"] : option["label"]})
      
      dict_property_check[key] = list_options

    data["dict_property"] = dict_property_check

    return data
  

  def form_valid(self, form):
    list_contact_property = HubspotHandleContactPropertiesAPI(form.cleaned_data['site']).get_all_properties()
    dict_properties = {}
    param_property_internal_name = form.cleaned_data['property_internal_name']
    dict_contact_property = { x['internal_name'] : x for x in list_contact_property}
   
    dict_properties = dict_contact_property.get(param_property_internal_name)
    options = dict_properties["options"]
    list_options = []
    for option in options:
      list_options.append({option["value"] : option["label"]})
    
    site_property = SitePropertySetting(
      site = form.cleaned_data['site'],
      property_label = form.cleaned_data['property_label'],
      property_internal_name = param_property_internal_name,
      type = form.cleaned_data['type'],
      sort = form.cleaned_data['sort'],
      properties = json.dumps(list_options),
    )

    site_property.save()
    success_message = param_property_internal_name +' property was created.'
    messages.add_message(self.request, messages.SUCCESS, success_message)
    return HttpResponseRedirect(self.get_success_url())


class SitePropertyUpdateView(SuccessMessageMixin ,PermissionRequiredMixin, UpdateView):
  model = SitePropertySetting
  permission_required = ['f_1_2_sites.change_sitepropertysetting']
  template_name = 'apps/f_1_2_sites/setting_property/site_property_update.html'
  fields = ["property_label","property_internal_name","sort"]
  
  success_message = 'Update property %(property_internal_name)s successed'

  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    form.fields['property_internal_name'].disabled = True
    
    return form

  def get_context_data(self, **kwargs):
    data = super().get_context_data()
    print(self.kwargs['pk'],self.kwargs['type'],"get_context_data")
    property_id = self.kwargs['pk']
    data['type'] = self.kwargs['type']
    data['pk'] = property_id
    return data

  def get_success_url(self): 
    return reverse("site_property_update" ,args=(self.kwargs['pk'],self.kwargs['type']))

class SitePropertyDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
  model = SitePropertySetting
  permission_required = ['f_1_2_sites.delete_sitepropertysetting']
  template_name = 'apps/f_1_2_sites/setting_property/site_property_delete.html'
  # success_url = reverse_lazy('site_setting_property')
  success_message = 'Delete Site Property successed'

  def get_context_data(self, **kwargs):
    data = super().get_context_data()
    
    property_id = self.kwargs['pk']
    type = self.kwargs['type']
    print('type--== ',type)
    obj_property = SitePropertySetting.objects.get(pk=property_id)

    data["property_internal_name"] = obj_property.property_internal_name
    data['pk'] = property_id
    data["type"] = type
    data["site_id"] = obj_property.site
    return data
    
  def delete(self, request, *args, **kwargs):
    messages.success(self.request, self.success_message)
    
    obj_setting = SitePropertySetting.objects.filter(id=self.kwargs['pk'])[0]
    site_id = obj_setting.site_id
    obj_setting.delete()
    return self.get_success_url(site_id)

  def get_success_url(self,site_id):
    
    return redirect("/sites/{}/setting-property#{}".format(site_id,self.kwargs['type']))   


class SitePropertyDeleteBulkView(SuccessMessageMixin, PermissionRequiredMixin, View):
  model = SitePropertySetting
  permission_required = ['f_1_2_sites.delete_sitepropertysetting']
  template_name = 'apps/f_1_2_sites/setting_property/site_property_delete.html'
  #success_url = reverse_lazy('site_list')

  def post(self, request):
    #1)Dữ liệu
    list_id = self.request.POST['list_id'].split(',')

    #2)Xử lý, Ko xóa mà chỉ có inactive nó thôi
    # Site.objects.filter(pk__in=list_id).update(is_active=0)

    #2.1) Xoa luon chư khong inactive 
    
    SitePropertySetting.objects.filter(pk__in=list_id).delete()

    return HttpResponse(1)

  def get_success_url(self):
    obj_property = SitePropertySetting.objects.get(pk=self.kwargs['pk'])
    site_id = obj_property.site.id
    
    return redirect("/sites/{}/setting-property#{}".format(site_id,self.kwargs['type']))   

def load_save_property_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_site_id = request.POST["site_id"]
    param_type = request.POST["type"]
    
    list_property = HubspotHandleContactPropertiesAPI(param_site_id).get_all_properties()
    dict_property = {x["internal_name"] : x for x in list_property}
    dict_property_check = {}
    for key,value in dict_property.items():
      options = value["options"]
      list_options = []
      for option in options:
        list_options.append({option["value"] : option["label"]})
      
      dict_property_check[key] = list_options

    list_form = HubspotHandleFormsAPI(param_site_id).get_form_name_and_guid_id()

    #3) dữ liệu trả về  
    data = {
      "list_property": list_property,
      "dict_property" : dict_property_check,
      "list_form" : list_form,
      "site_id" : param_site_id,
      "type" : param_type
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_property/modal/modal-create-property-setting-detail.html'

    return render(request, tmp_file_path, data)      

def save_property_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_site_id = request.POST["site_id"]
    param_type = request.POST["type"]
    param_property_label = request.POST["property_label"]
    param_property_sort = request.POST["property_sort"]
    param_property_internal = request.POST["property_internal"]
    param_list_option_property = json.loads(request.POST["list_option_property"])
    # dict_info = {
    #   'property_label' : param_property_label,
    #   'property_internal_name' : param_property_internal,
    #   'properties' : param_list_option_property,
    #   'type' : param_type,
    #   'sort' : param_property_sort,
    #   'site_id': param_site_id
    # }
    # print(dict_info,"dict_info")
    #2) Check xem property_internal_name đã có chay chưa
    check_is_exist = SitePropertySetting.objects.filter(site_id=param_site_id,type=param_type,property_internal_name=param_property_internal)

    if check_is_exist:
      return HttpResponse(0)

    #3) Lưu vô db
    
    obj_setting = SitePropertySetting(
                                      property_label=param_property_label,
                                      property_internal_name=param_property_internal,
                                      properties=json.dumps(param_list_option_property),
                                      type=param_type,
                                      sort=param_property_sort,
                                      site_id=param_site_id
                                      )
    obj_setting.save()                           

    return HttpResponse(1)

def load_update_property_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_property_id = request.POST["property_id"]
    property_info = SitePropertySetting.objects.get(id=param_property_id)
    
    # property_info.properties = json.loads(property_info.properties)

    #3) dữ liệu trả về  

    data = {
      "property_info": property_info,
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_property/modal/modal-update-property-setting-detail.html'

    return render(request, tmp_file_path, data)



def update_property_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_property_id = request.POST["property_id"]
    param_property_label = request.POST["property_label"]
    param_property_sort = request.POST["property_sort"]
    param_list_option_property = json.loads(request.POST["list_option_property"])

    #2) Lưu vô db
    # dict_info = {
    #   'property_label' : param_property_label,
    #   'id' : param_property_id,
    #   'properties' : param_list_option_property,
    #   'sort' : param_property_sort,
    # }
    obj_setting = SitePropertySetting.objects.get(id=param_property_id)
    obj_setting = SitePropertySetting(
                                      id = obj_setting.id,
                                      property_label=param_property_label,
                                      property_internal_name=obj_setting.property_internal_name,
                                      properties=json.dumps(param_list_option_property),
                                      type=obj_setting.type,
                                      sort=param_property_sort,
                                      site_id=obj_setting.site_id
                                      )
    obj_setting.save()    

    return HttpResponse(1)

def update_notify_email(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    param_site_id = int(request.POST["site_id"])
    param_type = request.POST["type"] 
    param_list_email = request.POST["list_email"]

    list_email = []
    if param_list_email != "":
      list_email = param_list_email.split(",")

    list_email = json.dumps(list_email)

    #2) lưu db tùy theo type truyền lên
    if param_type == "f21":
      obj_setting = F21PropertySetting.objects.filter(site_id=param_site_id)
      if not obj_setting:
        obj_setting = F21PropertySetting(site_id=param_site_id,email=list_email)
      else:
        obj_setting = obj_setting[0]
        obj_setting = F21PropertySetting(id=obj_setting.id,site_id=obj_setting.site_id,email=list_email)
      
      obj_setting.save()

    if param_type == "f22":
      obj_setting = F22PropertySetting.objects.filter(site_id=param_site_id)
      if not obj_setting:
        obj_setting = F22PropertySetting(site_id=param_site_id,email=list_email)
      else:
        obj_setting = obj_setting[0]
        obj_setting = F22PropertySetting(id=obj_setting.id,site_id=obj_setting.site_id,email=list_email)    

      obj_setting.save()

    return HttpResponse(1)

#============== SiteSettingGroupPage ====================#
class SiteSettingGroupPageView(PermissionRequiredMixin, ListView):
  model = SiteGroupPageSetting
  permission_required = ['f_1_2_sites.view_site']
  template_name = 'apps/f_1_2_sites/site_setting_group_page.html'
  context_object_name = 'site_setting_group'
  # ordering = ['name']

  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()
    list_sites = Site.objects.all()

    #3)Trả về
    data["list_sites"] = list_sites
    
    return data

  def get_queryset(self):
    #1)Dữ liệu
    qs = super().get_queryset()
    
    # #1.2)Dữ liệu từ request
    if self.kwargs['site_id']:
      param_site_id = int(self.kwargs['site_id'])
      
    else:
      return qs

    #2.1)Filter theo site
    if param_site_id != -1:
      qs = qs.filter(id=param_site_id)
    
    list_setting_page_group = SiteGroupPageSetting.objects.filter(site_id=param_site_id,is_active=1)
    
    #3)Trả về
    data = {
            "site_id" : param_site_id,
            "list_setting_page_group" : list_setting_page_group
            }
    
    return data

class SiteSettingGroupPageCreateView(SuccessMessageMixin, PermissionRequiredMixin, FormView):
  
  form_class = CreateSiteGroupPageSettingForm
  permission_required = ['f_1_2_sites.add_sitegrouppagesetting']
  template_name = 'apps/f_1_2_sites/setting_group_page/site_group_page_create.html'


  def get_success_url(self): 
    site_id = self.kwargs['site_id']
    return reverse("setting_group_page_create" ,args=(site_id,))

  def get_form(self, form_class=None):
    #1)Lấy form
    form = super().get_form(form_class)
    site_id = self.kwargs['site_id']    

    list_all_page = HubspotHandleCMSPageAPI(site_id).get_all_pages()
    list_resource_page = [i for i in list_all_page if "[Test][accu][WEB]"  in i["name"]]
    
    list_hb_list = HubspotHandleContactListsAPI(site_id).get_all_contact_lists()

    list_resource_choices = []
    for page_info in list_resource_page:
      list_resource_choices.append((page_info["id"],page_info["name"]))
    
    list_hb_list_choices = []
    for hb_list_info in list_hb_list:
      list_hb_list_choices.append((hb_list_info["id"],hb_list_info["name"]))

    form.fields['resource_top_page_id'] = forms.ChoiceField(required=True,label="Resource Top Page")
    form.fields['resource_top_page_id'].choices = (list_resource_choices)

    form.fields['hb_list_master_id'] = forms.ChoiceField(required=True,label="Hubspot List Master")
    form.fields['hb_list_master_id'].choices = (list_hb_list_choices)

    form.fields['site'].widget = forms.HiddenInput()
    form.fields['site'].initial  = int(site_id)
    
    return form
  
  def get_context_data(self, **kwargs):
    data = super().get_context_data()
    data['site_id'] = self.kwargs['site_id']    
    return data

  def form_valid(self, form):
    param_group_name = form.cleaned_data['group_name']
    param_hb_list_name = form.cleaned_data['hb_list_name_default']
    resource_top_page_id = form.cleaned_data['resource_top_page_id']
    hb_list_master_id = form.cleaned_data['hb_list_master_id']
    is_common = form.cleaned_data['is_common']
    site_id = form.cleaned_data['site']
    
    if is_common:
      list_obj_group = SiteGroupPageSetting.objects.filter(site=site_id,is_active=1)
      for item in list_obj_group:
        #1) set lại các group thuộc site về is_common = False
        SiteGroupPageSetting(id=item.id,
                              group_name = item.group_name,
                              resource_top_page_id = item.resource_top_page_id,
                              landing_page_master_id = item.landing_page_master_id,
                              is_common = False,
                              created_date = item.created_date,
                              last_updated = item.last_updated,
                              site_id = item.site,
                              thanks_page_master_id = item.thanks_page_master_id,
                              folder_pdf_id = item.folder_pdf_id,
                              folder_thumb_id = item.folder_thumb_id,
                              hb_list_master_id = item.hb_list_master_id,
                              hb_list_name_default = item.hb_list_name_default
                            ).save()

    site_group_page_setting_property = SiteGroupPageSetting(
      group_name = param_group_name,
      resource_top_page_id = resource_top_page_id,
      hb_list_name_default = param_hb_list_name,
      hb_list_master_id = hb_list_master_id,
      is_common = is_common,
      site_id = site_id
    )

    site_group_page_setting_property.save()
    success_message = param_group_name +' was created.'
    messages.add_message(self.request, messages.SUCCESS, success_message)
    
    return HttpResponseRedirect(self.get_success_url())

class SiteSettingGroupPageUpdateView(SuccessMessageMixin ,PermissionRequiredMixin, FormView):
  form_class = UpdateSiteGroupPageSettingForm
  permission_required = ['f_1_2_sites.change_sitegrouppagesetting']
  template_name = 'apps/f_1_2_sites/setting_group_page/site_group_page_update.html'
 
  def get_form(self, form_class=None):
    form = super().get_form(form_class)
    group_page_id = self.kwargs['pk']
    #1) biến lấy từ id
    obj_group_page = SiteGroupPageSetting.objects.get(id=group_page_id)
    group_name = obj_group_page.group_name
    site_id = obj_group_page.site.id
    resource_top_page_id = obj_group_page.resource_top_page_id
    is_common = obj_group_page.is_common
    
    #2) lấy danh sách page source top
    list_all_page = HubspotHandleCMSPageAPI(site_id).get_all_pages(is_draft=False)
    # list_resource_page = [i for i in list_all_page if "[accu]"  in i["name"]]
    list_resource_page = [i for i in list_all_page]
    
    list_resource_choices = []
    for page_info in list_resource_page:
      list_resource_choices.append((page_info["id"],page_info["name"]))
    
    form.fields["group_name"] = forms.CharField(label='Group name', max_length=255, required=True,initial=group_name)

    form.fields['resource_top_page_id'] = forms.ChoiceField(required=True,label="Resource Top Page",initial=resource_top_page_id)
    form.fields['resource_top_page_id'].choices = (list_resource_choices)

    form.fields["is_common"] = forms.BooleanField(label='Is common', required=False,initial=is_common)
	  
    form.fields['id'].widget = forms.HiddenInput()
    form.fields['id'].initial  = int(group_page_id)

    form.fields['site'].widget = forms.HiddenInput()
    form.fields['site'].initial  = int(site_id)

    return form

  def get_context_data(self, **kwargs):
    data = super().get_context_data()
    group_page_id = self.kwargs['pk']

    data['pk'] = group_page_id
    return data

  def form_valid(self, form):
    #1 biến truyền lên)
    param_id = form.cleaned_data['id']
    param_group_name = form.cleaned_data['group_name']
    resource_top_page_id = form.cleaned_data['resource_top_page_id']
    is_common = form.cleaned_data['is_common']
    site_id = form.cleaned_data['site']
    
    #2 update group page)
    obj_group_page = SiteGroupPageSetting.objects.get(id=param_id)
    created_date = obj_group_page.created_date
    last_updated = datetime.now()

    site_group_page_setting_property = SiteGroupPageSetting(
      id = param_id,
      group_name = param_group_name,
      resource_top_page_id = resource_top_page_id,
      is_common = is_common,
      site_id = site_id,
      created_date = created_date,
      last_updated=last_updated
    )
    site_group_page_setting_property.save()

    success_message = param_group_name +' was updated.'
    messages.add_message(self.request, messages.SUCCESS, success_message)
    
    return HttpResponseRedirect(self.get_success_url())


  def get_success_url(self):
    return reverse("site_group_page_update", args=(self.kwargs['pk'],))  

class SiteSettingGroupPageDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
  model = SiteGroupPageSetting
  permission_required = ['f_1_2_sites.delete_sitegrouppagesetting']
  template_name = 'apps/f_1_2_sites/setting_group_page/site_group_page_delete.html'
  success_url = reverse_lazy('site_setting_group_page')
  success_message = 'Delete Site Group Page successed'

  def get_context_data(self, **kwargs):
    data = super().get_context_data()
    group_page_id = self.kwargs['pk']
    obj_group_page = SiteGroupPageSetting.objects.get(pk=group_page_id)

    data["group_name"] = obj_group_page.group_name
    data['pk'] = group_page_id
    # data["site_id"] = obj_group_page.site.id
    return data
    
  def delete(self, request, *args, **kwargs):
    group_page_id = self.kwargs['pk']
    
    obj_group_page = SiteGroupPageSetting.objects.get(pk=group_page_id)
    site_group_page_setting = SiteGroupPageSetting(
      id = group_page_id,
      is_active= 0,
      site_id= obj_group_page.site,
      created_date=obj_group_page.created_date,
      last_updated= obj_group_page.last_updated,
      group_name = obj_group_page.group_name,
      resource_top_page_id = obj_group_page.resource_top_page_id,
      landing_page_master_id = obj_group_page.landing_page_master_id,
      thanks_page_master_id = obj_group_page.thanks_page_master_id,
      is_common = obj_group_page.is_common
    )

    site_group_page_setting.save()
    messages.success(self.request, self.success_message)

    return HttpResponseRedirect(self.get_success_url())
      
  def get_success_url(self):
    
    obj_group_page = SiteGroupPageSetting.objects.get(id=int(self.kwargs['pk']))
    site_id = obj_group_page.site.id
    
    return reverse("site_setting_group_page", args=(site_id,)) 


class SiteGroupPageDeleteBulkView(SuccessMessageMixin, PermissionRequiredMixin, View):
  model = SiteGroupPageSetting
  permission_required = ['f_1_2_sites.delete_sitegrouppagesetting']
  template_name = 'apps/f_1_2_sites/setting_group_page/site_group_page_delete.html'
  #success_url = reverse_lazy('site_list')

  def post(self, request):
    #1)Dữ liệu
    list_id = self.request.POST['list_id'].split(',')

    #2)Xử lý, Ko xóa mà chỉ có inactive nó thôi
    SiteGroupPageSetting.objects.filter(pk__in=list_id).update(is_active=0)

    return HttpResponse(1)

  def get_success_url(self):
    obj_property = SiteGroupPageSetting.objects.get(pk=self.kwargs['pk'])
    site_id = obj_property.site.id
    return reverse("modal_site_group_page_delete_bulk", args=(site_id,))   

def load_update_group_page_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    group_page_id = request.POST["group_page_id"]
    obj_group_page = SiteGroupPageSetting.objects.get(pk=group_page_id)

    resource_top_page_id_current = obj_group_page.resource_top_page_id
    is_common = obj_group_page.is_common
    site_id = obj_group_page.site.id

    list_hb_list = HubspotHandleContactListsAPI(site_id).get_all_contact_lists()
    list_all_page = HubspotHandleCMSPageAPI(site_id).get_all_pages(is_draft=False)
    # list_resource_page = [i for i in list_all_page if "[accu]"  in i["name"]]
    list_resource_page = [i for i in list_all_page]

    if is_common:
      is_common = 1
    else:
      is_common = 0  

    list_data_folder = []

    dict_data_folder_info = HubspotHandleCMSFilesAPI(site_id).get_all_folder_to_dict_key_id()
    
    name_folder_thumb = ""
    name_folder_pdf = ""
    
    if obj_group_page.folder_pdf_id != "":
      name_folder_pdf = dict_data_folder_info[int(obj_group_page.folder_pdf_id)]["name"]

    if obj_group_page.folder_thumb_id != "":
      name_folder_thumb = dict_data_folder_info[int(obj_group_page.folder_thumb_id)]["name"]

    #2) Laays ffolder hubspot
    dict_data_folder = HubspotHandleCMSFilesAPI(site_id).get_all_folder_type_dict()
    
    for i in dict_data_folder:
      list_data_folder.append(dict_data_folder[i])

    
    def _append_child(data):
      data_return = {
        'id': data['id'],
        'text': data['name'],
        'items': [_append_child(child) for key_child,child in data['child'].items()],
      }
      return data_return

    list_data_folder_custom = [_append_child(root_value) for root_name,root_value in dict_data_folder.items()]

    



    #3) dữ liệu trả về  
    data = {
      "list_resource_page" : list_resource_page,
      "obj_group_page" : obj_group_page,
      "list_hb_list" : list_hb_list,
      "is_common" : is_common,
      "name_folder_thumb" : name_folder_thumb,
      "name_folder_pdf" : name_folder_pdf,
      "list_data_folder" : list_data_folder,
      "list_data_folder_custom" : list_data_folder_custom,
    }
    
    tmp_file_path = 'apps/f_1_2_sites/setting_group_page/modal-update-group-page-detail.html'

    return render(request, tmp_file_path, data)

def save_update_group_page_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    group_page_id = int(request.POST["group_page_id"])
    site_id = request.POST["site_id"]
    group_name = request.POST["group_name"]
    folder_thumb_id = request.POST["folder_thumb_id"]
    resource_page_id = request.POST["resource_page_id"]
    hb_list_master_id = request.POST["hb_list_master_id"]
    folder_pdf_id = request.POST["folder_pdf_id"]
    hb_list_name_default = request.POST["hb_list_name_default"]
    is_common = int(request.POST["is_common"])
    #2) Check group name tồn tại hay chưa
    if is_common == 1:
      is_common = True
    else:
      is_common = False

    list_obj_group_page_setting_update = SiteGroupPageSetting.objects.filter(group_name=group_name,is_active=1,site=site_id)
    group_name_exist = False

    for item in list_obj_group_page_setting_update:
      if item.id != group_page_id:
        group_name_exist = True

    if group_name_exist:
      return HttpResponse(0)

    #3) check is_common
    if is_common:
      list_obj_group = SiteGroupPageSetting.objects.filter(site=site_id,is_active=1)
      for item in list_obj_group:
        #3.1) set lại các group thuộc site về is_common = False
        SiteGroupPageSetting(id=item.id,
                              group_name = item.group_name,
                              resource_top_page_id = item.resource_top_page_id,
                              landing_page_master_id = item.landing_page_master_id,
                              is_common = False,
                              created_date = item.created_date,
                              last_updated = item.last_updated,
                              site_id = item.site,
                              thanks_page_master_id = item.thanks_page_master_id,
                              folder_pdf_id = item.folder_pdf_id,
                              folder_thumb_id = item.folder_thumb_id,
                              hb_list_master_id = item.hb_list_master_id,
                              hb_list_name_default = item.hb_list_name_default,
                            ).save()
    obj_group_page_setting = SiteGroupPageSetting.objects.get(id=group_page_id)

    #4) Update lại giá trị
    date_now = datetime.now()
    SiteGroupPageSetting(
                          id=group_page_id,
                          group_name = group_name,
                          resource_top_page_id = resource_page_id,
                          landing_page_master_id = obj_group_page_setting.landing_page_master_id,
                          is_common = is_common,
                          created_date = obj_group_page_setting.created_date,
                          last_updated = date_now,
                          site_id = site_id,
                          thanks_page_master_id = obj_group_page_setting.thanks_page_master_id,
                          folder_pdf_id = folder_pdf_id,
                          folder_thumb_id = folder_thumb_id,
                          hb_list_master_id = hb_list_master_id,
                          hb_list_name_default = hb_list_name_default,
                          ).save()

    return HttpResponse(1)

def load_save_group_page_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    site_id = request.POST["site_id"]
    print("load_save_group_page_setting",site_id)
    #2) Laays ffolder hubspot
    dict_data_folder = HubspotHandleCMSFilesAPI(site_id).get_all_folder_type_dict()
    list_data_folder = []
    for i in dict_data_folder:
      list_data_folder.append(dict_data_folder[i])

    #2.1) lấy list hubspot list
    list_hb_list = HubspotHandleContactListsAPI(site_id).get_all_contact_lists()

    #2.2) lấy list_resource_page
    list_all_page = HubspotHandleCMSPageAPI(site_id).get_all_pages(is_draft=False)
    # list_resource_page = [i for i in list_all_page if "[accu]"  in i["name"]]
    list_resource_page = [i for i in list_all_page ]

    #Lấy list file templates name để chọn setting cho từng site
    
    #Xử lý foldẻ khi trả về
    def _append_child(data):
      data_return = {
        'id': data['id'],
        'text': data['name'],
        'items': [_append_child(child) for key_child,child in data['child'].items()],
      }
      return data_return

    list_data_folder_custom = [_append_child(root_value) for root_name,root_value in dict_data_folder.items()]
    #3) dữ liệu trả về  
    data = {
      "site_id" : site_id,
      "list_data_folder" : list_data_folder,
      "list_data_folder_custom" : list_data_folder_custom,
      "list_hb_list" : list_hb_list,
      "list_resource_page" : list_resource_page
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_group_page/modal-create-group-page-detail.html'

    return render(request, tmp_file_path, data)

def save_group_page_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    site_id = request.POST["site_id"]
    group_name = request.POST["group_name"]
    folder_thumb_id = request.POST["folder_thumb_id"]
    resource_page_id = request.POST["resource_page_id"]
    hb_list_master_id = request.POST["hb_list_master_id"]
    folder_pdf_id = request.POST["folder_pdf_id"]
    hb_list_name_default = request.POST["hb_list_name_default"]
    is_common = int(request.POST["is_common"])
    #2) Check group name tồn tại hay chưa

    if is_common == 1:
      is_common = True
    else:
      is_common = False

    list_obj_group_page_setting = SiteGroupPageSetting.objects.filter(group_name=group_name,is_active=1,site=site_id)
    group_name_exist = False
    print("is_common : ",is_common)
    if list_obj_group_page_setting:
      group_name_exist = True

    if group_name_exist:
      return HttpResponse(0)

    #3) check is_common
    if is_common:
      list_obj_group = SiteGroupPageSetting.objects.filter(site=site_id,is_active=1)
      for item in list_obj_group:
        #3.1) set lại các group thuộc site về is_common = False
        SiteGroupPageSetting(id=item.id,
                              group_name = item.group_name,
                              resource_top_page_id = item.resource_top_page_id,
                              landing_page_master_id = item.landing_page_master_id,
                              is_common = False,
                              created_date = item.created_date,
                              last_updated = item.last_updated,
                              site_id = item.site,
                              thanks_page_master_id = item.thanks_page_master_id,
                              folder_pdf_id = item.folder_pdf_id,
                              folder_thumb_id = item.folder_thumb_id,
                              hb_list_master_id = item.hb_list_master_id,
                              hb_list_name_default = item.hb_list_name_default,
                            ).save()

    #4) save mới giá trị
    date_now = datetime.now()
    SiteGroupPageSetting(
                          group_name = group_name,
                          resource_top_page_id = resource_page_id,
                          is_common = is_common,
                          created_date = date_now,
                          last_updated = date_now,
                          site_id = site_id,
                          folder_pdf_id = folder_pdf_id,
                          folder_thumb_id = folder_thumb_id,
                          hb_list_master_id = hb_list_master_id,
                          hb_list_name_default = hb_list_name_default,
                          ).save()

    return HttpResponse(1)



#============== SiteSettingGroupCTA ====================#
class SiteSettingGroupCTAView(PermissionRequiredMixin, ListView):
  model = SiteGroupCTASetting
  permission_required = ['f_1_2_sites.view_site']
  template_name = 'apps/f_1_2_sites/site_setting_group_cta.html'
  context_object_name = 'site_setting_group_cta'
  # ordering = ['name']

  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()
    list_sites = Site.objects.all()

    #3)Trả về
    data["list_sites"] = list_sites
    
    return data

  def get_queryset(self):
    #1)Dữ liệu
    qs = super().get_queryset()
    
    # #1.2)Dữ liệu từ request
    if self.kwargs['site_id']:
      param_site_id = int(self.kwargs['site_id'])
      
    else:
      return qs

    #2.1)Filter theo site
    if param_site_id != -1:
      qs = qs.filter(id=param_site_id)
    
    list_setting_cta_group = SiteGroupCTASetting.objects.filter(site_id=param_site_id,is_active=1)
    
    #3)Trả về
    data = {
            "site_id" : param_site_id,
            "list_setting_cta_group" : list_setting_cta_group
            }
    
    return data

class SiteSettingGroupCTADeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
  model = SiteGroupCTASetting
  permission_required = ['f_1_2_sites.delete_sitegroupctasetting']
  template_name = 'apps/f_1_2_sites/setting_group_cta/site_group_cta_delete.html'
  success_url = reverse_lazy('site_setting_group_cta')
  success_message = 'Delete Site Group CTA successed'

  def get_context_data(self, **kwargs):
    data = super().get_context_data()
    group_cta_id = self.kwargs['pk']
    obj_group_cta = SiteGroupCTASetting.objects.get(pk=group_cta_id)

    data["group_name"] = obj_group_cta.group_cta_name
    data['pk'] = group_cta_id
    # data["site_id"] = obj_group_page.site.id
    return data
    
  def delete(self, request, *args, **kwargs):
    group_cta_id = self.kwargs['pk']
    
    obj_group_cta = SiteGroupCTASetting.objects.get(pk=group_cta_id)
    site_group_cta_setting = SiteGroupCTASetting(
      id = group_cta_id,
      is_active= 0,
      site_id= obj_group_cta.site,
      created_date=obj_group_cta.created_date,
      last_updated= obj_group_cta.last_updated,
      group_cta_name= obj_group_cta.group_cta_name,
      cta_footer_setting = obj_group_cta.cta_footer_setting,
      cta_middle_setting = obj_group_cta.cta_middle_setting,
      cta_mobile_setting = obj_group_cta.cta_mobile_setting
    )

    site_group_cta_setting.save()
    messages.success(self.request, self.success_message)

    return HttpResponseRedirect(self.get_success_url())
      
  def get_success_url(self):
    
    obj_group_cta = SiteGroupCTASetting.objects.get(id=int(self.kwargs['pk']))
    site_id = obj_group_cta.site.id
    
    return reverse("site_setting_group_cta", args=(site_id,)) 

class SiteGroupCTADeleteBulkView(SuccessMessageMixin, PermissionRequiredMixin, View):
  model = SiteGroupCTASetting
  permission_required = ['f_1_2_sites.delete_sitegroupctasetting']
  template_name = 'apps/f_1_2_sites/setting_group_cta/site_group_cta_delete.html'
  #success_url = reverse_lazy('site_list')

  def post(self, request):
    #1)Dữ liệu
    list_id = self.request.POST['list_id'].split(',')

    #2)Xử lý, Ko xóa mà chỉ có inactive nó thôi
    SiteGroupCTASetting.objects.filter(pk__in=list_id).update(is_active=0)

    return HttpResponse(1)

  def get_success_url(self):
    obj_group_cta = SiteGroupCTASetting.objects.get(pk=self.kwargs['pk'])
    site_id = obj_group_cta.site.id
    return reverse("modal_site_group_cta_delete_bulk", args=(site_id,))

def load_save_group_cta_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    site_id = request.POST["site_id"]
    print("load_save_group_cta_setting",site_id)
    #2) Laays ffolder hubspot
    dict_data_folder = HubspotHandleCMSFilesAPI(site_id).get_all_folder_type_dict()
    list_data_folder = []
    for i in dict_data_folder:
      list_data_folder.append(dict_data_folder[i])

    #Lấy list file templates name để chọn setting cho từng site
    list_templates_middle_cta = []
    list_templates_footer_cta = []
    list_templates_mobile_cta = []
    list_templates_sidebar_cta = []
    
    for i in os.listdir(str(settings.BASE_DIR) + '/templates/apps/f_3_2_cta_management/cta_templates/layout/footer'):
      if i.endswith(".html"): 
        list_templates_footer_cta.append(i)

    for i in os.listdir(str(settings.BASE_DIR) + '/templates/apps/f_3_2_cta_management/cta_templates/layout/middle'):
      if i.endswith(".html"): 
        list_templates_middle_cta.append(i)

    for i in os.listdir(str(settings.BASE_DIR) + '/templates/apps/f_3_2_cta_management/cta_templates/layout/mobile'):
      if i.endswith(".html"): 
        list_templates_mobile_cta.append(i)

    for i in os.listdir(str(settings.BASE_DIR) + '/templates/apps/f_3_2_cta_management/cta_templates/layout/sidebar'):
      if i.endswith(".html"): 
        list_templates_sidebar_cta.append(i)    

    #Xử lý foldẻ khi trả về
    def _append_child(data):
      data_return = {
        'id': data['id'],
        'text': data['name'],
        'items': [_append_child(child) for key_child,child in data['child'].items()],
      }
      return data_return

    list_data_folder_custom = [_append_child(root_value) for root_name,root_value in dict_data_folder.items()]
    #3) dữ liệu trả về  
    data = {
      "site_id" : site_id,
      "list_templates_middle_cta" : list_templates_middle_cta,
      "list_templates_footer_cta" : list_templates_footer_cta,
      "list_templates_mobile_cta" : list_templates_mobile_cta,
      "list_templates_sidebar_cta" : list_templates_sidebar_cta,
      "list_data_folder" : list_data_folder,
      "list_data_folder_custom" : list_data_folder_custom,
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_group_cta/modal-create-group-cta-detail.html'

    return render(request, tmp_file_path, data)

def save_group_cta_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    site_id = request.POST["site_id"]
    group_name = request.POST["group_name"]
    folder_cta_id = request.POST["folder_cta_id"]
    cta_templates_middle = request.POST["cta_templates_middle"]
    cta_templates_footer = request.POST["cta_templates_footer"]
    cta_templates_mobile = request.POST["cta_templates_mobile"]
    cta_templates_sidebar = request.POST["cta_templates_sidebar"]
    cta_templates_footer = "apps/f_3_2_cta_management/cta_templates/layout/footer/" + cta_templates_footer
    cta_templates_middle = "apps/f_3_2_cta_management/cta_templates/layout/middle/" + cta_templates_middle
    cta_templates_mobile = "apps/f_3_2_cta_management/cta_templates/layout/mobile/" + cta_templates_mobile
    if cta_templates_sidebar != "":
      cta_templates_sidebar = "apps/f_3_2_cta_management/cta_templates/layout/sidebar/" + cta_templates_sidebar

    mobile_text_font_size = request.POST["mobile_text_font_size"]
    mobile_text_margin = request.POST["mobile_text_margin"]
    mobile_provider_font_size = request.POST["mobile_provider_font_size"]
    mobile_title_margin = request.POST["mobile_title_margin"]
    mobile_title_font_size = request.POST["mobile_title_font_size"]
    mobile_title_line_height = request.POST["mobile_title_line_height"]
    mobile_text_line_height = request.POST["mobile_text_line_height"]

    sidebar_text_font_size = request.POST["sidebar_text_font_size"]
    sidebar_text_margin = request.POST["sidebar_text_margin"]
    sidebar_provider_font_size = request.POST["sidebar_provider_font_size"]
    sidebar_title_margin = request.POST["sidebar_title_margin"]
    sidebar_title_font_size = request.POST["sidebar_title_font_size"]
    sidebar_title_line_height = request.POST["sidebar_title_line_height"]
    sidebar_text_line_height = request.POST["sidebar_text_line_height"]

    footer_text_font_size = request.POST["footer_text_font_size"]
    footer_text_margin = request.POST["footer_text_margin"]
    footer_provider_font_size = request.POST["footer_provider_font_size"]
    footer_title_margin = request.POST["footer_title_margin"]
    footer_title_font_size = request.POST["footer_title_font_size"]
    footer_title_line_height = request.POST["footer_title_line_height"]
    footer_text_line_height = request.POST["footer_text_line_height"]

    middle_text_font_size = request.POST["middle_text_font_size"]
    middle_text_margin = request.POST["middle_text_margin"]
    middle_provider_font_size = request.POST["middle_provider_font_size"]
    middle_title_margin = request.POST["middle_title_margin"]
    middle_title_font_size = request.POST["middle_title_font_size"]
    is_fixed_line_middle = request.POST["is_fixed_line_middle"]
    middle_title_line_height = request.POST["middle_title_line_height"]
    middle_text_line_height = request.POST["middle_text_line_height"]
    
    if int(is_fixed_line_middle) == 0:
      is_fixed_line_middle = False
    else:
      is_fixed_line_middle = True 

    #2) Check group name tồn tại hay chưa

    list_obj_group_cta_setting = SiteGroupCTASetting.objects.filter(group_cta_name=group_name,is_active=1,site=site_id)
    group_name_exist = False
    
    if list_obj_group_cta_setting:
      group_name_exist = True

    if group_name_exist:
      return HttpResponse(0)

    #3) chuyển dữ liệu lưu file thành dict
    dict_setting_footer = {
      "template_file" : cta_templates_footer,
      "title" : {"font_size" : int(footer_title_font_size),"margin_top":int(footer_title_margin),"line_height":int(footer_title_line_height)},
      "text" : {"font_size" : int(footer_text_font_size),"margin_top":int(footer_text_margin),"line_height":int(footer_text_line_height)},
      "provider" : {"font_size" : int(footer_provider_font_size)}
    }

    dict_setting_middle = {
      "template_file" : cta_templates_middle,
      "title" : {"font_size" : int(middle_title_font_size),"margin_top":int(middle_title_margin),"line_height":int(middle_title_line_height)},
      "text" : {"font_size" : int(middle_text_font_size),"margin_top":int(middle_text_margin),"line_height":int(middle_text_line_height)},
      "provider" : {"font_size" : int(middle_provider_font_size)},
      "is_fixed_line_middle" : is_fixed_line_middle
    }

    dict_setting_mobile = {
      "template_file" : cta_templates_mobile,
      "title" : {"font_size" : int(mobile_title_font_size),"margin_top":int(mobile_title_margin),"line_height":int(mobile_title_line_height)},
      "text" : {"font_size" : int(mobile_text_font_size),"margin_top":int(mobile_text_margin),"line_height":int(mobile_text_line_height)},
      "provider" : {"font_size" : int(mobile_provider_font_size)}
    }

    dict_setting_sidebar = {
      "template_file" : cta_templates_sidebar,
      "title" : {"font_size" : int(sidebar_title_font_size),"margin_top":int(sidebar_title_margin),"line_height":int(sidebar_title_line_height)},
      "text" : {"font_size" : int(sidebar_text_font_size),"margin_top":int(sidebar_text_margin),"line_height":int(sidebar_text_line_height)},
      "provider" : {"font_size" : int(sidebar_provider_font_size)}
    }

    #4) save mới giá trị
    date_now = datetime.now()
    SiteGroupCTASetting(
                          group_cta_name = group_name,
                          created_date = date_now,
                          last_updated = date_now,
                          site_id = site_id,
                          folder_cta_id = folder_cta_id,
                          cta_footer_setting = json.dumps(dict_setting_footer),
                          cta_middle_setting = json.dumps(dict_setting_middle),
                          cta_mobile_setting = json.dumps(dict_setting_mobile),
                          cta_sidebar_setting = json.dumps(dict_setting_sidebar)
                          ).save()

    return HttpResponse(1)

def load_update_group_cta_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    group_cta_id = request.POST["group_cta_id"]
    obj_group_cta = SiteGroupCTASetting.objects.get(pk=group_cta_id)

    dict_cta_footer_setting = json.loads(obj_group_cta.cta_footer_setting)
    dict_cta_middle_setting = json.loads(obj_group_cta.cta_middle_setting)
  
    if not dict_cta_middle_setting.get("is_fixed_line_middle"):
      dict_cta_middle_setting["is_fixed_line_middle"] = 0
    else:
      dict_cta_middle_setting["is_fixed_line_middle"] = 0 if dict_cta_middle_setting["is_fixed_line_middle"] =="False" else 1

    if not dict_cta_middle_setting["title"].get("line_height"):
      dict_cta_middle_setting["title"]["line_height"] = 24

    if not dict_cta_middle_setting["text"].get("line_height"):
      dict_cta_middle_setting["text"]["line_height"] = 24  

    if not dict_cta_footer_setting["title"].get("line_height"):
      dict_cta_footer_setting["title"]["line_height"] = 24

    if not dict_cta_footer_setting["text"].get("line_height"):
      dict_cta_footer_setting["text"]["line_height"] = 24 

    dict_cta_mobile_setting = json.loads(obj_group_cta.cta_mobile_setting)
    if not dict_cta_mobile_setting["title"].get("line_height"):
      dict_cta_mobile_setting["title"]["line_height"] = 24

    if not dict_cta_mobile_setting["text"].get("line_height"):
      dict_cta_mobile_setting["text"]["line_height"] = 24 

    dict_cta_sidebar_setting = json.loads(obj_group_cta.cta_sidebar_setting)
    #1.1)Xử lý sidebar cta cho những site không dùng hoặc chưa setting
    
    if not dict_cta_sidebar_setting :
      template_sidebar = ""
      font_size_title = 0
      text_font_size_title = 0
      line_height_title = 24
      line_height_text = 24
      title_margin_top = 0
      text_margin_top = 0
      provider_font_size = 0
      dict_cta_sidebar_setting = {"template_file":template_sidebar,
                                  "title" : {
                                    "font_size" : font_size_title,
                                    "margin_top" : title_margin_top,
                                    "line_height" : line_height_title
                                  },
                                  "text" : {
                                    "font_size" : text_font_size_title,
                                    "margin_top" : text_margin_top,
                                    "line_height" : line_height_text
                                  },
                                  "provider" : {
                                    "font_size" : provider_font_size
                                  }
                                 }
      obj_group_cta.cta_sidebar_setting = dict_cta_sidebar_setting                    
      
    else:
      template_sidebar = dict_cta_sidebar_setting["template_file"]
      index_sidebar = template_sidebar.rfind("/")
      template_sidebar = template_sidebar[index_sidebar + 1:]
      dict_cta_sidebar_setting["template_file"] = template_sidebar
      if not dict_cta_sidebar_setting["title"].get("line_height"):
        dict_cta_sidebar_setting["title"]["line_height"] = 24

      if not dict_cta_sidebar_setting["text"].get("line_height"):
        dict_cta_sidebar_setting["text"]["line_height"] = 24

      obj_group_cta.cta_sidebar_setting = dict_cta_sidebar_setting
    
    

    template_footer = dict_cta_footer_setting["template_file"]
    index_footer = template_footer.rfind("/")
    template_footer = template_footer[index_footer + 1:]
    dict_cta_footer_setting["template_file"] = template_footer

    obj_group_cta.cta_footer_setting = dict_cta_footer_setting

    template_middle = dict_cta_middle_setting["template_file"]
    index_middle = template_middle.rfind("/")
    template_middle = template_middle[index_middle + 1:]
    dict_cta_middle_setting["template_file"] = template_middle
    obj_group_cta.cta_middle_setting = dict_cta_middle_setting
    
    template_mobile = dict_cta_mobile_setting["template_file"]
    index_mobile = template_mobile.rfind("/")
    template_mobile = template_mobile[index_mobile + 1:]
    dict_cta_mobile_setting["template_file"] = template_mobile
    obj_group_cta.cta_mobile_setting = dict_cta_mobile_setting

    site_id = obj_group_cta.site.id

    list_data_folder = []

    dict_data_folder_info = HubspotHandleCMSFilesAPI(site_id).get_all_folder_to_dict_key_id()
    
    name_folder_cta = ""

    if obj_group_cta.folder_cta_id != "":
      name_folder_cta = dict_data_folder_info[int(obj_group_cta.folder_cta_id)]["name"]

    #Lấy list file templates name để chọn setting cho từng site
    list_templates_middle_cta = []
    list_templates_footer_cta = []
    list_templates_mobile_cta = []
    list_templates_sidebar_cta = []
    
    for i in os.listdir(str(settings.BASE_DIR) + '/templates/apps/f_3_2_cta_management/cta_templates/layout/footer'):
      if i.endswith(".html"): 
        list_templates_footer_cta.append(i)

    for i in os.listdir(str(settings.BASE_DIR) + '/templates/apps/f_3_2_cta_management/cta_templates/layout/middle'):
      if i.endswith(".html"): 
        list_templates_middle_cta.append(i)

    for i in os.listdir(str(settings.BASE_DIR) + '/templates/apps/f_3_2_cta_management/cta_templates/layout/mobile'):
      if i.endswith(".html"): 
        list_templates_mobile_cta.append(i)

    for i in os.listdir(str(settings.BASE_DIR) + '/templates/apps/f_3_2_cta_management/cta_templates/layout/sidebar'):
      if i.endswith(".html"): 
        list_templates_sidebar_cta.append(i)    

    #2) Laays ffolder hubspot
    dict_data_folder = HubspotHandleCMSFilesAPI(site_id).get_all_folder_type_dict()
    
    for i in dict_data_folder:
      list_data_folder.append(dict_data_folder[i])

    
    def _append_child(data):
      data_return = {
        'id': data['id'],
        'text': data['name'],
        'items': [_append_child(child) for key_child,child in data['child'].items()],
      }
      return data_return

    list_data_folder_custom = [_append_child(root_value) for root_name,root_value in dict_data_folder.items()]
    
    #3) dữ liệu trả về  
    data = {
      "obj_group_cta" : obj_group_cta,
      "name_folder_cta" : name_folder_cta,
      "list_data_folder" : list_data_folder,
      "list_templates_middle_cta" : list_templates_middle_cta,
      "list_templates_footer_cta" : list_templates_footer_cta,
      "list_templates_mobile_cta" : list_templates_mobile_cta,
      "list_templates_sidebar_cta" : list_templates_sidebar_cta,
      "list_data_folder_custom" : list_data_folder_custom,
    }
    tmp_file_path = 'apps/f_1_2_sites/setting_group_cta/modal-update-group-cta-detail.html'

    return render(request, tmp_file_path, data)

def save_update_group_cta_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    
    group_cta_id = int(request.POST["group_cta_id"])
    site_id = request.POST["site_id"]
    group_name = request.POST["group_name"]
    folder_cta_id = request.POST["folder_cta_id"]
    cta_templates_middle = request.POST["cta_templates_middle"]
    cta_templates_footer = request.POST["cta_templates_footer"]
    cta_templates_mobile = request.POST["cta_templates_mobile"]
    cta_templates_sidebar = request.POST["cta_templates_sidebar"]

    if cta_templates_sidebar != "":
      cta_templates_sidebar = "apps/f_3_2_cta_management/cta_templates/layout/sidebar/" + cta_templates_sidebar

    cta_templates_footer = "apps/f_3_2_cta_management/cta_templates/layout/footer/" + cta_templates_footer
    cta_templates_middle = "apps/f_3_2_cta_management/cta_templates/layout/middle/" + cta_templates_middle
    cta_templates_mobile = "apps/f_3_2_cta_management/cta_templates/layout/mobile/" + cta_templates_mobile

    mobile_text_font_size = request.POST["mobile_text_font_size"]
    mobile_text_margin = request.POST["mobile_text_margin"]
    mobile_provider_font_size = request.POST["mobile_provider_font_size"]
    mobile_title_margin = request.POST["mobile_title_margin"]
    mobile_title_font_size = request.POST["mobile_title_font_size"]
    mobile_title_line_heigh = request.POST["mobile_title_line_heigh"]
    mobile_text_line_heigh = request.POST["mobile_text_line_heigh"]

    sidebar_text_font_size = request.POST["sidebar_text_font_size"]
    sidebar_text_margin = request.POST["sidebar_text_margin"]
    sidebar_provider_font_size = request.POST["sidebar_provider_font_size"]
    sidebar_title_margin = request.POST["sidebar_title_margin"]
    sidebar_title_font_size = request.POST["sidebar_title_font_size"]
    sidebar_title_line_heigh = request.POST["sidebar_title_line_heigh"]
    sidebar_text_line_heigh = request.POST["sidebar_text_line_heigh"]

    footer_text_font_size = request.POST["footer_text_font_size"]
    footer_text_margin = request.POST["footer_text_margin"]
    footer_provider_font_size = request.POST["footer_provider_font_size"]
    footer_title_margin = request.POST["footer_title_margin"]
    footer_title_font_size = request.POST["footer_title_font_size"]
    footer_title_line_heigh = request.POST["footer_title_line_heigh"]
    footer_text_line_heigh = request.POST["footer_text_line_heigh"]

    middle_text_font_size = request.POST["middle_text_font_size"]
    middle_text_margin = request.POST["middle_text_margin"]
    middle_provider_font_size = request.POST["middle_provider_font_size"]
    middle_title_margin = request.POST["middle_title_margin"]
    middle_title_font_size = request.POST["middle_title_font_size"]
    is_fixed_line_middle = request.POST["is_fixed_line_middle"]
    middle_title_line_heigh = request.POST["middle_title_line_heigh"]
    middle_text_line_heigh = request.POST["middle_text_line_heigh"]
    print(is_fixed_line_middle,"is_fixed_line_middle")
    if int(is_fixed_line_middle) == 0:
      is_fixed_line_middle = False
    else:
      is_fixed_line_middle = True 

    #2) Check group name tồn tại hay chưa

    list_obj_group_cta_setting_update = SiteGroupCTASetting.objects.filter(group_cta_name=group_name,is_active=1,site=site_id)
    group_name_exist = False

    for item in list_obj_group_cta_setting_update:
      if item.id != group_cta_id:
        group_name_exist = True

    if group_name_exist:
      return HttpResponse(0)

    #3) chuyển dữ liệu lưu file thành dict
    dict_setting_footer = {
      "template_file" : cta_templates_footer,
      "title" : {"font_size" : int(footer_title_font_size),"margin_top":int(footer_title_margin),"line_height":int(footer_title_line_heigh)},
      "text" : {"font_size" : int(footer_text_font_size),"margin_top":int(footer_text_margin),"line_height":int(footer_text_line_heigh)},
      "provider" : {"font_size" : int(footer_provider_font_size)}
    }

    dict_setting_middle = {
      "template_file" : cta_templates_middle,
      "title" : {"font_size" : int(middle_title_font_size),"margin_top":int(middle_title_margin),"line_height":int(middle_title_line_heigh)},
      "text" : {"font_size" : int(middle_text_font_size),"margin_top":int(middle_text_margin),"line_height":int(middle_text_line_heigh)},
      "provider" : {"font_size" : int(middle_provider_font_size)},
      "is_fixed_line_middle" : is_fixed_line_middle
    }

    dict_setting_mobile = {
      "template_file" : cta_templates_mobile,
      "title" : {"font_size" : int(mobile_title_font_size),"margin_top":int(mobile_title_margin),"line_height":int(mobile_title_line_heigh)},
      "text" : {"font_size" : int(mobile_text_font_size),"margin_top":int(mobile_text_margin),"line_height":int(mobile_text_line_heigh)},
      "provider" : {"font_size" : int(mobile_provider_font_size)}
    }

    dict_setting_sidebar = {
      "template_file" : cta_templates_sidebar,
      "title" : {"font_size" : int(sidebar_title_font_size),"margin_top":int(sidebar_title_margin) ,"line_height":int(sidebar_title_line_heigh)},
      "text" : {"font_size" : int(sidebar_text_font_size),"margin_top":int(sidebar_text_margin),"line_height":int(sidebar_text_line_heigh)},
      "provider" : {"font_size" : int(sidebar_provider_font_size)}
    }
    
    #4) save mới giá trị
    date_now = datetime.now()
    obj_group_cta = SiteGroupCTASetting.objects.get(id=group_cta_id)
    SiteGroupCTASetting(  id = group_cta_id,
                          group_cta_name = group_name,
                          created_date = obj_group_cta.created_date,
                          last_updated = date_now,
                          site_id = site_id,
                          folder_cta_id = folder_cta_id,
                          cta_footer_setting = json.dumps(dict_setting_footer),
                          cta_middle_setting = json.dumps(dict_setting_middle),
                          cta_mobile_setting = json.dumps(dict_setting_mobile),
                          cta_sidebar_setting = json.dumps(dict_setting_sidebar)
                          ).save()

    return HttpResponse(1)

def test(request):
  site_id = 560035
  folder_id = 38490056682
  dict_folder_info = HubspotHandleCMSFilesAPI(site_id).get_all_folder_to_dict_key_id()
  data = dict_folder_info.get(folder_id)

  return HttpResponse(json.dumps(data))
from __Config.Include.Common_Include import *
from f_1_1_customers.models import Customer, CustomerGroup
from f_1_2_sites.models import Site, SiteAuth
from f_7_1_accounts.models import AccountUserSession
from f_7_1_accounts.authentication import utils

class SelectFunctionMSView(TemplateView):
  template_name = 'apps/f_7_2_pages/select_function_ms.html'

class SelectFunctionView(TemplateView):
  template_name = 'apps/f_7_2_pages/select_function.html'

  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()
    param_customer_id = self.kwargs['customer_id']
    param_site_id = self.kwargs['site_id']

    data['customer_id'] = param_customer_id
    data['site_id'] = param_site_id

    return data

class AfterSelectSiteView(View):
  def get(self, request, *args, **kwargs):
    site_id = kwargs['site_id']
    request.session['site_id'] = site_id
    list_customers = Customer.objects.filter(user=self.request.user.id)
    list_sites = Site.objects.filter(customer__in=list_customers)
    return redirect(reverse_lazy('select_function',args=(request.session['customer_id'], request.session['site_id'])))

class SelectSiteView(ListView):
  model = Site
  template_name = 'apps/f_7_2_pages/select_site.html'
  context_object_name = "list_sites"

  def get(self, request, *args, **kwargs):
    try:
      customer = Customer.objects.get(id=self.request.session['customer_id'])
      list_sites = Site.objects.filter(customer=customer)
      
    except Customer.DoesNotExist:
      list_sites = []

    if len(list_sites) == 1:
      return redirect(reverse_lazy('after_select_site',args=(list_sites[0].id,)))
      
    return super().get(request, args, kwargs)

  def get_queryset(self):
    customer = Customer.objects.get(id=self.request.session['customer_id'])
    list_sites = Site.objects.filter(customer=customer)
    return list_sites

class SelectCustomerView(ListView):
  model = Customer
  template_name = 'apps/f_7_2_pages/select_customer.html'
  context_object_name = "list_customers"

  def get(self, request, *args, **kwargs):
    try:

      is_ms_group = utils.check_ms_group(request.user)
      if is_ms_group:
        return redirect(reverse_lazy("select_function_ms"))

      customers = Customer().get_activate_customers_by_user(user_id=self.request.user.id)
      
      if len(customers) == 1:
        request.session['customer_id'] = customers[0].pk
        request.session['customer_name'] = customers[0].name
        request.session['customer_multi'] = False

        list_sites = customers[0].site.all()
        if len(list_sites) > 0:
          request.session['site_id'] = list_sites[0].pk

        return redirect(reverse_lazy('home'))

    except Customer.DoesNotExist:


      customers = []
      
    return super().get(request, args, kwargs)


  def get_queryset(self):
    list_customers = Customer.objects.filter(user=self.request.user)

    #Loop qua 1 vòng các customer
    for customer in list_customers:

      #Lấy main_chanel
      setattr(customer, "main_chanel_name", None)
      for customer_setting in customer.customersetting_set.all():
        if customer_setting.is_main_channel:
          setattr(customer, "main_chanel_name", customer_setting.site.name)
          break
      
      #Lấy trạng thai hợp đồng
      status = None
      options = []
      for contract in customer.customercontract_set.all():
        if contract and  contract.end_date and  contract.start_date:
          options = contract.option.all()

          setattr(customer,"plan_name", contract.plan.name)

          if datetime.now().date() > contract.end_date and int( (datetime.now().date() - contract.end_date).days) <= 14:
            # print("customer : ", customer.code, " số ngày  ", int( (contract.end_date - datetime.now().date()).days) , contract.end_date)
            status = '終了'

            #Đang sử dụng
          elif contract.start_date <= datetime.now().date() and contract.end_date >= datetime.now().date():
            status = '契約中'
            #Khi bắt đc hợp đồng đnag sử dụng thì đặt cách cho break
            break


      setattr(customer,"status", status)

      #Lấy option
      option_name = []
      for i in options:
        option_name.append(i.name)

      setattr(customer,"options_name", option_name)
      

    #Chỉ lấy các customer đang chạy hợp đồng và quá hạn k tới 14 ngày
    _list_customers = list(filter(lambda x: (x.status == "契約中" or x.status == "終了" ) , list_customers))

    return _list_customers
  
class HomeView(View):
  def get(self, request, *args, **kwargs):
    if not request.user.id :
      return redirect(reverse_lazy('login'))
    elif request.user.is_superuser:
      return redirect('home')
    else:
      return redirect(reverse_lazy("select_site"))
class AfterSelectAccountView(View):
  def get(self, request, *args, **kwargs):
    #1)Lưu customer id vào session
    if request.user.id:

      customer_id = self.kwargs.get('customer_id')
      list_customers = Customer.objects.filter(user=request.user, id=customer_id)
      
      if len(list_customers) > 0:
        request.session['customer_id'] = list_customers[0].pk
        request.session['customer_name'] = list_customers[0].name
        request.session['customer_multi'] = True

        list_sites = list_customers[0].site.all()
        if len(list_sites) > 0:
          request.session['site_id'] = list_sites[0].pk
      
      #trường hợp không có account nào
      else:
        return redirect(reverse_lazy("select_customer"))

    #2)Điều hướng
    return redirect(reverse_lazy('home'))
class AuthView(TemplateView):
  template_name = 'apps/f_7_2_pages/auth.html'
  def get_context_data(self, *args, **kwargs):
    #1)Dữ liệu
    context = super().get_context_data(*args, **kwargs)
    site_id = kwargs['site_id']
    site = Site.objects.get(pk=site_id)

    #2)Xử lý
    #2.1)Lấy phần authen trong DB
    site_auth = SiteAuth.objects.filter(site=site)
    if not site_auth:
      site_auth = SiteAuth(site=site)
      site_auth.save()
    else:
      site_auth = site_auth[0]
    
    #2.2)Xử lý đường link authen
    hb_auth_link = HubspotAPIAuth(site.pk).create_auth_url()
    ga_auth_link = GAAPIAuth(site.pk).create_auth_url()
    gsc_auth_link = GSCAPIAuth(site.pk).create_auth_url()
    
    site_auth = SiteAuth.objects.get(site=site)
    #3)Trả về
    context ['site_auth'] = site_auth
    context ['hb_auth_link'] = hb_auth_link
    context ['ga_auth_link'] = ga_auth_link
    context ['gsc_auth_link'] = gsc_auth_link
    return context 

class AuthHubView(View):
  def get(self, request):
    #1)Dữ liệu
    #1.1)Request
    param_site_id = request.GET["site_id"]
    param_code = request.GET["code"]

    #2)Xử lý
    #2.1)Authen GA
    token_info = HubspotAPIAuth(param_site_id).call_api_get_access_token(param_code)

    #2.2)Lưu vào DB
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    access_token_info = HubspotAPIAuth(param_site_id).get_access_token_info(access_token)
    hub_id = access_token_info.get("hub_id","-1")
    print("hub_id : ",hub_id)
    site_auth = SiteAuth.objects.get(site=param_site_id)
    site_auth.last_hub_refresh_token = refresh_token
    site_auth.hub_id = hub_id
    site_auth.save()
    return redirect(reverse('auth',args=(param_site_id,)))

class AuthGAView(View):
  def get(self, request):
    #1)Dữ liệu
    #1.1)Request
    param_site_id = request.GET["state"]
    param_code = request.GET["code"]

    #2)Xử lý
    #2.1)Authen GA
    token_info = GAAPIAuth(param_site_id).call_api_get_access_token(param_code)

    #2.2)Lưu vào DB
    # access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    site_auth = SiteAuth.objects.get(site=param_site_id)
    site_auth.last_ga_refresh_token = refresh_token
    site_auth.save()
    return redirect(reverse('auth',args=(param_site_id,)))

class AuthGSCView(View):
  def get(self, request):
    #1)Dữ liệu
    #1.1)Request
    param_site_id = request.GET["state"]
    param_code = request.GET["code"]

    #2)Xử lý
    #2.1)Authen GA
    token_info = GSCAPIAuth(param_site_id).call_api_get_access_token(param_code)

    #2.2)Lưu vào DB
    # access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    site_auth = SiteAuth.objects.get(site=param_site_id)
    site_auth.last_gsc_refresh_token = refresh_token
    site_auth.save()
    return redirect(reverse('auth',args=(param_site_id,)))

class SelectGroupView(ListView):
  model = CustomerGroup
  template_name = 'apps/f_7_2_pages/select_group.html'
  context_object_name = "list_groups"

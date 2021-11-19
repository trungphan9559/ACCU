from urllib import request
from __Config.Include.Common_Include import *
from f_1_1_customers.models import *
from f_1_1_customers.forms import *
from f_1_2_sites.models import SiteAuth,Site
from f_1_1_customers.until import draw_excel

# Create your views here.

class CustomerCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView): 
  form_class = CustomerCreateForm
  permission_required = ['f_1_1_customers.add_customer']
  template_name = 'apps/f_1_1_customers/customer/customer_create.html'
  success_url = reverse_lazy('customer_create')
  success_message = '「%(name)s」顧客 が作成されました。'

  def get_success_url(self):
    return f"{reverse_lazy('customer_create')}?group={self.group_id}"

  def get_form(self, form_class=None):
    #1)Lấy dữ liệu
    form = super().get_form(form_class)
    param_group_id = self.request.GET.get('group','-1')
    if str(param_group_id) != '-1':
      customer_group = CustomerGroup.objects.get(pk=param_group_id)
      list_sites = customer_group.site.all()
    else:
      list_sites = Site.objects.all()

    #2)Tạo code mặc định
    form.fields['id'].widget = forms.HiddenInput()
    form.fields['id'].initial  = random.randint(100000,999999)

    form.fields['customer_group'].initial  = param_group_id

    form.fields['site'].choices = ([(site.id, site.name) for site in list_sites])
    form.fields['site'].widget = forms.CheckboxSelectMultiple()
    form.fields['exclude_email'].widget = forms.TextInput()
    form.fields['email_domain'].widget = forms.TextInput()
    return form

  def form_valid(self, form):
    self.group_id = form.cleaned_data['customer_group'].id
    while Customer.objects.filter(id=form.instance.id):
      form.instance.id = random.randint(100000,999999)

    form.instance.exclude_email = json.dumps(form.instance.exclude_email.split(','))
    form.instance.email_domain = json.dumps(form.instance.email_domain.split(','))

    return super().form_valid(form)
        
class CustomerListView(PermissionRequiredMixin,ListView):
  model = Customer
  permission_required = ['f_1_1_customers.view_customer']
  template_name = 'apps/f_1_1_customers/customer/customer_list.html'
  context_object_name = 'list_customers'
  ordering = ['name']


  def get_queryset(self):

    #1.1)Dữ liệu từ request
    plan_id = int(self.request.GET.get('plan',-1))
    option_id = int(self.request.GET.get('option',-1))
    status = int(self.request.GET.get('status',-1))

    site_id = int(self.request.GET.get('site',-1))

    #Cái này chỉ có ở màn hinh list customer đi vào
    customer_id = self.request.GET.get('customer_id',-1)
    list_customers = Customer().filter_customers(site_id, status, plan_id, option_id, customer_id)

    return list_customers


  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()
    customer_group_id = self.request.GET.get('group')

    #2)Xử lý
    list_customer_groups = CustomerGroup.objects.all()

    try:
      customer_group = CustomerGroup.objects.get(pk=customer_group_id)
      list_plans = CustomerGroupPlanOption.objects.filter(customer_group=customer_group,type='plan').order_by('sort')
    except CustomerGroup.DoesNotExist:
      list_plans = []

    try:
      customer_group = CustomerGroup.objects.get(pk=customer_group_id)
      list_options = CustomerGroupPlanOption.objects.filter(customer_group=customer_group,type='option').order_by('sort')
    except CustomerGroup.DoesNotExist:
      list_options = []

    try:
      if customer_group_id != -1:
        customer_group = CustomerGroup.objects.get(pk=customer_group_id)
        list_sites = customer_group.site.all()
      else:
        print("trungggggg,,,,,")
        list_sites = Site.objects.all()
    except CustomerGroup.DoesNotExist:
      list_sites = []
      
  
    #3)Trả về
    data['list_customer_groups'] = list_customer_groups
    data['list_plans'] = list_plans
    data['list_options'] = list_options
    data['list_sites'] = list_sites
    return data

class CustomerDetailView(PermissionRequiredMixin,DetailView):
    model = Customer
    permission_required = ['f_1_1_customers.view_customer']
    template_name = 'apps/f_1_1_customers/customer/customer_detail.html'

class CustomerUpdateView(SuccessMessageMixin, PermissionRequiredMixin, UpdateView): 
  model = Customer
  permission_required = ['f_1_1_customers.change_customer']
  template_name = 'apps/f_1_1_customers/customer/customer_update.html'
  fields = ['name', 'domain', 'site', 'customer_group', 'exclude_email', 'email_domain', 'is_prioritize', 'is_active']
  success_message = 'Update %(name)s successed'

  def get_initial(self, *args, **kwargs):
    initial = super().get_initial()
    customer_id = self.kwargs['pk']
    customer_obj = Customer.objects.get(id = customer_id)
    customer_exclude_email = json.loads(customer_obj.exclude_email)
    initial["exclude_email"] =  ",".join(customer_exclude_email)
    customer_email_domain = json.loads(customer_obj.email_domain)
    initial["email_domain"] =  ",".join(customer_email_domain)
    return initial

  def get_form(self, form_class=None):
    form = super().get_form(form_class) 

    customer_id = self.kwargs['pk']
    customer_obj = Customer.objects.get(id = customer_id)
    param_group_id = customer_obj.customer_group_id
    
    if param_group_id != -1:
      customer_group = CustomerGroup.objects.get(pk=param_group_id)
      list_sites = customer_group.site.all()
    else:
      list_sites = Site.objects.all()

    # form.fields['name'].disabled = True
    # form.fields['domain'].disabled = True
    form.fields['customer_group'].disabled = True
    form.fields['site'].choices = ([(site.id, site.name) for site in list_sites])
    form.fields['site'].widget = forms.CheckboxSelectMultiple()

    form.fields['exclude_email'].widget = forms.TextInput()
    form.fields['email_domain'].widget = forms.TextInput()

    return form

  def form_valid(self, form):
    form.instance.exclude_email = json.dumps(form.instance.exclude_email.split(','))
    form.instance.email_domain = json.dumps(form.instance.email_domain.split(','))

    return super().form_valid(form)

  def get_success_url(self):
    return reverse("customer_update", args=(self.kwargs['pk'],))  

class CustomerDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
  model = Customer
  permission_required = ['f_1_1_customers.delete_customer']
  template_name = 'apps/f_1_1_customers/customer/customer_delete.html'
  success_url = reverse_lazy('customer_list')
  success_message = 'Delete Customer successed'

  def delete(self, request, *args, **kwargs):
    messages.success(self.request, self.success_message)
    return super().delete(request, *args, **kwargs)

class CustomerDeleteBulkView(SuccessMessageMixin, PermissionRequiredMixin, View): 
  permission_required = ['f_1_1_customers.delete_customer']

  def post(self, request):
    #1)Dữ liệu
    list_id = self.request.POST['list_id'].split(',')

    #2)Xử lý
    Customer.objects.filter(pk__in=list_id).delete()

    return HttpResponse(1)


########################################################################################

###############################        Contract     ####################################

########################################################################################


class CustomerContractCreateView(SuccessMessageMixin, PermissionRequiredMixin, CreateView): 
  model = CustomerContract
  permission_required = ['f_1_1_customers.add_customercontract']
  template_name = 'apps/f_1_1_customers/customer_contract/customer_contract_create.html'
  fields = ['customer',"payment_method", 'plan',"is_free",'contract_period_free','start_date_free','end_date_free', 'goal_contacts_monthly', 'goal_total_blogs','contract_period','start_date','end_date','option','contract_period_option','start_date_option','end_date_option',"site_id_main_channel","goal_main_channel","site_id_op_1","goal_op1","site_id_op_2","goal_op2", 'comment']

  success_message = 'Contract was created.'

  def get_success_url(self): 
    return reverse("customer_contract_create", args=(self.kwargs['customer_group_id'] ,self.kwargs['customer_id'] ))

  def get_form(self, form_class=None):
    #1)Lấy form
    form = super().get_form(form_class)
    customer_group_id = self.kwargs['customer_group_id']
    customer_id = self.kwargs['customer_id']
  
    form.fields['customer'].initial  = int(customer_id)
    form.fields['customer'].disabled = True
    #2)Dữ liệu
    form.fields['start_date'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['end_date'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['start_date_option'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['start_date_option'].required = False
    form.fields['contract_period_free'].required = False
    form.fields['end_date_option'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['end_date_option'].required = False
    form.fields['start_date_free'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['start_date_free'].required = False
    form.fields['end_date_free'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['end_date_free'].required = False
    form.fields['contract_period_option'].required = False

    list_method_choice_value = [("once","一括"),
                                ("monthly","月次"),
                                ("completely free","完全無償"),
                                ("other","その他")]
                                
    form.fields['payment_method'] = forms.ChoiceField(
                                    choices=list_method_choice_value,
                                    widget=forms.Select(),
                                    label="請求方法",
                                    required=True
                                )

    # form.fields['end_date'].disabled = True
    customer_group = CustomerGroup.objects.get(pk=customer_group_id)
    list_site = customer_group.site.all()
    list_site_choice_main_channel = [(-1,"-- メインチャンネルを選択 --")]
    list_site_choice_op1_channel = [(-1,"-- OP#1 チャンネル --")]
    list_site_choice_op2_channel = [(-1,"-- OP#2 チャンネル --")]
    for site in list_site:
      list_site_choice_main_channel.append((int(site.id),site.name))
      list_site_choice_op1_channel.append((int(site.id),site.name))
      list_site_choice_op2_channel.append((int(site.id),site.name))

    form.fields['site_id_main_channel'] = forms.IntegerField(
    widget=forms.Select(
    choices=list_site_choice_main_channel
    ),
    label="メインチャンネル",
    required = False
    )

    form.fields['site_id_op_1'] = forms.IntegerField(
    widget=forms.Select(
    choices=list_site_choice_op1_channel
    ),
    label="OP 1",
    required=False,
    )

    form.fields['site_id_op_2'] = forms.IntegerField(
    widget=forms.Select(
    choices=list_site_choice_op2_channel
    ),
    label="OP 2",
    required=False,
    )
    

    form.fields['goal_main_channel'].widget = forms.TextInput()
    form.fields['goal_main_channel'].required = False
    form.fields['goal_main_channel'].label  = "メインチャンネルの記事本数（⽉）"

    form.fields['goal_op1'].widget = forms.TextInput()
    form.fields['goal_op1'].label  = "OP#1の記事本数（⽉）"

    form.fields['goal_op1'].required = False
    form.fields['goal_op2'].widget = forms.TextInput()
    form.fields['goal_op2'].required = False
    form.fields['goal_op2'].label  = "OP#2の記事本数（⽉）"


    list_customer = Customer.objects.filter(customer_group=customer_group_id)
    list_plan = CustomerGroupPlanOption.objects.filter(customer_group=customer_group_id,type='plan')
    list_option = CustomerGroupPlanOption.objects.filter(customer_group=customer_group_id,type='option')
    
    
    #3)Sửa form.
    list_option_choice = Group.objects.filter(pk__in=(x.auth_group.id for x in list_option))
    list_option_choice_value = []
    for i in list_option_choice:
      list_option_choice_value.append((i.id,i.name))

    form.fields['customer'].queryset = list_customer
    form.fields['plan'].queryset = Group.objects.filter(pk__in=(x.auth_group.id for x in list_plan))
    
    form.fields['option']  = forms.ModelMultipleChoiceField(
    queryset=Group.objects.filter(pk__in=(x.auth_group.id for x in list_option)),
    widget=forms.CheckboxSelectMultiple(),
    required=False,
    )
    form.fields['comment'].required = False
    
    return form
  
  def form_invalid(self, form):
    print("form_invalid",form.errors)
    return super().form_invalid(form)

  def get_context_data(self):
    data = super().get_context_data()

    data['customer_group_id'] = self.kwargs['customer_group_id']
    data['customer_id'] = self.kwargs['customer_id']
    return data

class CustomerContractListView(SuccessMessageMixin,PermissionRequiredMixin,ListView):
  model = CustomerContract
  permission_required = ['f_1_1_customers.view_customercontract']
  template_name = 'apps/f_1_1_customers/customer_contract/customer_contract_list.html'
  context_object_name = 'customer_contract_list'
  ordering = ['-start_date']
  
  def get_queryset(self):
    #1)Dữ liệu
    qs = super().get_queryset()
    
    # #1.2)Dữ liệu từ request
    if self.request.GET:
      customer_group_id = int(self.request.GET.get('group',-1))
      customer_id = int(self.request.GET.get('customer',-1))
      site_id = int(self.request.GET.get('site',-1))
      plan_id = int(self.request.GET.get('plan',-1))
      option_id = int(self.request.GET.get('option',-1))
      status = int(self.request.GET.get('status',-1))
    else:
      return qs

    #2.1)Filter theo group
    if customer_group_id != -1:
      list_customers = Customer.objects.filter(customer_group=customer_group_id)
      qs = qs.filter(customer__in = list_customers)

    #2.2) Filter theo customer
    if customer_id != -1:
      qs = qs.filter(customer_id=customer_id)
    
    #2.2.1) Filter theo Site
    if site_id != -1:
      list_main_channel = CustomerSetting.objects.filter(is_main_channel=1, site_id=site_id)
      dict_main_channel = {}
      for item in list_main_channel:
        dict_main_channel[item.customer_id] = 1

      list_customers = Customer.objects.all()
      list_customer_filter = []
      for customer in list_customers:
        if dict_main_channel.get(customer.id): 
          list_customer_filter.append(customer)
          
      qs = qs.filter(customer__in = list_customer_filter)

    # 2.4)Filter theo hợp đồng
    if plan_id != -1:
      new_qs = []
      for customer_contract in qs:
        if customer_contract.plan_id == plan_id: 
          new_qs.append(customer_contract)
      qs = new_qs

    #2.5)Filter theo option
    if option_id != -1:
      new_qs = []
      for customer_contract in qs:
        if customer_contract.option.all().filter(pk=option_id): 
          new_qs.append(customer_contract)
      qs = new_qs

    #Thêm trường status using vào trong queryset
    for i in qs:
      #hết hạn
      if i.end_date < datetime.now().date():

        #hết hạn nhưng vẫn còng dùng đc
        if int((datetime.now().date() - i.end_date).days) <= 14:
          setattr(i, 'status', '終了')
        
        else:
          #Hết hạn nhưng không đc login vào tool nữa nhé.
            setattr(i, 'status', '無効')
      
      #Đang sử dụng
      elif i.start_date <= datetime.now().date() and i.end_date >= datetime.now().date():
        setattr(i, 'status', "契約中")

      #Chưa sử dụng
      else:
        setattr(i, 'status', "開始前")


    if status != -1:

      #Lấy status của customer đó
      str_status = ""
      if status == 1:
        str_status="開始前"

      if status == 2:
        str_status="契約中"

      if status == 3:
        str_status="終了"

      if status == 4:
        str_status="無効"

      qs = list(filter(lambda x: x.status == str_status, qs))

    #3)Trả về
    return qs

  def get_context_data(self, **kwargs):
    #1)Dữ liệu
    data = super().get_context_data()
    customer_group_id = self.request.GET.get('group')
    customer_setting_exist = False
    #2)Trả về
    if self.request.GET:
      customer_group_id = int(self.request.GET.get('group',-1))
      customer_id = int(self.request.GET.get('customer',-1))
      site_id = int(self.request.GET.get('site',-1))
      list_site = []
      #2.1)Filter theo group
      if customer_group_id != -1:
        list_customer = Customer.objects.filter(customer_group=customer_group_id)
      
      if site_id != -1:
        list_customer = Customer.objects.filter(customer_group=customer_group_id , site = site_id)
      else:
        list_site = Site.objects.all()
        list_customer = Customer.objects.filter(customer_group=customer_group_id)

      if customer_id != -1:
        try:
          customer_obj = Customer.objects.get(pk=customer_id)
          list_site = customer_obj.site.all()
          print(customer_obj.customersetting_set.all())
          customer_setting_exist = True if customer_obj.customersetting_set.all() else False

        except Customer.DoesNotExist:
          list_site = []
      else:
        list_site = Site.objects.all()

      if customer_group_id != -1:
        customer_group = CustomerGroup.objects.get(pk=customer_group_id)
        list_plans = CustomerGroupPlanOption.objects.filter(customer_group=customer_group,type='plan').order_by('sort')
        list_options = CustomerGroupPlanOption.objects.filter(customer_group=customer_group,type='option').order_by('sort')
      else:
        customer_group = CustomerGroup.objects.all()
        list_plans = CustomerGroupPlanOption.objects.filter(type='plan').order_by('sort')
        list_options = CustomerGroupPlanOption.objects.filter(type='option').order_by('sort')

    else:
      list_customer = Customer.objects.all()
      list_site = Site.objects.all()
      list_plans = []
      list_options = []
      customer_group = CustomerGroup.objects.all()
      
    list_customer_groups = CustomerGroup.objects.all()
    
    if str(customer_group_id) != '-1' and customer_group_id != None:
      list_site_group = customer_group.site.all()
      
      #khi group được chọn thì chỉ filter các site thuộc group đó thôi
      list_site = list(filter(lambda site: site in list_site_group, list_site))
    
    dict_main_channel = {}
    list_main_channel = CustomerSetting.objects.filter(is_main_channel=1)
    for channel in list_main_channel:
      dict_main_channel[channel.customer_id] = channel.site.en_name

    data['list_customer_groups'] = list_customer_groups
    data['list_customer'] = list_customer
    data['list_site'] = list_site
    data['list_plans'] = list_plans
    data['list_options'] = list_options
    data['customer_setting_exist'] = customer_setting_exist
    data['dict_main_channel'] = dict_main_channel
    
    return data

class CustomerContractDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView): 
  model = CustomerContract
  permission_required = ['f_1_1_customers.delete_customercontract']
  template_name = 'apps/f_1_1_customers/customer_contract/customer_contract_delete.html'
  success_url = reverse_lazy('customer_contract_list')
  success_message = 'Delete Contract successed'

  def delete(self, request, *args, **kwargs):
    messages.success(self.request, self.success_message)
    return super().delete(request, *args, **kwargs)

class CustomerContractUpdateView(SuccessMessageMixin, PermissionRequiredMixin,UpdateView): 
  model = CustomerContract
  permission_required = ['f_1_1_customers.change_customercontract']
  template_name = 'apps/f_1_1_customers/customer_contract/customer_contract_update.html'
  fields = ['customer',"payment_method", 'plan',"is_free",'contract_period_free','start_date_free','end_date_free', 'goal_contacts_monthly', 'goal_total_blogs','contract_period','start_date','end_date','option','contract_period_option','start_date_option','end_date_option',"site_id_main_channel","goal_main_channel","site_id_op_1","goal_op1","site_id_op_2","goal_op2", 'comment']
  success_message = 'Update successed'

  def get_form(self, form_class=None):
    #1)Lấy form
    form = super().get_form(form_class)
    customer_contract_id = self.kwargs['pk']
    customer_contract = CustomerContract.objects.get(pk=self.kwargs['pk'])
    customer_group_id = customer_contract.customer.customer_group.pk
    pay_method = customer_contract.payment_method
    
    list_method_choice_value = [("once","一括"),
                                ("monthly","月次"),
                                ("completely free","完全無償"),
                                ("other","その他")]

    form.fields['payment_method'] = forms.ChoiceField(
                                    choices=list_method_choice_value,
                                    widget=forms.Select(),
                                    label="請求方法",
                                    required=True,
                                    initial = pay_method
                                )
    
    #2)Dữ liệu
    list_customer = Customer.objects.filter(customer_group=customer_group_id)
    list_plan = CustomerGroupPlanOption.objects.filter(customer_group=customer_group_id,type='plan')
    list_option = CustomerGroupPlanOption.objects.filter(customer_group=customer_group_id,type='option')
    
    list_option_choice = Group.objects.filter(pk__in=(x.auth_group.id for x in list_option))
    
    customer_group = CustomerGroup.objects.get(pk=customer_group_id)
    list_site = customer_group.site.all()
    list_site_choice_main_channel = [(-1,"--Select Main Channel--")]
    list_site_choice_op1_channel = [(-1,"--Select OP 1 Channel--")]
    list_site_choice_op2_channel = [(-1,"--Select OP 2 Channel--")]
    for site in list_site:
      list_site_choice_main_channel.append((int(site.id),site.name))
      list_site_choice_op1_channel.append((int(site.id),site.name))
      list_site_choice_op2_channel.append((int(site.id),site.name))

    form.fields['site_id_main_channel'] = forms.IntegerField(
    widget=forms.Select(
    choices=list_site_choice_main_channel
    ),
    label="Main Channel",
    required = False
    )

    form.fields['site_id_op_1'] = forms.IntegerField(
    widget=forms.Select(
    choices=list_site_choice_op1_channel
    ),
    label="OP 1 Channel",
    required=False,
    )

    form.fields['site_id_op_2'] = forms.IntegerField(
    widget=forms.Select(
    choices=list_site_choice_op2_channel
    ),
    label="OP 2 Channel",
    required=False,
    )

    form.fields['goal_main_channel'].widget = forms.TextInput()
    form.fields['goal_main_channel'].label  = "Goal Main Channel"
    form.fields['goal_op1'].widget = forms.TextInput()
    form.fields['goal_op1'].label  = "Goal OP 1"

    form.fields['goal_op1'].required = False
    form.fields['goal_op2'].widget = forms.TextInput()
    form.fields['goal_op2'].required = False
    form.fields['goal_op2'].label  = "Goal OP 2"


    

    list_option_choice_value = []
    for i in list_option_choice:
      list_option_choice_value.append((i.id,i.name))
   

    form.fields['start_date'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['end_date'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['start_date_option'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['start_date_option'].required = False
    form.fields['contract_period_free'].required = False
    form.fields['end_date_option'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['end_date_option'].required = False
    form.fields['start_date_free'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['start_date_free'].required = False
    form.fields['end_date_free'].widget = forms.TextInput(attrs={'type': 'date'})
    form.fields['end_date_free'].required = False
    form.fields['contract_period_option'].required = False
    #3)Sửa form
    form.fields['customer'].disabled = True
    form.fields['plan'].queryset = Group.objects.filter(pk__in=(x.auth_group.id for x in list_plan))
    # form.fields['option']  = forms.ChoiceField(
    #     choices=list_option_choice_value,
    #     widget=forms.RadioSelect(),
    #     label="オプション",
    #     required=False,
    #     initial = option_id
    # )

    form.fields['option']  = forms.ModelMultipleChoiceField(
    queryset=Group.objects.filter(pk__in=(x.auth_group.id for x in list_option)),
    widget=forms.CheckboxSelectMultiple(),
    required=False,
    )
    

    return form

  def form_invalid(self, form):
    print("form_invalid",form.errors)
    return super().form_invalid(form)


  def get_success_url(self):
    return reverse("customer_contract_update", args=(self.kwargs['pk'],))  

class ContractDeleteBulkView(SuccessMessageMixin, PermissionRequiredMixin, View): 
  permission_required = ['f_1_1_customers.delete_customercontract']

  def post(self, request):
    #1)Dữ liệu
    list_id = self.request.POST['list_id'].split(',')

    #2)Xử lý
    list_customer_contracts = CustomerContract.objects.filter(pk__in=list_id)
    list_customer_contracts.delete()
    return HttpResponse(1)

########################################################################################

###############################   END     Contract  ####################################

########################################################################################






########### CUSTOMER SETTING #####################

def ajax_load_customer_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    param_customer_id = int(request.POST["customer_id"])
    param_site_id = int(request.POST.get("site_id",-1))
    
    list_sites = Customer.objects.get(pk=param_customer_id).site.all()
    
    if param_site_id != -1:
      site_id = param_site_id
    else:  
      site_id = list_sites[0].id
    
    customer_setting = CustomerSetting.objects.filter(customer_id=param_customer_id,site_id=site_id)
    
    list_hb_form_current = []
    default_file_password = ""
    is_main_channel = False

    if len(customer_setting) != 0:
      list_hb_form_current = json.loads(customer_setting[0].hb_form_id)
      default_file_password = customer_setting[0].default_file_password
      is_main_channel = customer_setting[0].is_main_channel

    customer_info = Customer.objects.filter(id=param_customer_id)[0]
    
    #2)API
    list_form = []
    obj_site_auth = SiteAuth.objects.filter(site_id = site_id)

    if len(obj_site_auth) != 0:
      if obj_site_auth[0].last_hub_refresh_token != '-1':
        list_form = HubspotHandleFormsAPI(site_id).get_form_name_and_guid_id()

    is_auth_hub = False
    obj_site_auth = SiteAuth.objects.filter(site_id = site_id)
    if obj_site_auth:
      if obj_site_auth[0].last_hub_refresh_token != '-1':
        is_auth_hub = True

    #3) dữ liệu trả về  
    data = {
      "customer_id" : param_customer_id,
      "customer_info" : customer_info,
      "list_site" : list_sites,
      "list_form_hb" : list_form,
      "site_current" : site_id,
      "is_auth_hub" : is_auth_hub,
      "default_file_password" : default_file_password,
      "list_hb_form_current" : list_hb_form_current,
      "is_main_channel" : is_main_channel
    }
    
    tmp_file_path = 'apps/f_1_1_customers/customer/modal-detail-customer-setting.html'

    return render(request, tmp_file_path, data)   

def ajax_save_customer_setting(request):
  if request.method == 'POST' and request.is_ajax():
    #1) Lấy dữ liệu
    param_customer_id = request.POST["customer_id"]
    param_list_hb_form = request.POST["list_hb_form"].split(",")
    param_site_id = request.POST["site_id"]
    param_default_file_password = request.POST["default_file_password"]
    param_is_main_channel = True if request.POST["is_main_channel"] == '1' else False

    print(request.POST["is_main_channel"], 'is_main_channel')
    print(param_is_main_channel, 'param_is_main_channel')
    
    obj_customer_setting = CustomerSetting.objects.filter(site_id=param_site_id,customer_id=param_customer_id)
    if not obj_customer_setting:
      obj_customer_setting = CustomerSetting(site_id = param_site_id ,
                                            customer_id = param_customer_id,
                                            hb_form_id =json.dumps(param_list_hb_form),
                                            default_file_password = param_default_file_password,
                                            created_date = datetime.now(),
                                            last_updated = datetime.now(),
                                            is_main_channel = param_is_main_channel)

      
      obj_customer_setting.save()
    else:
      obj_customer_setting = obj_customer_setting[0]
      obj_customer_setting = CustomerSetting(id = obj_customer_setting.id ,
                                            site_id = param_site_id,
                                            customer_id = param_customer_id,
                                            hb_form_id =json.dumps(param_list_hb_form),
                                            default_file_password = param_default_file_password,
                                            created_date = obj_customer_setting.created_date,
                                            last_updated = datetime.now(),
                                            is_main_channel = param_is_main_channel)

      
      obj_customer_setting.save()

    #3) dữ liệu trả về  
 
    return HttpResponse(1)


########### DOWLOAD CUSTOMER #####################
@login_required(login_url='/')
def download_customer_list(request):
  plan_id = int(request.GET.get('plan',-1))
  option_id = int(request.GET.get('option',-1))
  status = int(request.GET.get('status',-1))
  site_id = int(request.GET.get('site',-1))
  customer_id = request.GET.get('customer_id',-1)

  list_customers = Customer().filter_customers(site_id, status, plan_id, option_id, customer_id)
  
  #Tạo file excel
  reponse = draw_excel.draw_list_customer(list_customers)

  return reponse

@login_required(login_url='/')
def download_customer_contract_list(request):
  #1.1)Dữ liệu từ request
  customer_group_id = int(request.GET.get('group',-1))
  customer_id = int(request.GET.get('customer',-1))
  site_id = int(request.GET.get('site',-1))
  plan_id = int(request.GET.get('plan',-1))
  option_id = int(request.GET.get('option',-1))
  status = int(request.GET.get('status',-1))

  qs = CustomerContract.objects.all()

  dict_main_channel = {}
  list_customer_setting_main_channel = CustomerSetting.objects.filter(is_main_channel=1)
  for customer_setting in list_customer_setting_main_channel:
    dict_main_channel[customer_setting.customer_id] = customer_setting.site.en_name

  #2.1)Filter theo group
  if customer_group_id != -1:
    list_customers = Customer.objects.filter(customer_group=customer_group_id)
    qs = qs.filter(customer__in = list_customers)

  #2.2) Filter theo customer
  if customer_id != -1:
    qs = qs.filter(customer_id=customer_id)
  
  #2.2.1) Filter theo Site
  if site_id != -1:
    list_main_channel = CustomerSetting.objects.filter(is_main_channel=1, site_id=site_id)
    dict_main_channel_filter = {}
    for item in list_main_channel:
      dict_main_channel_filter[item.customer_id] = 1

    list_customers = Customer.objects.all()
    list_customer_filter = []
    for customer in list_customers:
      if dict_main_channel_filter.get(customer.id): 
        list_customer_filter.append(customer)
        
    qs = qs.filter(customer__in = list_customer_filter)

  # 2.4)Filter theo hợp đồng
  if plan_id != -1:
    new_qs = []
    for customer_contract in qs:
      if customer_contract.plan_id == plan_id: 
        new_qs.append(customer_contract)
    qs = new_qs

  #2.5)Filter theo option
  if option_id != -1:
    new_qs = []
    for customer_contract in qs:
      if customer_contract.option.all().filter(pk=option_id): 
        new_qs.append(customer_contract)
    qs = new_qs

  #Thêm trường status using vào trong queryset
  for i in qs:
    #hết hạn
    if i.end_date < datetime.now().date():

      #hết hạn nhưng vẫn còng dùng đc
      if int((datetime.now().date() - i.end_date).days) <= 14:
        setattr(i, 'status', '終了')
      
      else:
        #Hết hạn nhưng không đc login vào tool nữa nhé.
          setattr(i, 'status', '無効')
    
    #Đang sử dụng
    elif i.start_date <= datetime.now().date() and i.end_date >= datetime.now().date():
      setattr(i, 'status', "契約中")

    #Chưa sử dụng
    else:
      setattr(i, 'status', "開始前")


  if status != -1:

    #Lấy status của customer đó
    str_status = ""
    if status == 1:
      str_status="開始前"

    if status == 2:
      str_status="契約中"

    if status == 3:
      str_status="終了"

    if status == 4:
      str_status="無効"

    qs = list(filter(lambda x: x.status == str_status, qs))
  
  
  #Tạo file excel
  reponse = draw_excel.draw_list_customer_contract(qs, dict_main_channel)

  return reponse

#####

def test(request):
  date_now = '2021-04-01'
  site_id = 206640
  list_activate_customers = Customer().get_customers_contract(site_id, date_now)
  list_data = []

  table_html = '''<table cellpadding="4">
                    <thead>
                      <tr>
                        <th>no</th>
                        <th>id</th>
                        <th>name</th>
                        <th>plan</th>
                        <th>start_date</th>
                        <th>end_date</th>
                      </tr>
                    </thead>
                    <tbody>
                      [DATA]
                    </tbody>
                  </table>'''

  str_data = ''
  tr_tmp = '''<tr>
                <td>[no]</td>
                <td>[id]</td>
                <td>[name]</td>
                <td>[plan]</td>
                <td>[start_date]</td>
                <td>[end_date]</td>
              </tr>'''

  for index, customer_contract in enumerate(list_activate_customers):
    list_data.append({
      'id': customer_contract.id,
      'name': customer_contract.name,
      'plan': customer_contract.plan,
      'start_date': customer_contract.start_date,
      'end_date': customer_contract.end_date
    })
    str_data += tr_tmp.replace('[no]', str(index)).replace('[id]', customer_contract.id).replace('[name]', customer_contract.name).replace('[plan]', customer_contract.plan).replace('[start_date]', customer_contract.start_date.strftime("%Y-%m-%d")).replace('[end_date]', customer_contract.end_date.strftime("%Y-%m-%d"))

  table_html_data = table_html.replace('[DATA]', str_data)

  return HttpResponse(table_html_data)
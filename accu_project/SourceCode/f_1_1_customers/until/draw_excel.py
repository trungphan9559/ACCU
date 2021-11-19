from __Config.Include.Common_Include import *

import pandas as pd
import ast
try:
    from BytesIO import BytesIO 
except ImportError:
    from io import BytesIO 

def draw_list_customer(list_data_customer):
	try:
		date_now = datetime.now()
		end_date_now = date_now.strftime("%Y-%m-%d")
		dict_data_customer = {}
		list_customer_name = []
		list_customer_code = []
		list_customer_domain = []
		list_customer_current_plan = []
		list_customer_current_option = []
		list_customer_site = []
		list_customer_status = []

		for customer in list_data_customer:
			status = '契約中' if customer.is_active == 1 else ('開始前' if customer.is_next_contract == 1 else '終了')

			list_customer_name.append(customer.name)
			list_customer_code.append(customer.code)
			list_customer_domain.append(customer.domain)
			list_customer_current_plan.append(customer.plan_name)
			list_customer_current_option.append(customer.option_name)
			list_customer_site.append(customer.site_name)
			list_customer_status.append(status)


		dict_data_customer['顧客名'] = list_customer_name
		dict_data_customer['名称'] = list_customer_code
		dict_data_customer['サイトURL'] = list_customer_domain
		dict_data_customer['現プラン'] = list_customer_current_plan
		dict_data_customer['現オプション'] = list_customer_current_option
		dict_data_customer['契約サイト'] = list_customer_site
		dict_data_customer['契約状況'] = list_customer_status


		#2. Create a Pandas Excel writer using XlsxWriter as the engine.
		output = BytesIO() 
		writer = pd.ExcelWriter(output,engine='xlsxwriter')
		draw_excel_controller = DrawExcel(writer)

		#3) Seminar Property
		sheet_name = 'Customer'

		draw_excel_controller.draw_excel_table_only(sheet_name,dict_data_customer,pos_row=0)
		draw_excel_controller.auto_set_column(sheet_name,dict_data_customer)  


		writer.save()
		output.seek(0)

		response = HttpResponse(output, content_type='text/csv')
		file_name = '{0}-{1}.csv'.format("MSP-customer-", end_date_now)

		response['Content-Disposition'] = "attachment;filename={0}".format(file_name)
		print("qqqqqq")
		return response
	except Exception as inst:
		print(inst,"Errorr")
		
def draw_list_customer_contract(list_data_customer_contract, dict_main_channel):
	try:
		date_now = datetime.now()
		end_date_now = date_now.strftime("%Y-%m-%d")

		dict_data_customer = {}
		list_customer_name = []
		list_customer_code = []
		list_customer_start_date = []
		list_customer_end_date = []
		list_customer_contract_period = []
		list_customer_current_plan = []
		list_customer_current_option = []
		list_customer_goal_contract = []
		list_customer_goal_blog = []
		list_customer_status = []
		list_customer_site = []

		for contract in list_data_customer_contract:
			#Customer name, code
			list_customer_name.append( str(contract.customer.name) )
			list_customer_code.append(str(contract.customer.code))
			
			#Customer domain
			list_customer_start_date.append(contract.start_date.strftime('%Y-%m-%d'))
			list_customer_end_date.append(contract.end_date.strftime('%Y-%m-%d'))
			list_customer_contract_period.append(contract.contract_period)
			list_customer_current_plan.append(contract.plan.name)

			#Customer plan, option

			list_option = contract.option.all()
			if list_option:
				list_option = [i.name for i in list_option]
				list_customer_current_option.append(",  ".join(list_option))
			else:
				list_customer_current_option.append("")

			
			main_channel = dict_main_channel[contract.customer.id] if dict_main_channel.get(contract.customer.id) else ''

			list_customer_goal_blog.append(contract.goal_total_blogs)
			list_customer_goal_contract.append(contract.goal_contacts_monthly)
			list_customer_status.append(contract.status)
			list_customer_site.append(main_channel)


		dict_data_customer['顧客名'] = list_customer_name
		dict_data_customer['名称'] = list_customer_code
		dict_data_customer['開始日'] = list_customer_start_date
		dict_data_customer['終了日'] = list_customer_end_date
		dict_data_customer['契約期間'] = list_customer_contract_period
		dict_data_customer['プラン'] = list_customer_current_plan
		dict_data_customer['オプション'] = list_customer_current_option
		dict_data_customer['契約サイト'] = list_customer_site
		dict_data_customer['ゴール（送信数）'] = list_customer_goal_contract
		dict_data_customer['ゴール（投稿記事数）'] = list_customer_goal_blog
		dict_data_customer['契約状態'] = list_customer_status


		#2. Create a Pandas Excel writer using XlsxWriter as the engine.
		output = BytesIO() 
		writer = pd.ExcelWriter(output,engine='xlsxwriter')
		draw_excel_controller = DrawExcel(writer)

		#3) Seminar Property
		sheet_name = 'Customer Contract'

		draw_excel_controller.draw_excel_table_only(sheet_name,dict_data_customer,pos_row=0)
		draw_excel_controller.auto_set_column(sheet_name,dict_data_customer)  


		writer.save()
		output.seek(0)

		response = HttpResponse(output, content_type='text/csv')
		file_name = '{0}-{1}.csv'.format("MSP-customer-contract-", end_date_now)

		response['Content-Disposition'] = "attachment;filename={0}".format(file_name)

		return response
	except Exception as inst:
		print(inst,"Errorr")







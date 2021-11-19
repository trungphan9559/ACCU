from __Config.Include.Common_Include import *

import pandas as pd
import ast
try:
    from BytesIO import BytesIO 
except ImportError:
    from io import BytesIO 

def draw_list_user(list_user):
	try:
		dict_data_user = {}
		list_username = []
		list_fullname = []
		list_email = []
		list_user_status = []
		list_last_login = []
		list_date_joined = []
		list_customer = []
		
		for user in list_user:
			# if user.email == "":
			# 	continue
			# else:
			list_email.append(user.email)
			#Customer name, code
			if user.first_name == None:
				list_fullname.append(user.last_name)
			elif user.last_name == None:
				list_fullname.append(user.list_fullname)
			else:
				list_fullname.append(user.first_name +  " " + user.last_name)
			
			
			if  user.last_login == None and user.is_active == False:
				list_user_status.append("Ativating")
			elif  user.is_active == True:
				list_user_status.append("Active")
			else:
				list_user_status.append("Locked")
	
			list_customer.append(user.customer_name)
			
			# if user.last_login == None:
			# 	list_last_login.append("-")
			# else:
			# 	list_last_login.append(user.last_login.strftime('%Y-%m-%d'))
			# list_date_joined.append(user.date_joined.strftime('%Y-%m-%d'))		

		dict_data_user['Email'] = list_email
		dict_data_user['Full Name'] = list_fullname
		dict_data_user['Customer'] = list_customer
		dict_data_user['Status'] = list_user_status
		
		#2. Create a Pandas Excel writer using XlsxWriter as the engine.
		output = BytesIO() 
		writer = pd.ExcelWriter(output,engine='xlsxwriter')
		draw_excel_controller = DrawExcel(writer)

		#3) Seminar Property
		sheet_name = 'User'

		draw_excel_controller.draw_excel_table_only(sheet_name,dict_data_user,pos_row=1)
		draw_excel_controller.auto_set_column(sheet_name,dict_data_user)  

		writer.save()
		output.seek(0)

		response = HttpResponse(output, content_type='text/csv')
		file_name = '{0}.csv'.format("User List Info ")

		response['Content-Disposition'] = "attachment;filename={0}".format(file_name)

		return response
	except Exception as inst:
		print(inst,"Errorr")
		

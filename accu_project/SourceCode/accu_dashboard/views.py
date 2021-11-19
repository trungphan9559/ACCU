from math import nan
from re import I
from django.shortcuts import render
from __Config.Include.Common_Include import *
from random import randrange
import pandas as pd

TIME_DURATION_LIST = [{
						"min" : 0,
						"max" : 5,
					},
					{
						"min" : 5,
						"max" : 15,
					},{
						"min" : 15,
						"max" : 30,
					},{
						"min" : 30,
						"max" : 60,
					},{
						"min" : 60,
						"max" : 99999999,
					},
					]


class HomeView(TemplateView):
	template_name = 'apps/accu_dashboard/dashboard.html'

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data()
		param_type = self.request.GET.get("type",1)
		if str(param_type) not in ["1", "2", "3"]:
			param_type = "1"

		# Hard code power off
		list_provice = ["Ha Giang", "Cao Bang", "Bac Kan", "Tuyen Quang", "Lao Cai", "Dien Bien Phu", "Lai Chau", "Son La", "Yen Bai", "Hoa Binh", "Thai Nguyen", "Lang Son", "Ha Long"]
		list_district = ["Phong Điền", "Phú Vang", "A Lưới", "Cư Kwin", "Ea H'leo", "Núi Thành", "Tây Giang", "Đông Giang", "Duy Xuyên", "Nam Đông", "Ayunpa", "Ia Pa", "Mang Yang"]
		
		list_dai = []
		for idx,dicstric in enumerate(list_district):
			list_dai.append(f"Dai {idx+1}")


		dict_data_location = {
			"1" : list_dai,
			"2" : list_provice,
			"3" : list_district,
		}
		list_data_name = dict_data_location[str(param_type)]


		dict_data_off_provice = {
			"list_name" : ','.join(list_data_name),
			"list_time" : json.dumps([ randrange(100) for i in list_data_name]),
		}


		# Hard code battery
		list_batterys = [
			{
				'type' : "A",
				'name' : "name1",
				'label' : "labelA",
				'capacity' : "capacityA", # dung luong
				'producer' : "producerA", # nha san xuat
				'location' : "locationA",
				'current_time' : "lcurrent_timeA",
			},
			{
				'type' : "B",
				'name' : "nameB",
				'label' : "labelB",
				'capacity' : "capacityB", # dung luong
				'producer' : "producerB", # nha san xuat
				'location' : "locationB",
				'current_time' : "lcurrent_timeB",

			},
			{
				'type' : "C",
				'name' : "namec",
				'label' : "labelC",
				'capacity' : "capacityC", # dung luong
				'producer' : "producerC", # nha san xuat
				'location' : "locationC",
				'current_time' : "lcurrent_timeC",

			},
		]

		data['power_off'] = dict_data_off_provice
		data['list_batrerys'] = list_batterys
		return data	


class IndexDashBoard(TemplateView):
	template_name = 'apps/accu_dashboard/dashboard-summary.html'

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data()
		
		return data	


def get_data_summary(request):
	#1) Lấy dữ liệu
	param_start_date = request.POST["start_date"]
	param_end_date = request.POST["end_date"]
	param_time_duration = request.POST["time_duration"]
	print("param_start_date", param_start_date)
	print("param_end_date", param_end_date)
	print("param_time_duration", param_time_duration)

	
	# randrange(100)
	list_data_table = []

	#Read file excel
	file = str(settings.BASE_DIR + '/__Security_Data/MSMD.xlsx')
 
	xl_file = pd.ExcelFile(file)

	dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}

	list_value_excel = list(dfs.values())[0]
	dict_data_excel = {}
	for i in list_value_excel:
		dict_data_excel[i] = list_value_excel[i]

	"""
		['DATETIME', 'SITE_ID', 'BAT_DAU', 'KET_THUC', 'THOI_GIAN_MLL', 
			'ALARM_NAME', 'PROVINCE', 'DISTRICT', 'MA_PHONG_XL', 'NETWORK',
			 'NN_CAP_1', 'NN_CAP_2', 'NN_CAP_3', 'THOI_GIAN_MAT_DIEN', 'THOI_GIAN_CHAY_ACCU', 'TTML'])

	"""


	#Filter data
	param_start_date = datetime.strptime(param_start_date,"%Y-%m-%d")
	param_end_date = datetime.strptime(param_end_date,"%Y-%m-%d")

	for idx, data_time_even in enumerate(dict_data_excel["DATETIME"]):
		
		# Filter thowif gian mat dien
		if param_time_duration != -1  and int(param_time_duration) < len(TIME_DURATION_LIST) :
			time_min = TIME_DURATION_LIST[int(param_time_duration) -1]["min"]
			time_max = TIME_DURATION_LIST[int(param_time_duration) -1]["max"]
			print("time_min",time_min)
			print("time_max",time_max)
			if str(dict_data_excel["THOI_GIAN_CHAY_ACCU"][idx].astype(float)) == "nan" : 
				dict_data_excel["THOI_GIAN_CHAY_ACCU"][idx] = 0

			if dict_data_excel["THOI_GIAN_CHAY_ACCU"][idx].astype(float) < time_min or dict_data_excel["THOI_GIAN_CHAY_ACCU"][idx].astype(float) > time_max:
				continue 
			



		if data_time_even <= param_end_date and data_time_even >=  param_start_date:
			list_data_table.append({
				"time" : data_time_even,
				"site_id" : dict_data_excel["SITE_ID"][idx],
				"alarm_name" : dict_data_excel["ALARM_NAME"][idx],
				"province" : dict_data_excel["PROVINCE"][idx],
				"district" : dict_data_excel["DISTRICT"][idx],
				"room_code" : dict_data_excel["MA_PHONG_XL"][idx],
				"network" : dict_data_excel["NETWORK"][idx],
				"time_cut_off" : dict_data_excel["THOI_GIAN_MAT_DIEN"][idx],
				"time_run_accu" : float(dict_data_excel["THOI_GIAN_CHAY_ACCU"][idx].astype(float)),
			})


	data = {}
	
	data['list_data_sumary'] = sorted(list_data_table, key=lambda x: x["time_run_accu"], reverse=True)


	tmp_file_path = 'apps/accu_dashboard/detail-dashboard/summary.html'
	return render(request, tmp_file_path, data)


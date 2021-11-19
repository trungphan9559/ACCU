import time
import calendar

from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class DateCaculate:

  def get_list_month_range(self,start_date):
    list_month = []

    str_pre_month = datetime.now().strftime('%Y-%m-01')
    pre_month = datetime.strptime(str_pre_month,'%Y-%m-%d')

    while(str_pre_month > start_date):
      pre_month -= timedelta(1)
      str_pre_month = pre_month.strftime('%Y-%m-01')
      list_month.append(str_pre_month)
      pre_month = datetime.strptime(str_pre_month,'%Y-%m-%d')
      str_pre_month = pre_month.strftime('%Y-%m-01')

    if str_pre_month > start_date:
      list_month.append(start_date)

    list_month.reverse()

    return list_month
    

  def get_work_day(self,year,month):
    #1)Ngày tháng
    week_days = ("月", "火", "水", "木", "金", "土", "日")

    month_start_date = datetime.strptime('{}-{}-01'.format(year,month),'%Y-%m-%d')
    month_end_date = month_start_date + relativedelta(months=1) - timedelta(1)

    #2)Xử lý
    #2.1)Số ngày làm việc tháng này
    num_of_workdays = workdays.networkdays(month_start_date, month_end_date)
    
    #2.2)Số ngày nghỉ tháng này
    jp_holidays = jpholiday.month_holidays(year, month)
    list_jp_holidays = []
    num_of_worked_days = 0

    for date in jp_holidays:
      #2.2.1)Tính số ngày lễ trùng với ngày làm việc
      week_day = date[0].weekday()
      if week_day in [5, 6]:
        continue

      day = {
          'date': date[0].strftime("%m/%d") + '({0})'.format(week_days[week_day]),
          'name': date[1],
          'date_val': date[0].strftime("%Y-%m-%d")
      }
      list_jp_holidays.append(day)

    #2.3)Số ngày làm việc tính tới thời điểm hiện tại
    today = datetime.now()
    holidays = [x[0] for x in jp_holidays]

    if today > month_end_date:
      num_of_worked_days = workdays.networkdays(month_start_date.date(), month_end_date.date(), holidays=holidays)
    else:
      num_of_worked_days = workdays.networkdays(month_start_date.date(), today.date(), holidays=holidays)

    #3)Trả về
    return {
      'num_of_workdays' : num_of_workdays - len(list_jp_holidays),
      'num_of_worked_days' : num_of_worked_days,
      'list_jp_holidays' : list_jp_holidays,
    }

  def get_current_milliseconde(self):
    now = datetime.now()
    millisecond = int(time.mktime(now.timetuple())*1000)
    
    return millisecond
      
  def conver_datetime_to_millisecond(self,date):
    #dayformat 2019-01-31
    list_date = date.split("-")

    t1 = datetime(int(list_date[0]),int(list_date[1]),int(list_date[2]))

    millisecond = int(time.mktime(t1.timetuple())*1000)

    return millisecond

  def conver_millisecond_to_hours_minutes_seconds(self,millisecond):  
    total_seconds = millisecond//1000
    hours = total_seconds//60//60
    minutes = total_seconds//60%60
    seconds = total_seconds%60%60

    hours = hours if hours >= 10 else '0' + str(hours)
    minutes = minutes if minutes >= 10 else '0' + str(minutes)
    seconds = seconds if seconds >= 10 else '0' + str(seconds)
    
    return "{0}:{1}:{2}".format(hours,minutes,seconds)

  def conver_millisecond_to_datetime(self,millisecond,format='%Y-%m-%d %H:%M:%S'):  
    date = datetime.fromtimestamp(float(millisecond)/1000.0)
    date = date.strftime(format)
    return date

  def get_last_date_prev_month(self,start_date):
      #day format 2019-01-31 --> 2019-02-01
      change_datetime = datetime.strptime(start_date, "%Y-%m-%d")
      new_date = change_datetime - timedelta(days=1)
      check_time = new_date.strftime('%Y-%m-%d')

      return check_time

  def convert_date_to_month(self,start_date,end_date):
    list_start_date = start_date.split("-")
    list_end_date = end_date.split("-")

    x1 = datetime(int(list_start_date[0]),int(list_start_date[1]),int(list_start_date[2]))
    x2 = datetime(int(list_end_date[0]),int(list_end_date[1]),int(list_end_date[2]))

    list_month = []

    while x2 >= x1:
    #thứ 2 là ngày 1, cn là ngày 7   
      day_range = x2.date()

      end_date = x2.strftime("%Y-%m-%d")

      x2 = x2 - timedelta(day_range.day - 1)
      start_date = x2.strftime("%Y-%m-%d")
      x2 = x2 - timedelta(1)

      if(x2 > x1):
        dict_week = {"start_date": start_date, "end_date": end_date}
        list_month.append(dict_week)
      else:
        end_date = (x2 + timedelta(day_range.day)).strftime("%Y-%m-%d")
        start_date = x1.strftime("%Y-%m-%d")
        dict_week = {"start_date": start_date, "end_date": end_date}
        list_month.append(dict_week)
    list_month.reverse()
    return list_month

  #NẾU HÔM NAY KHÔNG PHẢI CUỐI THÁNG THÌ LẤY THÁNG TRƯỚC( Input: 2019-05-12 => Output: 2019-04-30)
  def get_the_most_recent_month(self):
    date = datetime.now()
    date_2 = date + timedelta(days=1)

    if date_2.month > date.month:
      the_most_recent_month = date.strftime('%Y-%m-%d')
    else:
      the_most_recent_month = date - timedelta(days=date.day)
      the_most_recent_month = the_most_recent_month.strftime('%Y-%m-%d')
    return the_most_recent_month

  #Nhập vào start_date = '2019-01-01',end_date = '2019-04-01' xuất ra ['2019-01-01', '2019-02-01', '2019-03-01', '2019-04-01']
  def conver_date_to_list_year_month(self,start_date,end_date):
    start_date = start_date.split('-')
    start_date = datetime(int(start_date[0]),int(start_date[1]),int(start_date[2]))

    end_date = end_date.split('-')
    end_date = datetime(int(end_date[0]),int(end_date[1]),int(end_date[2]))

    list_date = []
    while start_date <= end_date:
      # date = str(start_date.year) + '年' + str(start_date.month) +'月'
      date = start_date.strftime("%Y-%m-%d")

      list_date.append(date)

      start_date += relativedelta(months=1)

    return list_date

  #Lấy số tháng tính đến thời điểm hiện tại:
  def get_date_range_by_month(self,date):
    date = date.split('-')
    date = datetime(int(date[0]),int(date[1]),int(date[2]))
    now = datetime.now()

    date_range = now - date
    date_range = date_range.days/30
    date_range = round(date_range,0)
    date_range = int(date_range)
    return date_range
	
  def convert_date_to_week(self,start_date,end_date):
    list_start_date = start_date.split("-")
    list_end_date = end_date.split("-")

    x1 = datetime(int(list_start_date[0]),int(list_start_date[1]),int(list_start_date[2]))
    x2 = datetime(int(list_end_date[0]),int(list_end_date[1]),int(list_end_date[2]))

    list_week = []

    while x2 > x1:
    #thứ 2 là ngày 1, cn là ngày 7 
        day_range = x2.isoweekday()

        end_date = x2.strftime("%Y-%m-%d")

        x2 = x2 - timedelta(day_range - 1)
        start_date = x2.strftime("%Y-%m-%d")
        x2 = x2 - timedelta(1)

        if(x2 > x1):
            dict_week = {"start_date": start_date, "end_date": end_date}
            list_week.append(dict_week)
        else:
            end_date = (x2 + timedelta(day_range)).strftime("%Y-%m-%d")
            start_date = x1.strftime("%Y-%m-%d")
            dict_week = {"start_date": start_date, "end_date": end_date}
            list_week.append(dict_week)
    
    list_week.reverse()
    return list_week

  def convert_date_to_week_2_to_6(self,start_date,end_date):
    list_week = self.convert_date_to_week(start_date,end_date)
    list_week_2_to_6 = []
    for i in list_week:
      end_date = i['end_date'].split("-")
      end_date = datetime(int(end_date[0]),int(end_date[1]),int(end_date[2]))
      end_date = end_date - timedelta(2)
      end_date = end_date.strftime("%Y-%m-%d")
      i['end_date'] = end_date
      list_week_2_to_6.append(i)

    return list_week_2_to_6  

  #Nếu chọn 30 ngày thì trả về 30 ngày ngay trước nó, để so sánh dữ liệu
  def get_date_range_compare(self,start_date,end_date):
    start = start_date.split('-')
    start = datetime(int(start[0]),int(start[1]),int(start[2]))
    end = end_date.split('-')
    end = datetime(int(end[0]),int(end[1]),int(end[2]))

    date_range = end - start
    date_range = date_range.days

    start_compare = start - timedelta(date_range + 1)
    start_compare = start_compare.strftime('%Y-%m-%d')

    end_compare = start - timedelta(1)
    end_compare = end_compare.strftime('%Y-%m-%d')
    dict_date = {
                  'start_compare' : start_compare,
                  'end_compare' : end_compare,
    }
    return dict_date

  #Nhập vào 3630 thì xuất ra 1:0:30
  def cover_second_to_hour_minute_second(self,_seconds):
    _seconds = int(_seconds)
    hour = _seconds//3600
    minute = _seconds%3600//60
    seconds = _seconds%3600%60

    if hour < 10:
      hour = '0'+str(hour) 
    if minute < 10:
      minute = '0'+str(minute) 
    if seconds < 10:
      seconds = '0'+str(seconds) 

    return str(hour) + ':' + str(minute) + ':' + str(seconds)
  
  # Lấy về list 3 tháng gần nhất  , hiện tại tháng 5 sẽ trả về tháng 2,3,4: 
  def get_three_month_nearest(self):
    today = datetime.now()

    #Lấy dữ liệu tháng thứ 1:
    start_month_1 = today - relativedelta(months=1)
    start_month_1 = datetime(int(start_month_1.year),int(start_month_1.month),1)
    day_of_current_month = datetime(int(today.year),int(today.month),1)
    end_month_1 = day_of_current_month - timedelta(1)
    end_month_1 = end_month_1.strftime('%Y-%m-%d')

    #Lấy dữ liệu tháng t2:
    start_month_2 = today - relativedelta(months=2)
    start_month_2 = datetime(int(start_month_2.year),int(start_month_2.month),1)
    end_month_2 =  start_month_1 - timedelta(1)
    end_month_2 = end_month_2.strftime('%Y-%m-%d')

    #Lấy dữ liệu tháng thứ 3:
    start_month_3 = today - relativedelta(months=3)
    start_month_3 = datetime(int(start_month_3.year),int(start_month_3.month),1)
    end_month_3 =  start_month_2 - timedelta(1)
    end_month_3 = end_month_3.strftime('%Y-%m-%d')
    
    dict_data_months= {
                'month_1' : {
                            'start_date' : start_month_3.strftime('%Y-%m-%d'),
                            "end_date"   : end_month_3,
                },
                'month_2' : {
                            'start_date' : start_month_2.strftime('%Y-%m-%d'),
                            'end_date'   : end_month_2
                },
                'month_3' : {
                            'start_date' : start_month_1.strftime('%Y-%m-%d'),
                            'end_date'   : end_month_1
                }
    }
    return dict_data_months
  
  #Hàm lấy số ngày trong khoảng đã chọn
  def get_list_date_in_range(self,start_date,end_date):
    list_start_date = start_date.split("-")
    list_end_date = end_date.split("-")

    x1 = datetime(int(list_start_date[0]),int(list_start_date[1]),int(list_start_date[2]))
    x2 = datetime(int(list_end_date[0]),int(list_end_date[1]),int(list_end_date[2]))

    delta = x2 - x1

    list_date = []
    for i in range(delta.days + 1):
      value_date = (x1 + timedelta(days=i)).strftime('%Y-%m-%d')
      list_date.append(value_date)

    return list_date

  def conver_date_to_japan_date_format(self,date,is_year_month_day=False,is_year_month=False):
    change_datetime = datetime.strptime(date, "%Y-%m-%d")

    if is_year_month:
      japan_format = str(change_datetime.year) + '年' + str(change_datetime.month) + '月'
    if is_year_month_day:
      japan_format = str(change_datetime.year) + '年' + str(change_datetime.month) + '月' + str(change_datetime.day) + '日'

    return japan_format

  def get_weekday(self, date):
    weekdays = ['月','火','水','木','金','土','日']
    weekday_index = date.weekday()
    return weekdays[weekday_index]

  def get_end_of_month(self,date):
    # '2019-04-10' -> '2019-04-30'
    date = str(date)
    date = datetime.strptime(date, "%Y-%m-%d")
    next_month = date.month + 1 if date.month != 12 else 1

    end_this_month = datetime(date.year,next_month,1)
    end_this_month = end_this_month - timedelta(days=1)
    end_this_month = end_this_month.strftime("%Y-%m-%d")

    return end_this_month

  def get_week_japanese_in_month(self,year,month):
    cal = calendar.Calendar()
    week_days = {0:"月", 1:"火", 2:"水", 3:"木", 4:"金", 5:"土", 6:"日"}
    dict_ = {}
    for week in cal.monthdayscalendar(year, month):
      for i, day in enumerate(week):
        if day == 0:
          continue
        dict_[day] = week_days[i]

    return dict_

  def get_month_range(self,report_end_date,number_of_months):
    #1)TÍNH TOÁN NGÀY THÁNG
    report_end_date = report_end_date.split('-')
    report_end_date = datetime(int(report_end_date[0]),int(report_end_date[1]),int(report_end_date[2]))

    one_year_befor = report_end_date - relativedelta(months = number_of_months - 1)
    one_year_befor = datetime(one_year_befor.year,one_year_befor.month,1)

    #2)NGÀY BẮT ĐẦU VÀ NGÀY KẾT THÚC
    end_date = str(report_end_date.date())
    start_date = str(one_year_befor.date())
      
    #3)Lấy list month
    list_month = DateCaculate().convert_date_to_month(start_date,end_date)
    
    return list_month   
  
  def get_deadline_date_jp_work(self, start_date:str, work_days:int) -> str:

    #1)convert datetime
    start_date = datetime.strptime(start_date,'%Y-%m-%d')
    end_date = start_date + timedelta(60)
    
    #2.2)Số ngày nghỉ lễ trong 1 năm tới
    jp_holidays = jpholiday.jpholiday.between(start_date, end_date)
    jp_holidays = [i[0] for i in jp_holidays]

    end_date = tmp_day = start_date
    count_days = 0
    while count_days < work_days:
      
      if tmp_day not in jp_holidays and tmp_day.weekday() not in [5,6]:
        end_date = tmp_day
        count_days += 1
      tmp_day = tmp_day + timedelta(1)

    return end_date.strftime("%Y-%m-%d")
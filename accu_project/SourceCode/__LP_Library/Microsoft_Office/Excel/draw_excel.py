import pandas as pd
import re
from pprint import pprint

class DrawExcel:
  __writer = ''

  def __init__(self,writer):
    self.__writer = writer

  def is_japanese(self, str):
    return True if re.search(r'[ぁ-んァ-ン]', str) else False 

  def set_boder_column(self,sheet_name,data_table, text_wrap=False,start_row_index=0,data_col_width=[]):
    workbook = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 
    format_col = workbook.add_format({'text_wrap': text_wrap})
    format_col.set_font_name('游ゴシック')

    format_col_border = workbook.add_format({'text_wrap': text_wrap})
    format_col_border.set_border(1)

    format_col_border_per = workbook.add_format({'num_format': '0.00%'})
    format_col_border_per.set_border(1)

    #3) Set width
    column_index = 0
    width_default = 300
    for header,list_rows in data_table.items():
      for row_index,row in enumerate(list_rows):
        row_set_index = start_row_index + row_index
        col_width = width_default
        if len(data_col_width) > (column_index + 1):
          col_width = data_col_width[column_index]

        worksheet.set_column(column_index,column_index,col_width,format_col)
        str_row = str(row)
        if str_row.find('%') == len(str_row) - 1:
          row_remove_per = str_row.replace('%','')
          row_remove_per = float(row_remove_per) / 100
          worksheet.write(row_set_index, column_index, row_remove_per, format_col_border_per)
        else:
          worksheet.write(row_set_index, column_index, row, format_col_border)

      column_index += 1


  def set_resize_column(self,sheet_name,data_table, is_border=True,max_column_width=300,col=0,text_wrap=False):
    #1) Const
    PADDING = 10
    MAX_COLUMN_WIDTH = max_column_width + PADDING 

    #2)Xử lý auto
    workbook = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 
    format_col = workbook.add_format({'text_wrap': text_wrap})
    format_col.set_font_name('游ゴシック')
    if is_border:
      format_col.set_border(1)

    i = col

    for header,list_rows in data_table.items():

      max_length = len(header)
      #2.1)Chọn hàng có độ dài lớn nhất
      is_japanese = False
      for row in list_rows:
        row = str(row)
        row_length = len(row)

        if not is_japanese:
          is_japanese = self.is_japanese(row)

        max_length = row_length if row_length > max_length else max_length

      #2.2)Set độ rộng cho cột, không vượt quá MAX_COLUMN_WIDTH
      zoom_char_val = 1.6 if is_japanese else 1.1
      worksheet.set_column(i,i,max_length * zoom_char_val + PADDING if max_length < MAX_COLUMN_WIDTH else MAX_COLUMN_WIDTH,format_col)
      
      i += 1

  def auto_set_column(self,sheet_name,data_table,max_column_width=69,col=0):
    #1) Const
    PADDING = 1
    MAX_COLUMN_WIDTH = max_column_width + PADDING 

    #2)Xử lý auto
    workbook = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 
    format_1 = workbook.add_format({'text_wrap': True})

    i = col

    for header,list_rows in data_table.items():

      max_length = len(header)
      #2.1)Chọn hàng có độ dài lớn nhất
      for row in list_rows:
        row_length = len(str(row))
        max_length = row_length if row_length > max_length else max_length

      #2.2)Set độ rộng cho cột, không vượt quá MAX_COLUMN_WIDTH
      worksheet.set_column(i,i,max_length + PADDING if max_length < MAX_COLUMN_WIDTH else MAX_COLUMN_WIDTH,format_1)
      
      i += 1

  def draw_set_column(self,sheet_name,col_index,col_width):
    workbook = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 
    format_col = workbook.add_format({'text_wrap': True})
    format_col.set_font_name('游ゴシック')

    worksheet.set_column(col_index,col_index,col_width,format_col)


  def draw_excel_table_and_avg_table_and_data_table_decreption(self,sheet_name,data_table,pos_row = 0,pos_col = 0,data_table_decreption = {}):
    #1) Xử lý dữ liệu
    param_row_table = len(list(data_table.values())[0])#6
    param_col_table = len(data_table)#11

    #1.1)Phải đưa hết data_table về dạng list thì mới lọc dược
    list_value_in_data_table = list(data_table.values())

    #1.1.2)dữ liệu 2 ngày gần nhất để tính trung bình
    pre_value = list_value_in_data_table[param_col_table - 2]
    current_value = list_value_in_data_table[param_col_table - 1]

    #1.2)bảng để lưu dữ liệu trung bình
    data_table_avg ={}
    col_avg = []

    for row in range (0,param_row_table):
        try:
            current_value = list_value_in_data_table[param_col_table - 1][row]
            pre_value = list_value_in_data_table[param_col_table - 2][row]
            #1.2.1)Tính trung bình
            if(pre_value == 0 or pre_value == "n/a"):
                value_avg = 0
            else:
                value_avg = round((current_value - pre_value)/pre_value,4)
        #1.2.2)NẾU CHỈ CÓ 1 THÁNG THÌ GÁN THẲNG BẰNG = 0
        except:
            value_avg = round(0,4)
        col_avg.append(value_avg)

    data_table_avg["前月比"] = col_avg

    #2) Draw excel
    table = pd.DataFrame(data_table)
    table_avg = pd.DataFrame(data_table_avg)
    table_decription = pd.DataFrame(data_table_decreption)

    #2.1) chuyển từ dataFrame thành table trong excel
    table.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col,startrow=pos_row,index=False)
    table_avg.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col + param_col_table + 1,startrow=pos_row,index = False)
    table_decription.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col + param_col_table + 3,startrow=pos_row,index = False)

    #2.2) Lấy 2 biến này để  thao tác vẽ và format
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 

    #2.2.1) Thêm format
    format1 = workbook.add_format({
        'bold' : True,
        })
    format2 = workbook.add_format({'num_format': '0.00%'})

    #2.2.2)Đặt kiểu dữ liệu là phần trăm
    worksheet.set_column(param_col_table + 1,param_col_table + 1, None, format2)
    worksheet.set_column(0,0, None, format1)
    
    #2.2.3)Đặt chiều rộng của cột
    worksheet.set_column(0,param_col_table + 4, 11)


  def draw_excel_column_chart_by_row_value_v2(self,sheet_name,pos_table_total_row,pos_table_total_col,pos_table_row=0,pos_table_col=0,pos_chart_row=0,pos_chart_col=0,width=1000,height=540,title=''):
    #1) Dữ liệu
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2) Draw Excel
    chart = workbook.add_chart({'type': 'column','subtype': 'stacked'})
    chart.set_size({'width': width, 'height': height})
    chart.set_title({'name': title})

    #3) In dữ liệu chart
    #3.1)Tạo value trong chart
    for col_index in range(1, pos_table_total_col + 1):
      chart.add_series({
          #Google/Facebook/Ins
          'name' : [sheet_name, pos_table_row, pos_table_col + col_index + 1],
          #2017年8月 / 2017年9月 / 2017年10月
          #[0,0] --- [0,12]
          'categories': [sheet_name, pos_table_row + 1, pos_table_col, pos_table_row + pos_table_total_row, pos_table_col],
          #10 / 20 / 30
          #[0,0] --- [0,12]
          'values': [sheet_name, pos_table_row + 1, pos_table_col + col_index  + 1, pos_table_row + pos_table_total_row, pos_table_col + col_index + 1],
      })

    #4)Thêm chart vào file
    worksheet.insert_chart(pos_chart_row,pos_chart_col, chart)

  def draw_excel_column_chart_by_row_value(self,sheet_name,data_table,pos_table_row=0,pos_table_col=0,pos_chart_row=0,pos_chart_col=0,width=1000,height=250,title=''):
    #1) Dữ liệu
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2) Draw Excel
    chart = workbook.add_chart({'type': 'column','subtype': 'stacked'})
    chart.set_size({'width': width, 'height': height})
    chart.set_title({'name': title})

    #3) In dữ liệu chart
    #3.1)Số hàng, cố cột
    param_row_table = len(list(data_table.values())[0])
    param_col_table = len(data_table)

    #3.2)Tạo value trong chart
    for row in range(1,param_row_table + 1):   
      chart.add_series({
          #Google/Facebook/Ins
          'name' : [sheet_name, pos_table_row + row, pos_table_col],
          #2017年8月 / 2017年9月 / 2017年10月
          #[0,0] --- [0,12]
          'categories': [sheet_name, pos_table_row, pos_table_col + 1, pos_table_row, pos_table_col + param_col_table - 1],
          #10 / 20 / 30
          #[0,0] --- [0,12]
          'values': [sheet_name, pos_table_row + row, pos_table_col + 1, pos_table_row + row, pos_table_col + param_col_table - 1],
      })

    #4)Thêm chart vào file
    worksheet.insert_chart(pos_chart_row,pos_table_col, chart)


  def draw_excel_column_chart_by_column_value(self,sheet_name,data_table,pos_table_row=0,pos_table_col=0,pos_chart_row=0,pos_chart_col=0,width=550,height=250,title=''):
    #1) Lấy xlsx self.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2) Tạo đối tượng chart
    chart = workbook.add_chart({'type': 'column','subtype': 'stacked'})
    chart.set_size({'width': width, 'height': height})
    chart.set_title({'name': title})

    #3) In dữ liệu chart
    #3.1)Tổng Số cột của bảng
    param_col_table = len(data_table)
    param_row_table = len(list(data_table.values())[0])
    row_last_table = pos_table_row + param_row_table
    #3.2)Tạo value trong chart Giá trị lấy theo cột
    for col in range(1,param_col_table):   
        chart.add_series({
            'name' : [sheet_name, pos_table_row, col + 1],
            'categories': [sheet_name, pos_table_row + 1, pos_table_col, row_last_table, pos_table_col],
            'values': [sheet_name, pos_table_row + 1, col + 1, row_last_table, col + 1],
            })
        #3.2.1)Cho label xuống phía dưới
        chart.set_legend({'position': 'bottom'})

    #3.3) Thêm chart vào file
    worksheet.insert_chart(pos_chart_row,pos_chart_col, chart)   

  def draw_excel_line_chart_per_table_line(self,sheet_name,data_table,pos_table_row=0,pos_table_col=0,pos_chart_row=0,pos_chart_col=0):
    #1)Lấy xlsxself.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2)In dữ liệu chart
    #2.1)Số hàng, cố cột
    param_row_table = len(list(data_table.values())[0])#2
    param_col_table = len(data_table)#12

    #2.2)Tạo value trong chart
    #2.2.1)Độ dài của chart tính bằng col
    chart_row = 0
    for row in range(1,param_row_table + 1):
      #2.2.2) Tạo đối tượng chart
      chart = workbook.add_chart({'type': 'line'})
      chart.set_size({'width': 1000, 'height': 250})   
      chart.add_series({
          #Google/Facebook/Ins
          'name' : [sheet_name, pos_table_row + row, pos_table_col],
          #2017年8月 / 2017年9月 / 2017年10月
          #[0,0] --- [0,12]
          'categories': [sheet_name, pos_table_row, pos_table_col + 1, pos_table_row, pos_table_col + param_col_table - 1],
          #10 / 20 / 30
          #[0,0] --- [0,12]
          'values': [sheet_name, pos_table_row + row, pos_table_col + 1, pos_table_row + row, pos_table_col + param_col_table - 1],
      })

      #2.2.3)Thêm chart vào file
      worksheet.insert_chart(pos_chart_row + chart_row ,pos_chart_col, chart)
      chart_row += 14

  def draw_excel_table_with_border(self,sheet_name,data_table,pos_row = 0,pos_col = 0,header_bg_color="green",header_font_color="white",header=True,is_border=True):
    #1)Tạo pandas dataFrame từ date đầu vào
    table = pd.DataFrame(data_table)
    
    #2)chuyển từ dataFrame thành table trong excel
    table.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col,startrow=pos_row + 1,index=False,header=False)

    #3)Lấy 2 biến này để  thao tác vẽ và format
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #4) Header format
    if header:
      format_col = workbook.add_format({
        'align' : 'top',
        'valign' : 'center',
        'text_wrap' : False,
        'bold' : True,
        'border' : 1,
        #'bg_color' : header_bg_color,
        #'font_color': header_font_color,
        })

      format_col.set_font_name('游ゴシック')
      if is_border:
        format_col.set_bottom(1)
        format_col.set_left(1)
        format_col.set_border_color('#BFBFBF')
        format_col.set_bg_color('#D9D9D9')

      #2.3.1)THÊM FORMAT CHO HEADER
      for col_num, value in enumerate(table.columns.values):
        worksheet.write(pos_row, col_num+pos_col, value, format_col)

  def draw_excel_table_only(self,sheet_name,data_table,pos_row = 0,pos_col = 0,header_bg_color="green",header_font_color="white",header=True,is_border=True):
    #1)Tạo pandas dataFrame từ date đầu vào
    table = pd.DataFrame(data_table)
    
    #2)chuyển từ dataFrame thành table trong excel
    table.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col,startrow=pos_row + 1,index=False,header=False)

    if header:
      #2.2)Lấy 2 biến này để  thao tác vẽ và format
      workbook  = self.__writer.book
      worksheet = self.__writer.sheets[sheet_name] 

      #2.3)Thêm format
      format_col = workbook.add_format({
        'align' : 'top',
        'valign' : 'center',
        'text_wrap' : False,
        'bold' : True
        #'border' : 1,
        #'bg_color' : header_bg_color,
        #'font_color': header_font_color,
        })

      format_col.set_font_name('游ゴシック')
      if is_border:
        format_col.set_bottom(1)
        format_col.set_left(1)
        format_col.set_border_color('#BFBFBF')
        format_col.set_bg_color('#D9D9D9')

      #2.3.1)THÊM FORMAT CHO HEADER
      for col_num, value in enumerate(table.columns.values):
        worksheet.write(pos_row, col_num+pos_col, value, format_col)

  def draw_excel_description_box(self,sheet_name,header,body,first_row=0,first_col=0,last_row=5,last_col=5):
    #1) Lấy xlsxself.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2) Tạo format
    header_format = workbook.add_format({
    'color': '#F79C51',
    'bold' : True,
    'font_size': 20
    })
    body_format = workbook.add_format({
    'font_size': 12
    })
    merge_format = workbook.add_format({
    'bold':     True,
    'border':   6,
    'align':    'top',
    'text_wrap' : True,
    })

    #3) Viết ra file excel
    #3.1)Merge các cột các hàng lại thành 1 khung lớn
    worksheet.merge_range(first_row,first_col,last_row,last_col,'', merge_format)
    
    #3.2)Viết ra file excel kèm theo format cho từng chữ
    worksheet.write_rich_string(first_row,first_col,
                                header_format,header,
                                body_format,body,merge_format)

  def draw_excel_merge_range_left_align(self,sheet_name,text,first_row=0,first_col=0,last_row=2,last_col=2,bg_color="green",font_color='white'):
    #1) Lấy xlsxself.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2) Tạo format

    merge_format = workbook.add_format({
    'bold':     True,
    'align':    'left',
    'valign':   'vcenter',
    'text_wrap' : True,
    'font_color': font_color
    })

    #3) Viết ra file excel
    #3.1)Merge các cột các hàng lại thành 1 khung lớn
    worksheet.merge_range(first_row,first_col,last_row,last_col,text, merge_format)

  def draw_excel_fill_bg(self,sheet_name,text,row_index=0,col_index=0,bg_color="green",text_align='center', is_bold=True, font_color="black"):
    #1) Lấy xlsxself.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2) Tạo format

    col_format = workbook.add_format({
      'bold':     is_bold,
      'align':    text_align,
      'valign':   'vcenter',
      'text_wrap' : True,
      'bg_color': bg_color,
      'font_color': font_color,
      'border' : 1,
    })
    col_format.set_font_name('游ゴシック')

    #3) Viết ra file excel
    #3.1)Merge các cột các hàng lại thành 1 khung lớn
    worksheet.write(row_index, col_index, text, col_format)

  def draw_excel_merge_range(self,sheet_name,text,first_row=0,first_col=0,last_row=2,last_col=2,bg_color="green",font_color='white'):
    #1) Lấy xlsxself.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2) Tạo format

    merge_format = workbook.add_format({
    'bold':     True,
    'align':    'center',
    'valign':   'vcenter',
    'text_wrap' : True,
    'bg_color': bg_color,
    'font_color': font_color,
    'border' : 1,
    })

    #3) Viết ra file excel
    #3.1)Merge các cột các hàng lại thành 1 khung lớn
    worksheet.merge_range(first_row,first_col,last_row,last_col,text, merge_format)

  def draw_excel_merge_range_with_font_family(self,sheet_name,text,first_row=0,first_col=0,last_row=2,last_col=2,bg_color="green",font_color='white'):
    #1) Lấy xlsxself.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    #2) Tạo format

    merge_format = workbook.add_format({
    'bold':     True,
    'align':    'center',
    'valign':   'vcenter',
    'text_wrap' : True,
    'bg_color': bg_color,
    'font_color': font_color,
    'border' : 1,
    })
    merge_format.set_font_name('游ゴシック')

    #3) Viết ra file excel
    #3.1)Merge các cột các hàng lại thành 1 khung lớn
    worksheet.merge_range(first_row,first_col,last_row,last_col,text, merge_format)    
  
  def draw_excel_table_not_fomart_header(self,sheet_name,data_table,caption,row_caption,col_caption,pos_row = 0,pos_col = 0,header=True):
    #1)Số hàng, cố cột
    param_row_table = len(list(data_table.values())[0])#6
    param_col_table = len(data_table)#11

    #2)Tạo pandas dataFrame từ date đầu vào
    table = pd.DataFrame(data_table)

    #2.1)chuyển từ dataFrame thành table trong excel
    table.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col,startrow=pos_row + 1,index=False,header=header)
    #2.2)Lấy 2 biến này để  thao tác vẽ và format
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 

    #2.2.1) vẽ caption, thêm format
    worksheet.write(row_caption,col_caption,caption,None)
    worksheet.set_column(pos_col-1,pos_col+param_col_table,20)

  def draw_excel_column_chart_by_column_value_v2(self,sheet_name,data_table,row_firt_table,row_last_table,pos_table_col,pos_chart_row,pos_chart_col):
    # 1) Lấy xlsx self.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    # 2) Tạo đối tượng chart
    chart = workbook.add_chart({'type': 'column','subtype': 'stacked'})
    chart.set_size({'width': 700, 'height': 250})

    # 3) In dữ liệu chart

    # 3.1)Tổng Số cột của bảng
    param_col_table = len(data_table)

    # 3.2)Tạo value trong chart Giá trị lấy theo cột
    for col in range(1,param_col_table):   
        chart.add_series({
            # 2017年8月 / 2017年9月 / 2017年10月
            #[0:12]
            'name' : [sheet_name, row_firt_table, col + 1],
            # CEC/ROIT/PBC
            # [0,0] --- [12,0]
            'categories': [sheet_name, row_firt_table + 1, pos_table_col, row_last_table, pos_table_col],
            # 10 / 20 / 30
            # [0,0] --- [0,12]
            'values': [sheet_name, row_firt_table + 1, col + 1, row_last_table, col + 1],
            })
        #Cho label xuống phía dưới
        chart.set_legend({'position': 'bottom'})

    # 3.3) Thêm chart vào file
    worksheet.insert_chart(pos_chart_row,pos_chart_col, chart)  

  def draw_excel_table_only_has_merge_v1(self,sheet_name,data_table,pos_row = 0,pos_col = 0,header_bg_color="green",header_font_color="white",header=False,is_border=True,list_col_merge=[]):
    #1)Tạo pandas dataFrame từ date đầu vào
    table = pd.DataFrame(data_table)
    
    #2)chuyển từ dataFrame thành table trong excel
    table.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col,startrow=pos_row + 1,index=False)
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 
    if header:
      #2.2)Lấy 2 biến này để  thao tác vẽ và format
      #2.3)Thêm format
      format_col = workbook.add_format({
        'align' : 'top',
        'valign' : 'center',
        'text_wrap' : False,
        'bold' : True
        #'border' : 1,
        #'bg_color' : header_bg_color,
        #'font_color': header_font_color,
        })

      format_col.set_font_name('游ゴシック')
      if is_border:
        format_col.set_bottom(1)
        format_col.set_left(1)
        format_col.set_border_color('#BFBFBF')
        format_col.set_bg_color('#D9D9D9')

      #2.3.1)THÊM FORMAT CHO HEADER
      for col_num, value in enumerate(table.columns.values):
        worksheet.write(pos_row, col_num+pos_col, value, format_col)

    dict_merge_format = {'align': 'center', 'valign': 'vcenter', 'border': 1}
    merge_format = workbook.add_format(dict_merge_format)

    lastRow = len(table)

    color_bg_saturday = "#deeaf6"
    color_text_saturday = "#4472c4"
    color_bg_sunday = "#fbe4d5"
    color_text_sunday = "#ff0055"
    merge_format_saturday = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1,"font_color":color_text_saturday,'bg_color': color_bg_saturday})
    merge_format_sunday = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1,"font_color":color_text_sunday,'bg_color': color_bg_sunday})

    for value in list_col_merge:
      startCells = [1]

      for row in range(2,len(table)+1):
        if (table.loc[row-1,value["name"]] != table.loc[row-2,value["name"]]):
          startCells.append(row)


      for row in startCells:
        
        try:
          endRow = startCells[startCells.index(row)+1]-1 
          if row == endRow:
            if table.loc[row-1,value["name"]] == "土":
              worksheet.write(row + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format_saturday)
            elif table.loc[row-1,value["name"]] == "日":
              worksheet.write(row + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format_sunday)
            else:
              worksheet.write(row + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format)

          else:
            
            if table.loc[row-1,value["name"]] == "土":
              worksheet.merge_range(row + pos_row + 1, value["col"], endRow + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format_saturday)
            elif table.loc[row-1,value["name"]] == "日":
              worksheet.merge_range(row + pos_row + 1, value["col"], endRow + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format_sunday)
            else:
              worksheet.merge_range(row + pos_row + 1, value["col"], endRow + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format)

        except IndexError:
          if row == lastRow:
            
            if table.loc[row-1,value["name"]] == "土":
              worksheet.write(row + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format_saturday)
            elif table.loc[row-1,value["name"]] == "日":
              worksheet.write(row + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format_sunday)
            else:
              worksheet.write(row + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format)
          else:
            if table.loc[row-1,value["name"]] == "土":
               worksheet.merge_range(row + pos_row + 1, value["col"], lastRow + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format_saturday)
            elif table.loc[row-1,value["name"]] == "日":
               worksheet.merge_range(row + pos_row + 1, value["col"], lastRow + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format_sunday)
            else:
               worksheet.merge_range(row + pos_row + 1, value["col"], lastRow + pos_row + 1, value["col"], table.loc[row-1,value["name"]], merge_format)
             
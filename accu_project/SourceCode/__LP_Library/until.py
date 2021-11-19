import io
import json
import hashlib
import statistics
import requests,os
from PIL import Image
from datetime import datetime
from urllib.request import Request, urlopen
from main import settings
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.chrome.options import Options
import string, random
from _io import BytesIO
from collections import defaultdict

PATH_FOLDER_BLOG_IMAGE = settings.BASE_DIR + "/static/img/tinify/"

def remove_channel_name(name):
  channel_names = [
    '(BizApp)',
    '(Azure)',
    '(M365)',
    '(DX)',
    '(移行製品)',
    '(管理製品)'
  ]
  final_name = name
  for item in channel_names:
    final_name = final_name.replace(item, '')

  final_name.strip()

  return final_name
  
def get_day_subject_in_email():
  week_days = ("（月）","（火）","（水）","（木）","（金）","（土）","（日）")
  time_now = datetime.now()
  time_now_week_day = time_now.weekday()
  time_now_format = '{0}年{1}月{2}日{3}'.format(time_now.year, time_now.month, time_now.day,week_days[time_now_week_day]) 

  return time_now_format

def sql_query_cover_special_charater(input_string):
  input_string = input_string.replace("'","\\'")
  input_string = input_string.replace('"','\\"')

  return input_string

#sort_key = lambda x : x[1]['page_views']
def sort_dict_with_key(dct,_key,_reverse=False):
  dct = dct.items()
  dct = sorted(dct,key=_key,reverse=_reverse)
  dct = dict((key,value) for key,value in dct)
  return dct

def get_currency_rate_from_usd(currency_code):
  url = "https://api.exchangeratesapi.io/latest?base=USD"
  try:
    jsonurl = urlopen(url)
    rates = json.loads(jsonurl.read())["rates"]

    return rates[currency_code]
  except Exception as ins:
    print("Error",ins)
    return 0  

def get_currency_code_by_language(language_code):
  location_name = ''

  code_data = {
    "ja" : 'JPY',
    "us" : 'USD',
    "en" : 'USD',
    "vi" : 'USD',
  }
  
  if code_data.get(language_code):
    location_name = code_data[language_code]

  return location_name

def get_quartile_data(array):
  try:
    
    array = list(filter(lambda x: x != None, array))
    array.sort()
    total_element = len(array)
    median = statistics.median(array)
    lower_bound = 0
    upper_bound = 0
    if total_element % 2 == 0:
      center = int(total_element/2)
      lower_bound = statistics.median(array[0:center])
      upper_bound = statistics.median(array[center:])
    else:
      center = int(total_element/2)
      lower_bound = statistics.median(array[0:center])
      upper_bound = statistics.median(array[center+1:])
    safety_range =[lower_bound,upper_bound] 
    data = {
      'median' : median,
      'safety_range' : safety_range,
    }
    return data
  except Exception as ins:
    data = {
      'median' : 0,
      'safety_range' : [0,0],
    }
    return data

def extract_domain(domain):
  domain = domain.strip("/")
  domain = domain.replace("https://","")
  domain = domain.replace("http://","")
  domain = domain.replace("www.","")
  return domain

def get_md5_encryption(str_input = ""):
  """ 
  Input : String need encryption  (Type string)

  Output : md5 encryption like b'\xb1\n\x8d\xb1d\xe0uA\x05\xb7\xa9\x9b\xe7.?\xe5' (type Byte)
  """

  try:
    hash_object = hashlib.md5(str_input.encode())

    return hash_object.digest()
  except Exception as inst :
    print(inst)
    return None

def extract_image_from_pdf(URL_PDF="", is_crop = False):
  #Trên Linux để cài đc popler thì chạy lênh này ==>>>    $apt-get install poppler-utils
  # URL_PDF = "https://www.clouderp.jp/hubfs/resource/PDF/no-1-erp-ecommerce-psa-customer-management.pdf"
  path_file = "E:/MS-Portal/SourceCode/1.pdf"
  pages = convert_from_path(URL_PDF, dpi=500, single_file=True)
  if is_crop:
    # Nếu crop thumb thì resize lại ảnh cở 1000px
    pages = convert_from_path(URL_PDF, dpi=500, single_file=True, size=(1000,None))

  count = 1
  path_img = str(settings.BASE_DIR)   + '/static/img/test/'+'{}.jpg'.format(str(count))
  for page in pages:
    page.save( path_img, 'JPEG')
    break
  return {
    'path_img' : path_img
  }

def create_thumb_img(path_image, is_use_horizontal = False):
  now = datetime.now()


  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--ignore-certificate-errors')
  chrome_options.add_argument('--ignore-ssl-errors')
  if settings.CONFIG_ENV_TYPE == 'local':
  # chrome_driver_path = settings.BASE_DIR + '/__Security_Data/Chrome_driver/chromedriver_win32/chromedriver.exe'
    chrome_driver_path = ChromeDriverManager().install()
  else:
    chrome_driver_path = settings.BASE_DIR + '/__Security_Data/Chrome_driver/chromedriver_linux64/chromedriver'
  
  path_html_page_image = settings.CURRENT_URL + '/static/js_create_thumb_templates/index.html'
  if is_use_horizontal:
    print("use horizontal thumb templates")
    path_html_page_image = settings.CURRENT_URL + '/static/js_create_thumb_templates/slide.html'


  browser = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
  print(path_html_page_image, "path_html_page_image")
  
  browser.get(path_html_page_image)
  path_book_line = settings.CURRENT_URL + "/static/js_create_thumb_templates/img/book-line.png"

  #Thay ảnh thumb
  browser.execute_script('document.getElementById("img-book").src="' + path_image + '"')

  browser.maximize_window()
  browser.set_window_size(1920, 1080)


  import time
  time.sleep(3)
  element = browser.find_element_by_class_name("line-shadow-white") 
  # element = browser.find_element_by_id("thumb-img") 
  path_new_img = settings.BASE_DIR +'/static/img/test/'+ get_random_string(8) + "_thumb.png"
  element.screenshot(path_new_img)
  browser.close()                             
  browser.quit()

  result = tinify_from_url(settings.CURRENT_URL+'/static/img/test/'+path_new_img.split("/")[-1])
  print('create_thumb_img ++ result : ',result)
  if result : 
    os.remove(path_new_img)
  

  return {
    'path_img' : path_new_img if result == False else result['path_save']
  }



def get_random_string(length):
  # Random string with the combination of lower and upper case
  letters = string.ascii_letters
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str


def create_cta_img(path_html_file, class_take_screen="screenshot-cta"):
  now = datetime.now()

  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--ignore-certificate-errors')
  chrome_options.add_argument('--ignore-ssl-errors')
  if settings.CONFIG_ENV_TYPE == 'local':
  # chrome_driver_path = settings.BASE_DIR + '/__Security_Data/Chrome_driver/chromedriver_win32/chromedriver.exe'
    chrome_driver_path = ChromeDriverManager().install()
  else:
    chrome_driver_path = settings.BASE_DIR + '/__Security_Data/Chrome_driver/chromedriver_linux64/chromedriver'
  
  browser = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
  browser.maximize_window()

  browser.get(path_html_file)
  print(path_html_file, " +>>>>>>>>>>>>>>>>>>>>>>> path_html_file")
  # browser.get("data:text/html;charset=utf-8," + a)
  browser.set_window_size(1920, 1080)
  import time
  time.sleep(2)
  print("trungggggggggggggggg", browser)


  # element = browser.find_element_by_class_name("wrapper-img") 
  # element = browser.find_element_by_id("cta-banner-background")
  # #Đoạn này kiểm tra đã load xong font hay chưa
  check_loading_font = "loading"
  while check_loading_font != "loaded":
    print("first run to load font =>>>>>>>>>", check_loading_font)
    check_loading_font = browser.execute_script("""return document.fonts.status;""")
    print("after loading =>>>>>>>>>", check_loading_font)

  print("start take screen shot")

  element = browser.find_element_by_class_name(class_take_screen) 

  path_new_img = settings.BASE_DIR +'/static/img/test/'+ get_random_string(8) + "_cta.png"
  element.screenshot(path_new_img)
  browser.close()                            
  browser.quit()
  
  result = tinify_from_url(settings.CURRENT_URL+'/static/img/test/'+path_new_img.split("/")[-1])
  print('create_cta_img -- result : ',result)
  if result : 
    os.remove(path_new_img)

  return {
    'path_img' : path_new_img if result == False else result['path_save']
  }

def tinify_from_url(image_url, resize=750):
  try:
    tinify.key = "jDWynj5FBMnpGtNSN4QCqcms3m8S0gR5"
    #1)Kết nối API
    get_image = requests.get(image_url)
    #2)Xử lý
    #2.1)Ktra link tồn tại hay không
    if get_image.status_code != 200:
      return False

    #2.2)Ktra độ dài của ảnh
    img = Image.open(BytesIO(get_image.content))
    width = img.size[0]
    print('2222222222')
    #2.3)Cắt ảnh
    source = tinify.from_url(image_url)
    resized = source
    print('33333333')
    if resize and width > resize:
      resized = source.resize(
        width=resize
      )
    print('444444444')
    #3)Lưu ảnh
    file_names = image_url.split("/")[-1]
    path_save = PATH_FOLDER_BLOG_IMAGE + file_names
    resized.to_file(path_save)
    print('55555555')
    return {
      "width": width,
      "file_names": file_names,
      "path_save": path_save,
    }

  except Exception as e:
    print('exception ',e)
    return False


def create_thumb_html(html_data, is_use_horizontal = False):
  now = datetime.now()


  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--ignore-certificate-errors')
  chrome_options.add_argument('--ignore-ssl-errors')
  if settings.CONFIG_ENV_TYPE == 'local':
  # chrome_driver_path = settings.BASE_DIR + '/__Security_Data/Chrome_driver/chromedriver_win32/chromedriver.exe'
    chrome_driver_path = ChromeDriverManager().install()
  else:
    chrome_driver_path = settings.BASE_DIR + '/__Security_Data/Chrome_driver/chromedriver_linux64/chromedriver'
  
  path_html_page_image = settings.CURRENT_URL + '/static/js_create_thumb_templates/croppie.html'
  if is_use_horizontal:
    print("use horizontal thumb templates")
    path_html_page_image = settings.CURRENT_URL + '/static/js_create_thumb_templates/croppie.html'


  browser = webdriver.Chrome(chrome_driver_path, chrome_options=chrome_options)
  print(path_html_page_image, "path_html_page_image")
  
  browser.get(path_html_page_image)
  
  path_book_line = settings.CURRENT_URL + "/static/js_create_thumb_templates/img/book-line.png"


  #Thay ảnh thumb
  browser.execute_script("document.getElementById('result-crop').innerHTML='" + html_data + "'")

  JS_GET_HEIGHT = '''return Math.max( document.body.scrollHeight,
                            document.body.offsetHeight, 
                            document.documentElement.clientHeight,
                            document.documentElement.scrollHeight,  
                            document.documentElement.offsetHeight);'''
  height = browser.execute_script(JS_GET_HEIGHT)
  # browser.set_window_size(1280, height)
  browser.set_window_size(1920, height)
  
  import time
  time.sleep(3)
  # element = browser.find_element_by_class_name("wrapper-img") 
  element = browser.find_element_by_id("result-crop") 
  path_new_img = settings.BASE_DIR +'/static/img/test/'+ get_random_string(8) + "_thumb.png"
  # path_new_img = "D:/thumb1.png"
  element.screenshot(path_new_img)
  browser.close()                             
  browser.quit()

  result = tinify_from_url(settings.CURRENT_URL+'/static/img/test/'+path_new_img.split("/")[-1])
  print('create_thumb_img ++ result : ',result)
  if result : 
    os.remove(path_new_img)
  

  return {
    'path_img' : path_new_img if result == False else result['path_save']
  }


def dict_sum(*dicts) -> dict:
  """
  Cộng 2 dict theo key:
    Input:
      x = {'both1':10, 'both2':2, 'only_x': 100 }
      y = {'both1':10, 'both2': 20, 'only_y':200 }

    Use:
      dict_sum(x, y)

    Output: 
      {'both1': 20, 'both2': 22, 'only_x': 100, 'only_y': 200}


  """
  ret = defaultdict(int)
  for d in dicts:
    for k, v in d.items():
      ret[k] += v
  return dict(ret)


def hash_text(text, hashlen=12):
  import hashlib
  return hashlib.md5(text.encode("utf-8")).hexdigest()[:hashlen]

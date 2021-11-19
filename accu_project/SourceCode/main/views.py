from __Config.Include.Common_Include import *
import urllib.parse

def util(request):
  tmp_file = 'apps/docs/util.html'

  data = {

  }

  return render(request, tmp_file, data)

def docs(request):
  tmp_file = 'apps/docs/index.html'

  data = {

  }

  return render(request, tmp_file, data)

def guide(request):
  tmp_file = 'apps/guide/index.html'

  data = {

  }

  return render(request, tmp_file, data)

def download(request):
  if request.user.is_authenticated:
    filename = request.GET['file']
    #filename = 'サービスご利用ガイド_202106.pdf'
    file_path = settings.BASE_DIR + '/__Security_Data/guide/v2/{}'.format(filename)

    #2.3)Mở file
    f = open(file_path,'rb')

    #3)Download file về 
    response = HttpResponse(f, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
    response['Content-Disposition'] = 'attachment;filename={}'.format(urllib.parse.quote(filename))
    f.close()
    return response
  else:
    return HttpResponse('<center style="margin-top: 100px;">You don’t have permission to access this page.<br><a href="/accounts/login">Click here to Login</a></center>') 

def redirect_login(request):
  return redirect('/accounts/login')
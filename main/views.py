from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .utils import get_sftp_file_list, download_file


### 세션을
def login_check(request):
    return request.session.get('is_logged_in')

def main_page(request):
    # 로그인 확인
    if login_check(request):
        file_list = get_sftp_file_list(request.session.get('file_path'))
        return render(request, 'MainPage.html', {'file_list': file_list})
    else:
        return render(request, 'MainPage.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 단순 인증 로직 (예시)
        if username == 'admin' and password == '1234':
            request.session['is_logged_in'] = True
            request.session['file_path'] = '.'
        return redirect('home')
    return redirect('login')

@csrf_exempt
def download_item(request):
    if login_check(request):
        file_path = request.session.get('file_path')
        file_name = request.POST.get('file_name')
        print(f"download_file_path: {file_path}, file_name: {file_name}")

        file_stream = download_file(file_path, file_name)

        response = FileResponse(file_stream, as_attachment=True, filename=file_name)
        return response
    else:
        return redirect('login')

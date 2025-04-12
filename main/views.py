from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from .models import *

### 로그인 여부 확인
def login_check(request):
    return request.session.get('is_logged_in')

### 메인 페이지
def main_page(request):
    # 로그인 확인
    file_list = []
    if login_check(request):
        file_list = get_sftp_file_list(request.session.get('file_path'))

    return render(request, 'MainPage.html', {'file_list': file_list})


### 로그인
@csrf_exempt
def login(request):
    # POST 방식의 통신일 경우에만 로그인 시도
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # User 테이블에 계정이 있을경우 session 할당 및 로그인
        try:
            User.objects.get(name=username, password=password)
            request.session['is_logged_in'] = True
            request.session['file_path'] = '.'
            request.session['user_name'] = username

            return render(request, 'MainPage.html', {
                'user_name': request.session.get('user_name')
            })

        # User 테이블에 계정이 없을경우 error alert 실행
        except User.DoesNotExist:
            return render(request, "LoginPage.html", {
                'error': '아이디 또는 비밀번호가 일치하지 않습니다'
            })

    return render(request, 'LoginPage.html', {
        'user_name': ''
    })


# 로그아웃
@csrf_exempt
def logout(request):
    request.session.clear()

    return redirect('home')


# 파일 업/다운로드 로그 확인
@csrf_exempt
def logs(request):

    return redirect('home')


# 파일 다운로드 혹은 디렉토리 이동
@csrf_exempt
def download_item(request):
    if login_check(request):
        file_path = request.session.get('file_path')
        file_name = request.POST.get('file_name')

        # 파일 다운로드
        if len(file_name.split('.')) == 2:
            print(f"file_path: {file_path}, file_name: {file_name}")

            file_stream = download_file(file_path, file_name)

            # 브라우저에 저장된 경로로 파일 다운로드
            response = FileResponse(file_stream, as_attachment=True, filename=file_name)
            return response

        # 이전 디렉토리로 이동
        elif len(file_name.split('.')) == 3:
            file_path = file_path.split('/')

            # 마지막 이동 디렉토리 제거
            # 마지막 이동 디렉토리가 ./라면 제거하지 않음
            if len(file_path) > 1:
                del file_path[-1]

            file_path = '/'.join(file_path)
            request.session['file_path'] = file_path

            return redirect('home')

        # 디렉토리 이동
        else:
            print(f"{file_name} is dir")

            # 현재 경로에 이동 디렉토리 추가
            request.session['file_path'] += '/' + file_name

            return redirect('home')
    else:
        render(request, 'LoginPage.html')

import os

from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from NasWeb import settings
from .data_log import insert_log
from .utils import *
from .models import *
from .auth import *


### 메인 페이지
def main_page(request):
    # 로그인 확인
    file_list = []
    if login_check(request):
        file_list = get_sftp_file_list(request.session.get('file_path'))

    return render(request, 'MainPage.html',
                  {
                      'file_list': file_list,
                      'user_name': request.session['user_name']
                  })


### 로그인
@csrf_exempt
def login(request):

    if login_check(request):
        return redirect('home')
    else:
        # 로그인 페이지로 이동
        return render(request, 'LoginPage.html')


# 파일 업/다운로드 로그 확인
@csrf_exempt
def logs(request):

    if request.session.get('is_logged_in'):
        return redirect('log_proc')
    else:
        return render(request, 'LoginPage.html')


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
            try:
                response = FileResponse(file_stream, as_attachment=True, filename=file_name)
                if insert_log(request, file_name, "download"):
                    return response
                else:
                    return render(request, "MainPage.html", {
                        'error': '파일 다운로드에 실패했습니다.',
                        'file_list': get_sftp_file_list(request.session.get('file_path')),
                        'user_name': request.session['user_name']
                    })
            except Exception as e:
                return render(request, "MainPage.html", {
                    'error': '파일 다운로드에 실패했습니다.',
                    'file_list': get_sftp_file_list(request.session.get('file_path')),
                    'user_name': request.session['user_name']
                })

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


### 파일 업로드
@csrf_exempt
def upload_item(request):

    if login_check(request):
        if request.method == 'POST':
            files = request.FILES.getlist('upload_file')

            for file in files:
                upload_file_path = os.path.join(settings.BASE_DIR, 'file', file.name)
                remote_file_path = f"{request.session['file_path']}/{file.name}"
                print(f"file_path: {upload_file_path}")

                if upload_file(upload_file_path, file, remote_file_path):
                    print(f"{file} is uploaded successfully")
                    insert_log(request, file.name, "upload")
                    delete_file(upload_file_path)
                else:
                    print(f"{file} is uploaded failed")
                    delete_file(upload_file_path)

            return render(request, 'MainPage.html',
            {
                'file_list': get_sftp_file_list(request.session.get('file_path')),
                'user_name': request.session['user_name']
            })
        else:
            return redirect('home')

    else:
        return render(request, 'LoginPage.html')

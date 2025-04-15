### 로그인
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from main.models import User


### 로그인 여부 확인
def login_check(request):
    return request.session.get('is_logged_in')


### 로그인 프로세스
@csrf_exempt
def login_proc(request):
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


### 로그아웃
@csrf_exempt
def logout(request):
    request.session.clear()

    return redirect('home')
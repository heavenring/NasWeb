from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .utils import get_sftp_file_list

def main_page(request):
    if request.session.get('is_logged_in'):
        file_list = get_sftp_file_list('.')
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
        return redirect('home')
    return redirect('home')

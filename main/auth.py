### 로그인
import base64

from Cryptodome.Cipher import PKCS1_v1_5, AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import unpad
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from main.models import User

### 로그인 여부 확인
def login_check(request):
    return request.session.get('is_logged_in')


### RSA 키 생성
def get_public_key(request):
    # RSA 키 생성
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # 세션에 Private Key 저장
    request.session['private_key'] = private_key.decode('utf-8')

    # 공개키는 클라이언트로 전송 (PEM 포맷)
    return HttpResponse(public_key.decode('utf-8'), content_type='text/plain')


### e2e 복호화
def decrypt_login_data(request):
    e2e_data = request.POST.get('e2e_data')
    aes_key = request.POST.get('aes_key')
    aes_iv = request.POST.get('aes_iv')

    # 2. RSA 개인키로 AES 키 복호화
    private_key = request.session.get('private_key')
    cipher_rsa = PKCS1_v1_5.new(RSA.import_key(private_key))
    aes_key_base64 = cipher_rsa.decrypt(base64.b64decode(aes_key), None)
    aes_key = base64.b64decode(aes_key_base64)

    # 3. AES-CBC 복호화로 로그인 정보 획득
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv=base64.b64decode(aes_iv))
    decrypted_data = cipher_aes.decrypt(base64.b64decode(e2e_data))
    decrypted_login_data = unpad(decrypted_data, AES.block_size)

    login_data = decrypted_login_data.decode('utf-8').split('&&&&')

    return login_data[0], login_data[1]


### 로그인 프로세스
@csrf_exempt
def login_proc(request):
    # POST 방식의 통신일 경우에만 로그인 시도
    if request.method == 'POST':

        user_name, password = decrypt_login_data(request)
        # User 테이블에 계정이 있을경우 session 할당 및 로그인
        try:
            User.objects.get(name=user_name, password=password)
            request.session['is_logged_in'] = True
            request.session['file_path'] = '.'
            request.session['user_name'] = user_name

            return redirect('home')

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
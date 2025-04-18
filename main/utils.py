import os
from io import BytesIO

import paramiko
from decouple import config
from django.views.static import directory_index


### ssh 접속 정보
def ssh_info():
    return config('ssh_host'), int(config('ssh_port')), config('ssh_user'), config('ssh_pwd')


### 파일 다운로드
def download_file(filepath, filename):
    host, port, username, password = ssh_info()

    remote_path = f"{filepath}/{filename}"

    print('ssh connect try')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    print('ssh connect success')

    print(f'file download try')
    sftp = ssh.open_sftp()
    with sftp.file(remote_path, 'rb') as remote_file:
        file_data = remote_file.read()

    sftp.close()
    ssh.close()
    print(f'file download success')

    return BytesIO(file_data)  # 파일 스트림 반환


### 파일 업로드
def upload_file(upload_file_path, upload_file, remote_file_path):
    host, port, username, password = ssh_info()

    try:
        with open(upload_file_path, 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)
    except FileNotFoundError:
        print('file not found')
        return False

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)

        sftp = ssh.open_sftp()
        sftp.put(upload_file_path, remote_file_path)
        sftp.close()
        ssh.close()
    except paramiko.ssh_exception.SSHException:
        print('ssh connect fail')
        return False

    return True


### 업로드 성공한 파일 삭제
def delete_file(upload_file_path):
    try:
        os.remove(upload_file_path)
        print(f"delete file: {upload_file_path}")
    except FileNotFoundError:
        print(f"delete file not found: {upload_file_path}")


### sftp를 통해 nas에 있는 파일 목록 조회
def get_sftp_file_list(dir_path):
    # ssh 접속 정보 획득
    host, port, username, password = ssh_info()

    file_list = ['..'] # web에 출력할 file 리스트
    try:
        # sftp 연결 시도
        print('sftp connect try')
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        print('sftp connect success')

        # 숨김파일을 제외한 파일 조회
        black_file_list = config('black_file').split(',')
        for item in sftp.listdir_attr(dir_path):
            if not (item.filename.startswith('.') or item.filename in black_file_list):
                full_path = f"{dir_path}/{item.filename}"
                print(f'sftp file: {item.filename}, full path: {full_path}')
                file_list.append(item.filename)

        sftp.close()
        transport.close()
    except Exception as e:
        file_list.append((f"Error: {e}", None))
    return file_list
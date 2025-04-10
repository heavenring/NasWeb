import paramiko
from decouple import config
from django.views.static import directory_index


def download_file(filepath, filename, download_dir):

    hostname = config('ssh_host')
    port = config('ssh_port')
    username = config('ssh_user')
    password = config('ssh_pwd')

    remote_path = f"{filepath}/{filename}"

    print('ssh connect try')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    print('ssh connect success')

    print(f'file download try')
    sftp = ssh.open_sftp()
    sftp.get(remote_path, download_dir)
    sftp.close()
    ssh.close()
    print(f'file download success')

    return download_dir


def upload_file(upload_file_path, remote_path):
    hostname = config('ssh_host')
    port = config('ssh_port')
    username = config('ssh_user')
    password = config('ssh_pwd')

    with open(upload_file_path, 'wb+') as destination:
        for chunk in remote_path.chunks():
            destination.write(chunk)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    sftp = ssh.open_sftp()
    sftp.put(upload_file_path, remote_path)
    sftp.close()
    ssh.close()
import paramiko

def check_perms():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.200', username='utking', password='Oxford18.')
        
        stdin, stdout, stderr = client.exec_command('ls -la /var/lib/squeezeboxserver/cache/updates')
        print("LMS Cache Updates Directory:")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_perms()

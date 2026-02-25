import paramiko

def check_perms():
    lms_server_ip = '10.1.1.200'
    lms_server_user = 'utking'
    lms_server_pass = 'Oxford18.'
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(lms_server_ip, username=lms_server_user, password=lms_server_pass)
        
        print("Checking directory permissions...")
        stdin, stdout, stderr = client.exec_command("ls -ld /var/lib/squeezeboxserver/cache/updates")
        print("Updates Dir:", stdout.read().decode().strip())
        
        stdin, stdout, stderr = client.exec_command("groups")
        print("User groups:", stdout.read().decode().strip())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_perms()

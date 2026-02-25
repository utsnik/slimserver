import paramiko

def main():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.200', username='utking', password='Oxford18.', timeout=10)
        
        print("Successfully connected to LMS server (10.1.1.200)")
        stdin, stdout, stderr = client.exec_command("ls -ld /var/lib/squeezeboxserver/cache")
        print("Cache Dir:", stdout.read().decode().strip())
        
        stdin, stdout, stderr = client.exec_command("mkdir -p /var/lib/squeezeboxserver/cache/updates")
        print("Created/Verified updates directory.")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

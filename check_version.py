import paramiko

def main():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.60', username='root', password='1234', timeout=10)
        
        stdin, stdout, stderr = client.exec_command("cat /etc/squeezeos.version")
        out = stdout.read().decode()
        print("SqueezeOS Version currently running:\n", out.strip())
        
        client.close()
    except Exception as e:
        print(f"Error connecting: {e}")

if __name__ == "__main__":
    main()

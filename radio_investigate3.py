import paramiko

def main():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.60', username='root', password='1234', timeout=10)
        
        print("--- checking /usr/bin/upgrade ---")
        stdin, stdout, stderr = client.exec_command("ls -lh /usr/bin/upgrade")
        print(stdout.read().decode())
        
        stdin, stdout, stderr = client.exec_command("head -n 20 /usr/bin/upgrade")
        out = stdout.read().decode()
        err = stderr.read().decode()
        if out: print(out)
        if err: print("head error:", err)
        
        print("\n--- Disk space ---")
        stdin, stdout, stderr = client.exec_command("df -h")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

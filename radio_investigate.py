import paramiko

def main():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.60', username='root', password='1234', timeout=10)
        
        print("--- /usr/bin/upgrade ---")
        stdin, stdout, stderr = client.exec_command("cat /usr/bin/upgrade")
        print(stdout.read().decode())
        
        print("\n--- /var/log/messages (last 50 lines) ---")
        stdin, stdout, stderr = client.exec_command("tail -n 50 /var/log/messages")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

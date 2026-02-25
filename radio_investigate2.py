import paramiko

def main():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.60', username='root', password='1234', timeout=10)
        
        print("--- File type of /usr/bin/upgrade ---")
        stdin, stdout, stderr = client.exec_command("ls -la /usr/bin/upgrade && file /usr/bin/upgrade 2>/dev/null || echo 'no file command'")
        print(stdout.read().decode())
        
        print("\n--- Upgrade Logs in /tmp ---")
        stdin, stdout, stderr = client.exec_command("ls -la /tmp/*upgrade* /var/log/*upgrade* 2>/dev/null")
        print(stdout.read().decode())
        
        print("\n--- dmesg (last 20 lines) ---")
        stdin, stdout, stderr = client.exec_command("dmesg | tail -n 20")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

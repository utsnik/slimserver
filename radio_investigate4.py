import paramiko

def main():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.60', username='root', password='1234', timeout=10)
        
        print("--- mount points ---")
        stdin, stdout, stderr = client.exec_command("mount")
        print(stdout.read().decode())
        
        print("\n--- locating 'upgrade' binary ---")
        stdin, stdout, stderr = client.exec_command("which upgrade")
        print(stdout.read().decode())
        
        print("\n--- checking free space explicitly on /tmp ---")
        stdin, stdout, stderr = client.exec_command("df -h /tmp")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

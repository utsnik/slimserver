import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        cmd = "grep -A 3 -B 3 -i 'wpa-supplicant' /tmp/squeezeos_build_baby_v9.log | grep -i 'patch\\|error\\|fail'"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("\n--- Grep Output ---")
        print(stdout.read().decode())
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

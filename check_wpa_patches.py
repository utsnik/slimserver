import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        cmd = "ls -la /home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/wpa-supplicant/wpa-supplicant-2.10/"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("\n--- Patch Files ---")
        print(stdout.read().decode())
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

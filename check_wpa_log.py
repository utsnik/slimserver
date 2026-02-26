import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        # Build the find command to locate the log file
        cmd = "find /home/utking/squeezeos-build/src/poky/build/tmp-baby/work/ -path '*wpa-supplicant*' -name 'log.do_patch*' | head -n 1"
        stdin, stdout, stderr = client.exec_command(cmd)
        log_path = stdout.read().decode().strip()
        
        if log_path:
            print(f"Located log: {log_path}")
            # Cat the contents
            stdin, stdout, stderr = client.exec_command(f"cat {log_path}")
            print("\n--- Log Contents ---")
            print(stdout.read().decode())
        else:
            print("Log not found.")
            
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

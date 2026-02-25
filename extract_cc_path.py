import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        # Script to run inside docker
        inner_script = """
cd poky
. ./poky-init-build-env ../build > /dev/null 2>&1
MACHINE=baby bitbake -e openssl | grep "^CC="
"""
        # Save script to a temporarily file in the volume
        sftp = client.open_sftp()
        with sftp.file('/home/utking/squeezeos-build/src/get_cc_path.sh', 'w') as f:
            f.write(inner_script)
        sftp.close()
        
        # Run the script inside docker
        cmd = "docker run --rm -v /home/utking/squeezeos-build/src:/home/squeezeos squeezeos_builder /bin/bash /home/squeezeos/get_cc_path.sh"
        stdin, stdout, stderr = client.exec_command(cmd)
        
        print("\n--- Bitbake CC Environment ---")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

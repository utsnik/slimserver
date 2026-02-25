import paramiko
import os

def main():
    try:
        # 1. Download from 10.1.4.164
        build_host = '10.1.4.164'
        build_user = 'utking'
        build_key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        print(f"Connecting to build server {build_host}...")
        client1 = paramiko.SSHClient()
        client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client1.connect(build_host, username=build_user, key_filename=build_key_path)
        
        sftp1 = client1.open_sftp()
        remote_bin = '/home/utking/squeezeos-build/src/poky/build/tmp-baby/deploy/images/baby_9.0.2_r17111.bin'
        remote_ver = '/home/utking/squeezeos-build/src/poky/build/tmp-baby/deploy/images/baby.version'
        
        local_bin = 'baby.bin'
        local_ver = 'baby.version'
        
        print("Downloading baby_9.0.2_r17111.bin as baby.bin...")
        sftp1.get(remote_bin, local_bin)
        print("Downloading baby.version...")
        sftp1.get(remote_ver, local_ver)
        
        sftp1.close()
        client1.close()
        
        print("Download complete.")
        
        # 2. Upload to 10.1.1.200
        lms_host = '10.1.1.200'
        lms_user = 'utking'
        lms_password = 'Oxford18.'
        
        print(f"Connecting to LMS server {lms_host}...")
        client2 = paramiko.SSHClient()
        client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client2.connect(lms_host, username=lms_user, password=lms_password)
        
        # We upload to home directory first, then use sudo to move them to the correct spot
        sftp2 = client2.open_sftp()
        print("Uploading to /home/utking/...")
        sftp2.put(local_bin, '/home/utking/baby.bin')
        sftp2.put(local_ver, '/home/utking/baby.version')
        sftp2.close()
        
        print("Moving files to /var/lib/squeezeboxserver/cache/updates...")
        commands = [
            "echo 'Oxford18.' | sudo -S mkdir -p /var/lib/squeezeboxserver/cache/updates",
            "echo 'Oxford18.' | sudo -S mv /home/utking/baby.bin /var/lib/squeezeboxserver/cache/updates/baby.bin",
            "echo 'Oxford18.' | sudo -S mv /home/utking/baby.version /var/lib/squeezeboxserver/cache/updates/baby.version",
            "echo 'Oxford18.' | sudo -S chown -R squeezeboxserver:squeezeboxserver /var/lib/squeezeboxserver/cache/updates",
            "echo 'Oxford18.' | sudo -S chmod 777 /var/lib/squeezeboxserver/cache/updates/*"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = client2.exec_command(cmd)
            stdout.read() # Wait for command to finish
            err = stderr.read().decode()
            if err and "password for" not in err.lower():
                print(f"Warning/Error: {err}")
                
        client2.close()
        print("Deployment to 10.1.1.200 complete!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

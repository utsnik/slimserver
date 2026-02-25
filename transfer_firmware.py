import paramiko
import os

def transfer():
    build_server_ip = '10.1.4.164'
    build_server_user = 'utking'
    key_path = r'C:\Users\Igland\.ssh\oracle_key'
    
    lms_server_ip = '10.1.1.200'
    lms_server_user = 'utking'
    lms_server_pass = 'Oxford18.'
    
    remote_src_dir = '/home/utking/squeezeos-build/src/poky/build/tmp-fab4/deploy/images/'
    remote_dest_dir = '/var/lib/squeezeboxserver/cache/updates/'
    
    files = ['custom.fab4.bin', 'custom.fab4.version']
    temp_dir = 'temp_fw'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    try:
        # 1. Download from build server
        print(f"Connecting to build server {build_server_ip}...")
        build_client = paramiko.SSHClient()
        build_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        build_client.connect(build_server_ip, username=build_server_user, key_filename=key_path)
        
        build_sftp = build_client.open_sftp()
        for f in files:
            print(f"Downloading {f}...")
            build_sftp.get(remote_src_dir + f, os.path.join(temp_dir, f))
        build_sftp.close()
        build_client.close()
        
        # 2. Upload to LMS server
        print(f"Connecting to LMS server {lms_server_ip}...")
        lms_client = paramiko.SSHClient()
        lms_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        lms_client.connect(lms_server_ip, username=lms_server_user, password=lms_server_pass)
        
        lms_sftp = lms_client.open_sftp()
        for f in files:
            print(f"Uploading {f} to {remote_dest_dir}...")
            lms_sftp.put(os.path.join(temp_dir, f), remote_dest_dir + f)
            # Set permissions to be readable by squeezeboxserver user
            lms_sftp.chmod(remote_dest_dir + f, 0o644)
        lms_sftp.close()
        
        # Try to change ownership if via sudo (needs password interactively usually, but let's try 644 first)
        print("Finalizing permissions...")
        lms_client.exec_command(f"chmod 644 {remote_dest_dir}custom.fab4.*")
        
        lms_client.close()
        print("Transfer complete!")
        
    except Exception as e:
        print(f"Error during transfer: {e}")

if __name__ == "__main__":
    transfer()

import paramiko
import os
import time

def deploy():
    lms_server_ip = '10.1.1.200'
    lms_server_user = 'utking'
    lms_server_pass = 'Oxford18.'
    
    remote_tmp_dir = '/tmp/'
    remote_dest_dir = '/var/lib/squeezeboxserver/cache/updates/'
    
    files = ['custom.fab4.bin', 'custom.fab4.version']
    temp_dir = 'temp_fw'
    
    try:
        print(f"Connecting to LMS server {lms_server_ip}...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(lms_server_ip, username=lms_server_user, password=lms_server_pass)
        
        sftp = client.open_sftp()
        for f in files:
            local_path = os.path.join(temp_dir, f)
            remote_tmp_path = remote_tmp_dir + f
            print(f"Uploading {f} to {remote_tmp_path}...")
            sftp.put(local_path, remote_tmp_path)
        sftp.close()
        
        # Now move using sudo
        for f in files:
            remote_tmp_path = remote_tmp_dir + f
            remote_dest_path = remote_dest_dir + f
            print(f"Moving {remote_tmp_path} to {remote_dest_path} via sudo...")
            
            # Use sudo -S to read password from stdin
            command = f"echo '{lms_server_pass}' | sudo -S mv {remote_tmp_path} {remote_dest_path}"
            stdin, stdout, stderr = client.exec_command(command)
            # Wait for execution
            stdout.channel.recv_exit_status()
            
            # Fix ownership
            print(f"Changing ownership of {remote_dest_path} to squeezeboxserver...")
            command = f"echo '{lms_server_pass}' | sudo -S chown squeezeboxserver:nogroup {remote_dest_path}"
            stdin, stdout, stderr = client.exec_command(command)
            stdout.channel.recv_exit_status()

        print("Verifying files in destination...")
        stdin, stdout, stderr = client.exec_command(f"ls -la {remote_dest_dir}")
        print(stdout.read().decode())
        
        client.close()
        print("Deployment successful!")
        
    except Exception as e:
        print(f"Error during deployment: {e}")

if __name__ == "__main__":
    deploy()

import paramiko
import os

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        # We need to copy the patch into the squeezeplay recipe directory
        # and create a bbappend to apply it.
        squeezeplay_dir = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezeplay/'
        client.exec_command(f'mkdir -p {squeezeplay_dir}')
        
        # 1. Copy patch
        stdin, stdout, stderr = client.exec_command(f'cp /home/utking/squeezeos-build/src/radio_snappiness_full.patch {squeezeplay_dir}')
        stdout.channel.recv_exit_status()
        
        # 2. Create bbappend
        bbappend_file = squeezeplay_dir + 'squeezeplay_svn.bbappend'
        
        bbappend_content = """FILESEXTRAPATHS_prepend := "${THISDIR}:"
SRC_URI += "file://radio_snappiness_full.patch"
"""
        sftp = client.open_sftp()
        with sftp.file(bbappend_file, 'w') as f:
            f.write(bbappend_content)
            
        print("Created squeezeplay_svn.bbappend to inject Lua optimizations.")
        
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

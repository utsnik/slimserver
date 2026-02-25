import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        sftp = client.open_sftp()
        
        # Upload new patch
        local_patch = 'radio_snappiness_v9.patch'
        remote_patch = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezeplay/files/radio_snappiness_v9.patch'
        sftp.put(local_patch, remote_patch)
        print(f"Uploaded {local_patch} to {remote_patch}")
        
        # Update recipe
        bb_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezeplay/squeezeplay_svn.bb'
        with sftp.file(bb_file, 'r') as f:
            content = f.read().decode()
            
        new_content = content.replace('radio_snappiness_full.patch', 'radio_snappiness_v9.patch')
        
        with sftp.file(bb_file, 'w') as f:
            f.write(new_content)
        print("Updated squeezeplay_svn.bb to use radio_snappiness_v9.patch")
            
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

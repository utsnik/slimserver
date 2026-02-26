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
        bb_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezeplay/squeezeplay_svn.bb'
        
        with sftp.file(bb_file, 'r') as f:
            content = f.read().decode()
            
        old_func = """def squeezeos_squeezeplay_revision(d):
	import bb, os
	return open(os.path.join(bb.data.getVar('STAGING_DIR_TARGET', d, 1), 'squeezeos_squeezeplay_revision'), 'r').readline().strip()"""

        new_func = """def squeezeos_squeezeplay_revision(d):
	import bb, os
	path = os.path.join(bb.data.getVar('STAGING_DIR_TARGET', d, 1), 'squeezeos_squeezeplay_revision')
	if os.path.exists(path):
		return open(path, 'r').readline().strip()
	return "00000" """

        if old_func in content:
            new_content = content.replace(old_func, new_func)
            with sftp.file(bb_file, 'w') as f:
                f.write(new_content)
            print("Successfully patched squeezeos_squeezeplay_revision function for robustness")
        else:
            print("Function signature changed or already patched")
            
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

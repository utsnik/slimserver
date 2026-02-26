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
        bb_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/wpa-supplicant/wpa-supplicant_2.10.bb'
        
        try:
            with sftp.file(bb_file, 'r') as f:
                content = f.read().decode()
                
            # Remove the offending line from SRC_URI
            patched_content = content.replace('\tfile://0001-Enable-TLSv1.0-by-default.patch;patch=1;pnum=0 \\\n', '')
            
            if patched_content != content:
                with sftp.file(bb_file, 'w') as f:
                    f.write(patched_content)
                print(f"Patched {bb_file} by removing 0001 patch reference.")
            else:
                print("Patch reference not found, recipe might already be clean.")
                
            # Let's also remove the bbappend we created as it might be causing parse errors
            bbappend_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/wpa-supplicant/wpa-supplicant_2.10.bbappend'
            try:
                sftp.remove(bbappend_file)
                print(f"Removed problematic bbappend: {bbappend_file}")
            except Exception as e:
                print(f"bbappend not found or could not be removed: {e}")
                
        except Exception as e:
            print(f"Error accessing recipe: {e}")

        sftp.close()
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

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
        bbappend_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/wpa-supplicant/wpa-supplicant_2.10.bbappend'
        
        # We'll just define SRC_URI to remove the offending patch string
        bbappend_content = """# The 0001 patch file is empty and causes patch(1) to prompt/fail in automated builds
SRC_URI := "${@oe_filter_out('file://0001-Enable-TLSv1.0-by-default.patch;patch=1;pnum=0', '${SRC_URI}', d)}"
"""
        with sftp.file(bbappend_file, 'w') as f:
            f.write(bbappend_content)
        print(f"Created {bbappend_file}")
            
        sftp.close()
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

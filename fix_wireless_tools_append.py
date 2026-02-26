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
        
        # Create a bbappend file to override the dead HP SRC_URI
        # The base SRC_URI is "http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/wireless_tools.29.tar.gz file://man.patch;patch=1 ..."
        bbappend_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/wireless-tools/wireless-tools_29.bbappend'
        
        # We rewrite SRC_URI entirely to use a Debian archive mirror for v29, keeping the local patches
        bbappend_content = """# Override dead HP Labs mirror
SRC_URI = "http://archive.ubuntu.com/ubuntu/pool/universe/w/wireless-tools/wireless-tools_29.orig.tar.gz \\
           file://man.patch;patch=1 \\
           file://wireless-tools.if-pre-up \\
           file://zzz-wireless.if-pre-up"
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

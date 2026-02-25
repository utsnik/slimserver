import paramiko

def main():
    try:
        host = '10.1.1.200'
        user = 'utking'
        password = 'Oxford18.'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password)
        
        # Determine OS and find Cache/updates
        stdin, stdout, stderr = client.exec_command('uname -a')
        os_info = stdout.read().decode()
        print(f"Server OS info: {os_info}")
        
        # Try to find the updates Cache directory
        print("Searching for Lyrion/Squeezebox Cache/updates directory...")
        # Check some common places first to be fast
        common_paths = [
            "/var/lib/squeezeboxserver/cache",
            "/var/lib/logitechmediaserver/cache",
            "/opt/logitechmediaserver/cache",
            "/opt/lms/cache"
        ]
        
        found_cache = ""
        for path in common_paths:
            stdin, stdout, stderr = client.exec_command(f"ls -d {path}")
            if stdout.read().decode().strip():
                found_cache = path
                break
                
        if not found_cache:
            # If not found in common, search
            stdin, stdout, stderr = client.exec_command("find / -type d -name 'updates' -path '*/Cache/*' -o -path '*/cache/*' 2>/dev/null | head -n 1")
            found_cache = stdout.read().decode().strip()
            
        if not found_cache:
            stdin, stdout, stderr = client.exec_command("find / -type d -name 'updates' 2>/dev/null | grep -i 'squeezebox\|logitech\|lms\|lyrion' | head -n 1")
            found_cache = stdout.read().decode().strip()
            
        if found_cache:
            print(f"Found updates directory: {found_cache}")
        else:
            print("Could not find the updates directory. We will just create one in the home directory for now.")
            found_cache = "/home/utking/updates"
            client.exec_command(f"mkdir -p {found_cache}")
            
        client.close()
    except Exception as e:
        print(f"Error connecting to 10.1.1.200: {e}")

if __name__ == "__main__":
    main()

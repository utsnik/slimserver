import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        # Test command to see include search paths
        # We use a dummy file and -v -E to see the search list
        cmd = """docker run --rm -v /home/utking/squeezeos-build/src:/home/squeezeos squeezeos_builder /bin/bash -c "
echo '#include <stdio.h>' > test.c
arm-none-linux-gnueabi-gcc --sysroot=/home/squeezeos/poky/build/tmp-baby/staging/armv5te-none-linux-gnueabi -v -E test.c -o /dev/null 2>&1 | grep -A 20 '#include <...>'
" """
        
        stdin, stdout, stderr = client.exec_command(cmd)
        print("\n--- Header Search Paths ---")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        # 1. Kill the running container
        stdin, stdout, stderr = client.exec_command("docker kill $(docker ps -q)")
        print("Kill output:", stdout.read().decode())
        
        # 2. Append thread optimizations to the template that gets copied when trigger_build_robust runs!
        # The script does: cp build/conf/local.conf.sample ../build/conf/local.conf
        # So we must append it to local.conf.sample or explicitly to the end of the script!
        
        sftp = client.open_sftp()
        local_conf_sample = '/home/utking/squeezeos-build/src/poky/build/conf/local.conf.sample'
        try:
            with sftp.file(local_conf_sample, 'r') as f:
                content = f.read().decode()
            if 'BB_NUMBER_THREADS = "16"' not in content:
                content += '\nPARALLEL_MAKE = "-j 16"\nBB_NUMBER_THREADS = "16"\n'
                with sftp.file(local_conf_sample, 'w') as f:
                    f.write(content)
                print("Appended threading to local.conf.sample")
            else:
                print("Threading already exists in local.conf.sample")
        except Exception as e:
            print(f"Error touching conf: {e}")
            
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

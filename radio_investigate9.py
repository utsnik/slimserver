import paramiko

def main():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.60', username='root', password='1234', timeout=10)
        
        stdin, stdout, stderr = client.exec_command("cat /usr/share/jive/applets/SetupFirmwareUpgrade/UpgradeUBI.lua | grep 'cmd' -B 2 -A 5")
        print(stdout.read().decode())
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

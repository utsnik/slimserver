import paramiko

def main():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.60', username='root', password='1234', timeout=10)
        sftp = client.open_sftp()
        
        files = ['UpgradeUBI.lua', 'SetupFirmwareUpgradeApplet.lua']
        base_path = '/usr/share/jive/applets/SetupFirmwareUpgrade/'
        
        for f in files:
            print(f"--- {f} ---")
            with sftp.file(base_path + f, 'r') as fh:
                content = fh.read().decode()
                # Print lines related to fw_setenv, upgrade, os., flash
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'fw_setenv' in line or 'os.' in line or '/bin/' in line or 'system(' in line or 'popen(' in line or 'flash' in line.lower():
                        print(f"{i+1}: {line.strip()}")
        
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

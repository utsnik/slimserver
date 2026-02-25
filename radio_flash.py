import paramiko
import sys
import time

def main():
    try:
        print("Connecting to Squeezebox Radio (10.1.1.60)...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('10.1.1.60', username='root', password='1234', timeout=10)
        
        # We need to run the wget command from the python HTTP server we started earlier
        # since SCP from build server requires sshpass which had interactive issues.
        print("Downloading fab4.bin via HTTP to /tmp...")
        stdin, stdout, stderr = client.exec_command("wget -O /tmp/fab4.bin http://10.1.4.164:8080/fab4.bin")
        err = stderr.read().decode()
        if "error" in err.lower() or "failed" in err.lower():
            print("Wget error:", err)
        
        print("Stopping rc.jive...")
        client.exec_command("/etc/init.d/rc.jive stop")
        time.sleep(2)
        
        print("Executing /usr/bin/upgrade...")
        stdin, stdout, stderr = client.exec_command("/usr/bin/upgrade /tmp/fab4.bin")
        out = stdout.read().decode()
        print("Upgrade output:", out)
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

import paramiko

def run_cmd(client, cmd):
    print(f"Running: {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out: print("STDOUT:", out)
    if err: print("STDERR:", err)

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('10.1.1.60', username='root', password='1234', timeout=10)
    
    run_cmd(client, "find /usr/share/jive -name '*Update*' -o -name '*Upgrade*'")
    run_cmd(client, "find /etc/init.d -name '*upgrade*' -o -name '*update*'")
    run_cmd(client, "grep -ir upgrade /usr/share/jive/applets/ | head -n 20")
    run_cmd(client, "ls -la /usr/sbin/ | grep -i fw")
    client.close()
except Exception as e:
    print(f"Error: {e}")

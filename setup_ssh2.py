import paramiko
import sys

host = '10.1.4.164'
username = 'utking'
password = 'Oxford18.'
pub_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCpYDDjwCVkM/XXMdLc/OjGqXliALRM9TVIlv1nC7Jzwm1dgxd13TahLhojww48WNYeSmz2V4ZPEhIdXbIePfhyNS8ACpYDN1ZOew0AE2xZjDX72zDBbxYG0CpfAvxQ1bylg2mOVN/wagUj7tYjAM6w6hX7k8EnsVdmY8z7vY2o3WSqDvSWy6Y9zpLOr9/A298Vdjja+PKvfzcOB0svz8td3E82mVp8QmSWaSD8YQNVy7bD7bJWk0EroyJ8qQ+7gAcOuTXYwJSuY2VPB3XBhJ6TgXGmfz45wm4tHa7EVQm/Nh7FlbMb4Uc/vcufIvj3Kr8a2KkmuRcNt33WIVYkryTIGisxdLbGmqB6ufqBMyIPSrX/+kI/QQs7o01mXYFG1QgVFGt0jARaG4wKpd1SwdFdJZT23rsDrZEOGaYifk9C/maJDjJRt5UJfyVzxvZF4EXjSM8nG4R9AZZqZv04EMhn88o3uU+EhVysafqgAzcwod71fNR9lSlBjigdZJNSAxE= utking@download-server\n'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, username=username, password=password)
    
    # Create .ssh directory
    ssh.exec_command('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
    
    # Append public key to authorized_keys
    stdin, stdout, stderr = ssh.exec_command('cat >> ~/.ssh/authorized_keys')
    stdin.write(pub_key)
    stdin.close()
    
    # Ensure correct permissions
    ssh.exec_command('chmod 600 ~/.ssh/authorized_keys')
    
    print("Successfully installed SSH key on " + host)
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
finally:
    ssh.close()

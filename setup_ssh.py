import paramiko
import sys

host = '10.1.4.164'
username = 'utking'
password = 'Oxford18.'
pub_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4F4W1L3URjIyOP4XR5XA9E6Li5TUCAQr2UeqMvoUOpsorVgBRFsJruO5E/TxooU650P+ATUp8jkA56ijOhjiQou1bin2F6eSxGWWmJsNUWRQkYHAt4fS4PeIMAIAWYvp3grlShdbIG7ifI26Z8q8P3hWOqmlYyx5tXgwSxBjD2zShVwRvXVciIp8o9L0P1fgnlRiCxpBlo6Dl1NKaIBFUWB1ryZqBpiry4FragTAMIWQY/9r4kAKASHd1x6oHPwfWxe56CWJqBzNTJ+hGoJnsA4nWjhBagfz3Qga/Sc8BTFETATWwLdC9nbZZioN+WGgNBBU18wvQn+UEHZkxOC/P redlight-oracle\n'

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

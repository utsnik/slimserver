import paramiko
import re

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        sftp = client.open_sftp()
        
        # 1. Squeezecenter Fix
        sc_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezecenter/squeezecenter_svn.bb'
        with sftp.file(sc_file, 'r') as f:
            content = f.read().decode()
        
        if 'for i in ${INCLUDED_PLUGINS}; do' in content and 'if [ -e ' not in content:
            new_loop = """	for i in ${INCLUDED_PLUGINS}; do
		if [ -e ${D}/${prefix}/squeezecenter/Slim/Plugin.tmp/$i ]; then
			mv ${D}/${prefix}/squeezecenter/Slim/Plugin.tmp/$i ${D}/${prefix}/squeezecenter/Slim/Plugin
		else
			echo "Plugin $i not found in Plugins.tmp, skipping"
		fi
	done"""
            content = re.sub(r'\tfor i in \$\{INCLUDED_PLUGINS\}; do.*?\tdone', new_loop, content, flags=re.DOTALL)
            with sftp.file(sc_file, 'w') as f:
                f.write(content)
            print("Patched squeezecenter_svn.bb with robust plugin loop")

        # 2. libdbd-sqlite-perl Fix
        dbd_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/perl/libdbd-sqlite-perl_1.34.bb'
        with sftp.file(dbd_file, 'r') as f:
            content = f.read().decode()
        
        if 'libdbi-perl-native (> 1.614)' in content:
            content = content.replace('libdbi-perl-native (> 1.614)', 'libdbi-perl-native')
            with sftp.file(dbd_file, 'w') as f:
                f.write(content)
            print("Patched libdbd-sqlite-perl_1.34.bb to ignore DBI version constraint")

        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

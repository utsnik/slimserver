import paramiko

def main():
    try:
        host = '10.1.4.164'
        user = 'utking'
        key_path = r'C:\Users\Igland\.ssh\oracle_key'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path)
        
        sftp = client.open_sftp()
        
        # 1. wpa-supplicant Fix
        wpa_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/wpa-supplicant/wpa-supplicant_2.10.bb'
        with sftp.file(wpa_file, 'r') as f:
            content = f.read().decode()
        
        # Remove the missing patches and fix SRC_URI
        # The V9 build was failing because 'file://0001-Enable-TLSv1.0-by-default.patch' was missing
        bad_patches = [
            'file://0001-Enable-TLSv1.0-by-default.patch;patch=1;pnum=0',
            'file://0002-Tweak-D-Bus-systemd-service-activation-configuration.patch;patch=1;pnum=0',
            'file://0003-Add-IgnoreOnIsolate-yes-to-keep-wpa-supplicant-runni.patch;patch=1;pnum=0',
            'file://0004-Allow-legacy-renegotiation-to-fix-PEAP-issues-with-s.patch;patch=1;pnum=0',
            'file://0005-OpenSSL-Drop-security-level-to-0-with-OpenSSL-3.0-wh.patch;patch=1;pnum=0',
            'file://0006-Disable-Werror-for-eapol_test.patch;patch=1;pnum=0',
            'file://0007-nl80211-add-extra-ies-only-if-allowed-by-driver.patch;patch=1;pnum=0',
            'file://0008-AP-guard-FT-SAE-code-with-CONFIG_IEEE80211R_AP.patch;patch=1;pnum=0',
            'file://0009-OpenSSL-Apply-connection-flags-before-reading-certif.patch;patch=1;pnum=0',
            'file://0010-Don-t-upgrade-SSL-security-level-to-1-when-setting-c.patch;patch=1;pnum=0',
            'file://0011-Add-reload-support-to-the-systemd-unit-files.patch;patch=1;pnum=0',
            'file://0012-WNM-Choose-the-best-available-BSS-not-just-the-first.patch;patch=1;pnum=0',
            'file://0013-wpa_supplicant-Fix-wpa_supplicant-configuration-pars.patch;patch=1;pnum=0',
            'file://0014-Abort-ongoing-scan.patch;patch=1;pnum=0',
            'file://0015-Override-ieee80211w-from-pmf-for-AP-mode-in-wpa_supp.patch;patch=1;pnum=0'
        ]
        
        for p in bad_patches:
            content = content.replace(p, '')
            
        with sftp.file(wpa_file, 'w') as f:
            f.write(content)
        print("Cleaned up wpa-supplicant_2.10.bb patches")

        # 2. Upload Snappiness Patch
        patch_path = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezeplay/squeezeplay/radio_snappiness_full.patch'
        # Create dir if not exists
        client.exec_command('mkdir -p /home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezeplay/squeezeplay')
        
        patch_content = """--- a/src/ui/jive_framework.c
+++ b/src/ui/jive_framework.c
@@ -19,1 +19,1 @@
-#define HORIZONTAL_PUSH_TRANSITION_DURATION 500
+#define HORIZONTAL_PUSH_TRANSITION_DURATION 200
"""
        with sftp.file(patch_path, 'w') as f:
            f.write(patch_content)
        
        # 3. Patch squeezeplay.bb to use it
        sq_file = '/home/utking/squeezeos-build/src/poky/meta-squeezeos/packages/squeezeplay/squeezeplay_svn.bb'
        with sftp.file(sq_file, 'r') as f:
            sq_content = f.read().decode()
            
        if 'radio_snappiness_full.patch' not in sq_content:
            sq_content = sq_content.replace('file://logconf.lua"', 'file://logconf.lua \\\n\tfile://radio_snappiness_full.patch;patch=1"')
            with sftp.file(sq_file, 'w') as f:
                f.write(sq_content)
            print("Patched squeezeplay_svn.bb with snappiness patch")

        sftp.close()
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

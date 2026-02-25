import re
import os

def clean_patch(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    skip_hunk = False
    
    # Files to keep (relative to squeezeplay/ directory)
    allowed_files = [
        'share/jive/ui/SimpleMenu.lua',
        'share/jive/ui/Window.lua',
        'src/ui/jive.h',
        'src/ui/jive_framework.c'
    ]

    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for new file header
        if line.startswith('diff --git'):
            # Strip src/squeezeplay/ prefix
            line = line.replace('a/src/squeezeplay/', 'a/').replace('b/src/squeezeplay/', 'b/')
            
            # Check if file is allowed
            match = re.search(r'b/(\S+)', line)
            if match:
                current_file = match.group(1)
                if current_file in allowed_files:
                    skip_hunk = False
                else:
                    skip_hunk = True
            
            if not skip_hunk:
                new_lines.append(line)
        elif line.startswith('--- a/src/squeezeplay/'):
            if not skip_hunk:
                new_lines.append(line.replace('--- a/src/squeezeplay/', '--- a/'))
        elif line.startswith('+++ b/src/squeezeplay/'):
            if not skip_hunk:
                new_lines.append(line.replace('+++ b/src/squeezeplay/', '+++ b/'))
        elif not skip_hunk:
            # Check for invalid hunks within allowed files
            # For jive_framework.c, we MUST NOT include the HORIZONTAL_PUSH_TRANSITION_DURATION hunk
            if 'jive_framework.c' in locals().get('current_file', ''):
                if '-#define HORIZONTAL_PUSH_TRANSITION_DURATION' in line:
                    # Skip this specific hunk
                    # We need to backtrack and remove the hunk header if possible, 
                    # but easiest is to just search ahead for the next hunk or file
                    while i < len(lines) and not (lines[i].startswith('@@') or lines[i].startswith('diff')):
                        i += 1
                    i -= 1 # adjust for the while loop increment
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        i += 1

    with open(output_path, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    clean_patch(r'Firmware\patches\radio_snappiness_full.patch', 'radio_snappiness_v9.patch')
    print("Cleaned patch saved to radio_snappiness_v9.patch")

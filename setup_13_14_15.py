import os
import glob
import re

for i in [13, 14, 15]:
    src = f"Series-Dai-So-To-Hop/.github/workflows/render-comb{i}-v2.yml"
    dst = f".github/workflows/render-comb{i}-v2.yml"
    with open(src, "r") as f:
        content = f.read()

    # Add working directory
    if "defaults:" not in content:
        content = re.sub(r'(timeout-minutes:\s*\d+\n)', r'\1    defaults:\n      run:\n        working-directory: Series-Dai-So-To-Hop\n', content)
    
    # Fix artifact paths
    lines = content.split('\n')
    new_lines = []
    in_path_block = False
    for line in lines:
        if line.strip() == "path: |":
            in_path_block = True
            new_lines.append(line)
        elif in_path_block:
            if line.strip() in ["if-no-files-found: warn", "if-no-files-found: error", "retention-days: 7"] or not line.startswith(" " * 12):
                in_path_block = False
                new_lines.append(line)
            else:
                if line.strip() and not "Series-Dai-So-To-Hop/" in line:
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(" " * indent + "Series-Dai-So-To-Hop/" + line.lstrip())
                else:
                    new_lines.append(line)
        else:
            new_lines.append(line)
    
    content = '\n'.join(new_lines)

    # Add default fallbacks for inputs
    default_voice = 'on'
    if 'default: \'off\'' in content or 'default: "off"' in content or 'default: off' in content:
        default_voice = 'off'
    content = content.replace("${{ inputs.voice }}", "${{ inputs.voice || '" + default_voice + "' }}")
    content = content.replace("${{ inputs.quality == 'preview' }}", "${{ inputs.quality == 'preview' || github.event_name == 'push' }}")
    
    with open(dst, "w") as f:
        f.write(content)

    print(f"Processed {src} -> {dst}")

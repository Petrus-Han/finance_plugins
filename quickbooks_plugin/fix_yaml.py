#!/usr/bin/env python3
"""Fix missing human_description in tool YAML files."""
import os
import re
from pathlib import Path

def fix_yaml_file(filepath: Path) -> bool:
    """Add human_description after label if missing."""
    content = filepath.read_text()
    lines = content.split('\n')
    new_lines = []
    modified = False
    i = 0

    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        # Check if this is a label block with en_US and zh_Hans
        if re.match(r'^(\s+)label:\s*$', line):
            indent = re.match(r'^(\s+)', line).group(1)
            param_indent = indent

            # Collect label block
            i += 1
            en_us_val = None
            zh_hans_val = None

            while i < len(lines) and (lines[i].startswith(indent + '  ') or lines[i].strip() == ''):
                new_lines.append(lines[i])
                if 'en_US:' in lines[i]:
                    en_us_val = lines[i].split('en_US:')[1].strip()
                if 'zh_Hans:' in lines[i]:
                    zh_hans_val = lines[i].split('zh_Hans:')[1].strip()
                i += 1

            # Check if next non-empty line is human_description
            peek_idx = i
            while peek_idx < len(lines) and lines[peek_idx].strip() == '':
                peek_idx += 1

            if peek_idx < len(lines) and 'human_description:' not in lines[peek_idx]:
                # Need to add human_description
                if en_us_val and zh_hans_val:
                    new_lines.append(f'{param_indent}human_description:')
                    new_lines.append(f'{param_indent}  en_US: {en_us_val}')
                    new_lines.append(f'{param_indent}  zh_Hans: {zh_hans_val}')
                    modified = True
                    print(f"  Added human_description: {en_us_val}")

            continue

        i += 1

    if modified:
        filepath.write_text('\n'.join(new_lines))

    return modified


def main():
    tools_dir = Path(__file__).parent / 'tools'

    for yaml_file in sorted(tools_dir.glob('*.yaml')):
        print(f"\nProcessing {yaml_file.name}...")
        if fix_yaml_file(yaml_file):
            print(f"  ✓ Fixed {yaml_file.name}")
        else:
            print(f"  - No changes needed")


if __name__ == '__main__':
    main()

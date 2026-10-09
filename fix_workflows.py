from pathlib import Path
import re

for i in [6, 7, 8]:
    file_path = Path(f'/Users/admin/Kho-Code-Manim/.github/workflows/render-stat{i:02d}.yml')
    content = file_path.read_text()
    
    # Add write permissions
    content = content.replace('  contents: read', '  contents: write')
    
    # Add working-directory
    if 'defaults:' not in content:
        content = content.replace('    steps:', '    defaults:\n      run:\n        working-directory: Manim-Typst/series-thong-ke\n    steps:')
    
    # Move Unit Tests AFTER Prepare... but before Smoke render
    # First, cut the Unit test block
    unit_test_regex = r'      - name: Unit tests.*?\n(.*?)(?=\n      - name: Compile)'
    unit_test_match = re.search(unit_test_regex, content, re.DOTALL)
    if unit_test_match:
        unit_test_block = unit_test_match.group(0) + '\n'
        content = content.replace(unit_test_block, '')
        
        # Insert after Prepare...
        prepare_regex = r'      - name: Prepare.*?\n.*?run:.*?\n'
        prepare_match = re.search(prepare_regex, content)
        if prepare_match:
            insert_idx = prepare_match.end()
            content = content[:insert_idx] + unit_test_block + content[insert_idx:]

    # Fix artifact paths
    content = re.sub(r'path: \|\n\s+media/videos', 'path: |\n            Manim-Typst/series-thong-ke/media/videos', content)
    content = content.replace('artifacts/stat', 'Manim-Typst/series-thong-ke/artifacts/stat')
    content = content.replace(f'STAT{i:02d}_vi.srt', f'Manim-Typst/series-thong-ke/STAT{i:02d}_vi.srt')
    content = content.replace(f'stat{i:02d}/runtime_plan.json', f'Manim-Typst/series-thong-ke/stat{i:02d}/runtime_plan.json')
    content = content.replace(f'preview/stat{i:02d}/', f'Manim-Typst/series-thong-ke/preview/stat{i:02d}/')
    
    # Add Youtube steps
    if 'Auto Upload Full HD to YouTube' not in content:
        youtube_block = f"""
      - name: Auto Upload Full HD to YouTube (Public)
        if: ${{{{ inputs.quality == 'fullhd' }}}}
        env:
          YOUTUBE_CLIENT_ID: ${{{{ secrets.YOUTUBE_CLIENT_ID }}}}
          YOUTUBE_CLIENT_SECRET: ${{{{ secrets.YOUTUBE_CLIENT_SECRET }}}}
          YOUTUBE_REFRESH_TOKEN: ${{{{ secrets.YOUTUBE_REFRESH_TOKEN }}}}
        run: |
          python -m pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
          VIDEO=$(find media/videos -type f -name 'STAT{i:02d}.mp4' | head -n 1)
          python ../../scripts/upload_to_youtube.py \\
            --file "$VIDEO" \\
            --series thong_ke \\
            --lesson {i} \\
            --category-id 27 \\
            --privacy public
      - name: Commit and Push YouTube History
        if: ${{{{ inputs.quality == 'fullhd' }}}}
        run: |
          git config --global user.name "GitHub Actions Bot"
          git config --global user.email "actions@github.com"
          git add ../../youtube_uploaded_history.json
          git commit -m "docs(stat{i:02d}): auto-update youtube_uploaded_history.json" || echo "No changes to commit"
          git push
"""
        content += youtube_block
        
    file_path.write_text(content)

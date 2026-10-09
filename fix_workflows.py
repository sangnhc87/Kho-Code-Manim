import os
import glob

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Add working-directory if not present
    if 'working-directory: Series-Dai-So-To-Hop' not in content:
        # Find where jobs: render: steps: is
        # The structure is:
        # jobs:
        #   render:
        #     runs-on: ubuntu-latest
        #     timeout-minutes: 180
        #     steps:
        
        replacement = """jobs:
  render:
    runs-on: ubuntu-latest
    timeout-minutes: 180
    defaults:
      run:
        working-directory: Series-Dai-So-To-Hop
    steps:"""
        
        if 'jobs:\n  render:\n    runs-on: ubuntu-latest\n    timeout-minutes: 180\n    steps:' in content:
            content = content.replace(
                'jobs:\n  render:\n    runs-on: ubuntu-latest\n    timeout-minutes: 180\n    steps:',
                replacement
            )
        else:
            print(f"Warning: Could not find jobs signature in {filepath}")

    # Fix upload-artifact paths
    # The paths block looks like:
    #          path: |
    #            media/videos/**/COMB02.mp4
    #            qa_comb02_v2/
    #            narration_COMB02_v2.md
    #            subtitles_COMB02_v2.srt
    #            voice/comb02_voice_manifest.json
    
    # We want to replace lines inside `path: |` by prepending `Series-Dai-So-To-Hop/` to them.
    # We can just replace the specific known strings:
    replacements = [
        ('media/videos/**/COMB', 'Series-Dai-So-To-Hop/media/videos/**/COMB'),
        ('qa_comb', 'Series-Dai-So-To-Hop/qa_comb'),
        ('narration_COMB', 'Series-Dai-So-To-Hop/narration_COMB'),
        ('subtitles_COMB', 'Series-Dai-So-To-Hop/subtitles_COMB'),
        ('voice/comb', 'Series-Dai-So-To-Hop/voice/comb')
    ]
    for old, new in replacements:
        # Make sure we only replace if it's not already replaced
        # Actually it's simpler to just do standard string replacement
        content = content.replace('\n            ' + old, '\n            ' + new)

    with open(filepath, 'w') as f:
        f.write(content)

workflows = glob.glob('.github/workflows/render-comb*-v2.yml')
for wf in workflows:
    process_file(wf)
    print(f"Processed {wf}")

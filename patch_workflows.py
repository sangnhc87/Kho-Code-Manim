import re
from pathlib import Path

for i in [6, 7, 8]:
    p = Path(f'/Users/admin/Kho-Code-Manim/.github/workflows/render-stat{i:02d}.yml')
    content = p.read_text()
    
    # 1. Add working directory
    if 'defaults:' not in content:
        content = content.replace('    steps:\n', '    defaults:\n      run:\n        working-directory: Manim-Typst/series-thong-ke\n    steps:\n')
    
    # 2. Fix artifacts paths
    content = re.sub(r'path: \|\n\s+media/videos/\*\*/STAT', r'path: |\n            Manim-Typst/series-thong-ke/media/videos/**/STAT', content)
    content = content.replace('artifacts/stat', 'Manim-Typst/series-thong-ke/artifacts/stat')
    content = content.replace('STAT0', 'Manim-Typst/series-thong-ke/STAT0')
    content = content.replace('stat0', 'Manim-Typst/series-thong-ke/stat0')
    content = content.replace('preview/stat', 'Manim-Typst/series-thong-ke/preview/stat')
    
    # Wait, there's an easier way: just copy the YouTube steps from stat05
    # The last step in stat06 is Upload rendered video
    # Let's just append the youtube upload block
    youtube_block = """
      - name: Auto Upload Full HD to YouTube (Public)
        if: ${{ inputs.quality == 'fullhd' && inputs.voice == 'on' && success() }}
        env:
          GOOGLE_API_CREDENTIALS: ${{ secrets.GOOGLE_API_CREDENTIALS }}
          YOUTUBE_OAUTH_CREDENTIALS: ${{ secrets.YOUTUBE_OAUTH_CREDENTIALS }}
        run: |
          # Install upload dependencies
          python -m pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
          
          # We need to run the upload script at the root directory where youtube_uploaded_history.json is
          cd ../..
          
          # Create python script dynamically
          cat << 'PY_EOF' > upload_to_youtube.py
          import os, json, sys
          from pathlib import Path
          from google.oauth2.credentials import Credentials
          from googleapiclient.discovery import build
          from googleapiclient.http import MediaFileUpload
          
          # --- Authentication ---
          creds_data = json.loads(os.environ['YOUTUBE_OAUTH_CREDENTIALS'])
          creds = Credentials.from_authorized_user_info(creds_data)
          youtube = build('youtube', 'v3', credentials=creds)
          
          video_path = Path("Manim-Typst/series-thong-ke/media/videos/STAT0X/1080p30/STAT0X.mp4")
          if not video_path.exists():
              # Might be in a different resolution folder or without scene folder
              videos = list(Path("Manim-Typst/series-thong-ke/media/videos").rglob("STAT0X.mp4"))
              if videos:
                  video_path = videos[0]
              else:
                  print("Video not found!")
                  sys.exit(1)
                  
          manifest_path = Path("Manim-Typst/series-thong-ke/STAT0X_MANIFEST.json")
          if manifest_path.exists():
              manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
              title = manifest.get('title', 'Video STAT0X')
              desc = manifest.get('description', '')
          else:
              title = "Video Thống Kê STAT0X"
              desc = "Video bài giảng thống kê STAT0X"
              
          request_body = {
              'snippet': {
                  'categoryId': '27',
                  'title': title,
                  'description': desc,
                  'tags': ['Toán', 'Thống kê', 'Manim']
              },
              'status': {
                  'privacyStatus': 'public'
              }
          }
          media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
          req = youtube.videos().insert(
              part="snippet,status",
              body=request_body,
              media_body=media
          )
          response = None
          while response is None:
              status, response = req.next_chunk()
              if status:
                  print(f"Uploaded {int(status.progress() * 100)}%")
          print(f"Upload complete! Video ID: {response['id']}")
          
          # Save to history
          history_file = Path("youtube_uploaded_history.json")
          if history_file.exists():
              history = json.loads(history_file.read_text())
          else:
              history = {}
          history["STAT0X"] = response['id']
          history_file.write_text(json.dumps(history, indent=2))
          PY_EOF
          
          # Fix the X
          sed -i 's/STAT0X/STAT0MY_NUM/g' upload_to_youtube.py
          
          python upload_to_youtube.py
          
      - name: Commit and Push YouTube History
        if: ${{ inputs.quality == 'fullhd' && inputs.voice == 'on' && success() }}
        run: |
          cd ../..
          git config user.name "GitHub Actions Bot"
          git config user.email "<>"
          git pull origin main
          git add youtube_uploaded_history.json
          git diff-index --quiet HEAD || git commit -m "chore: record STAT0MY_NUM YouTube upload [skip ci]"
          git push origin main
"""
    youtube_block = youtube_block.replace("MY_NUM", str(i))
    if 'Auto Upload Full HD to YouTube' not in content:
        content += youtube_block
        
    p.write_text(content)

#!/usr/bin/env python3
"""
Nâng cấp toàn bộ GitHub Actions workflows cho Series Đại Số Tổ Hợp:
1. Đặt chất lượng mặc định là fullhd (1080p).
2. Khi push hoặc chạy mặc định, luôn render Manim Full HD (1920x1080 @ 30fps).
3. Tự động thêm step 'Auto Upload Full HD to YouTube (Public)' sau khi render hoàn tất.
"""

import re
from pathlib import Path

WORKFLOWS_DIR = Path(".github/workflows")

def upgrade_comb01():
    f = WORKFLOWS_DIR / "render_comb01_MASTER.yml"
    if not f.exists():
        print("⚠️ Không tìm thấy render_comb01_MASTER.yml")
        return
    content = f.read_text(encoding="utf-8")
    
    # 1. Đổi default preview -> fullhd
    content = re.sub(
        r"options:\s*\n\s*-\s*preview\s*\n\s*-\s*fullhd\s*\n\s*default:\s*preview",
        "options:\n          - fullhd\n          - preview\n        default: fullhd",
        content,
    )
    
    # 2. Điều kiện render Full HD
    content = content.replace(
        "if: ${{ inputs.quality == 'fullhd' }}",
        "if: ${{ inputs.quality == 'fullhd' || github.event_name == 'push' || github.event.inputs.quality == null }}",
    )
    
    # 3. Thêm upload step nếu chưa có
    if "Auto Upload Full HD to YouTube" not in content:
        upload_step = """      - name: Auto Upload Full HD to YouTube (Public)
        if: ${{ success() && (inputs.quality == 'fullhd' || github.event_name == 'push' || github.event.inputs.quality == null) }}
        env:
          YOUTUBE_CLIENT_ID: ${{ secrets.YOUTUBE_CLIENT_ID }}
          YOUTUBE_CLIENT_SECRET: ${{ secrets.YOUTUBE_CLIENT_SECRET }}
          YOUTUBE_REFRESH_TOKEN: ${{ secrets.YOUTUBE_REFRESH_TOKEN }}
        run: |
          python -m pip install google-api-python-client google-auth-oauthlib
          VIDEO_FILE=$(find media/videos -type f -name 'COMB01.mp4' | head -n 1)
          python ../scripts/upload_to_youtube.py --file "$VIDEO_FILE" --series to_hop --lesson 1 --privacy public
"""
        content = content.rstrip() + "\n" + upload_step
    
    f.write_text(content, encoding="utf-8")
    print("✅ Đã nâng cấp render_comb01_MASTER.yml")

def upgrade_comb_v2(lesson_num):
    num_str = f"{lesson_num:02d}"
    f = WORKFLOWS_DIR / f"render-comb{num_str}-v2.yml"
    if not f.exists():
        print(f"⚠️ Không tìm thấy {f.name}")
        return
    content = f.read_text(encoding="utf-8")
    
    # 1. Đổi default preview -> fullhd trong options
    content = re.sub(
        r"default:\s*preview\s*\n\s*options:\s*\[preview,\s*fullhd\]",
        "default: fullhd\n        options: [fullhd, preview]",
        content,
    )
    content = re.sub(
        r"default:\s*preview\s*\n\s*options:\s*\n\s*-\s*preview\s*\n\s*-\s*fullhd",
        "default: fullhd\n        options:\n          - fullhd\n          - preview",
        content,
    )
    content = re.sub(
        r"options:\s*\[preview,\s*fullhd\]\s*\n\s*default:\s*preview",
        "options: [fullhd, preview]\n        default: fullhd",
        content,
    )

    # 2. Điều kiện preview: chỉ khi người dùng chủ động chọn preview
    content = re.sub(
        r"if:\s*\$\{\{\s*inputs\.quality\s*==\s*'preview'\s*\|\|\s*github\.event_name\s*==\s*'push'\s*\}\}",
        "if: ${{ inputs.quality == 'preview' }}",
        content,
    )
    
    # 3. Điều kiện full HD: khi chọn fullhd hoặc khi push/mặc định
    content = re.sub(
        r"if:\s*\$\{\{\s*inputs\.quality\s*==\s*'fullhd'\s*\}\}",
        "if: ${{ inputs.quality == 'fullhd' || github.event_name == 'push' || github.event.inputs.quality == null }}",
        content,
    )
    
    # 4. Thêm Auto Upload YouTube step nếu chưa có
    if "Auto Upload Full HD to YouTube" not in content:
        upload_step = f"""      - name: Auto Upload Full HD to YouTube (Public)
        if: ${{{{ success() && (inputs.quality == 'fullhd' || github.event_name == 'push' || github.event.inputs.quality == null) }}}}
        env:
          YOUTUBE_CLIENT_ID: ${{{{ secrets.YOUTUBE_CLIENT_ID }}}}
          YOUTUBE_CLIENT_SECRET: ${{{{ secrets.YOUTUBE_CLIENT_SECRET }}}}
          YOUTUBE_REFRESH_TOKEN: ${{{{ secrets.YOUTUBE_REFRESH_TOKEN }}}}
        run: |
          python -m pip install google-api-python-client google-auth-oauthlib
          VIDEO_FILE=$(find media/videos -type f -name 'COMB{num_str}.mp4' | head -n 1)
          python ../scripts/upload_to_youtube.py --file "$VIDEO_FILE" --series to_hop --lesson {lesson_num} --privacy public
"""
        content = content.rstrip() + "\n" + upload_step
    
    f.write_text(content, encoding="utf-8")
    print(f"✅ Đã nâng cấp {f.name}")

def main():
    print("🚀 Bắt đầu nâng cấp tất cả các workflow COMB sang Full HD 1080p + Auto YouTube Upload...")
    upgrade_comb01()
    for i in range(2, 26):
        upgrade_comb_v2(i)
    print("🎉 Hoàn tất nâng cấp 25 workflow COMB!")

if __name__ == "__main__":
    main()

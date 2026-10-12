#!/usr/bin/env python3
"""
Script upload video lên Facebook Reels cho Trang (Facebook Page) tự động.
Hỗ trợ tích hợp với GitHub Actions và quy trình render Manim.
Sử dụng curl subprocess để đảm bảo độ tin cậy, tốc độ cao và vượt qua lỗi chứng chỉ SSL trên macOS/Linux.

Tác giả: Thầy Nguyễn Văn Sang
Trang mặc định: ConicTypst (Page ID: 1249523211575010)
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
HISTORY_FILE = REPO_ROOT / "facebook_uploaded_history.json"
GRAPH_API_VERSION = "v20.0"


def run_curl(args: list[str], timeout: int = 60) -> dict:
    cmd = ["curl", "-s", "--max-time", str(timeout)] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Lệnh curl thất bại ({res.returncode}): {res.stderr.strip()}")
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"raw": res.stdout.strip()}


def load_history() -> dict:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_history(history: dict):
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def get_token(args_token: str | None) -> str:
    token = args_token or os.environ.get("FB_PAGE_ACCESS_TOKEN")
    if not token:
        # Fallback secrets file nếu chạy local
        for p in [REPO_ROOT / ".facebook_secrets.json", Path.home() / ".facebook_secrets.json"]:
            if p.exists():
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    token = data.get("access_token") or data.get("page_access_token")
                    if token:
                        break
                except Exception:
                    pass
    if not token:
        print("❌ Thiếu FB_PAGE_ACCESS_TOKEN! Vui lòng set biến môi trường FB_PAGE_ACCESS_TOKEN hoặc truyền --token.")
        sys.exit(1)
    return token.strip()


def get_page_info(token: str, page_id: str | None = None) -> tuple[str, str]:
    target_id = page_id or os.environ.get("FB_PAGE_ID") or "me"
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{target_id}?fields=id,name&access_token={token}"
    data = run_curl([url])
    if "error" in data:
        print(f"❌ Lỗi xác thực token Facebook: {data['error']}")
        sys.exit(1)
    return str(data.get("id")), data.get("name", "Unknown Page")


def upload_reel(
    video_path: Path,
    description: str,
    token: str,
    page_id: str,
    page_name: str
) -> str:
    file_size = video_path.stat().st_size
    print(f"🎬 Bắt đầu đăng Facebook Reel:")
    print(f"   - File: {video_path.name} ({file_size / 1024 / 1024:.2f} MB)")
    print(f"   - Trang: {page_name} (ID: {page_id})")

    # BƯỚC 1: Khởi tạo phiên upload (upload_phase=start)
    start_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/video_reels"
    res1 = run_curl([
        "-X", "POST",
        "-d", f"upload_phase=start&access_token={token}",
        start_url
    ])

    if "error" in res1:
        print(f"❌ Bước 1 (start) thất bại: {res1['error']}")
        sys.exit(1)

    video_id = str(res1.get("video_id"))
    upload_url = res1.get("upload_url")
    print(f"   ✅ Khởi tạo phiên upload thành công: video_id={video_id}")

    # BƯỚC 2: Tải dữ liệu video lên rupload.facebook.com
    print(f"   🚀 Đang tải file nhị phân ({file_size / 1024 / 1024:.2f} MB) lên Meta rupload...")
    cmd_upload = [
        "curl", "-s", "--max-time", "600",
        "-X", "POST",
        "-H", f"Authorization: OAuth {token}",
        "-H", "offset: 0",
        "-H", f"file_size: {file_size}",
        "-H", "Content-Type: application/octet-stream",
        "--data-binary", f"@{video_path}",
        upload_url
    ]
    res2_raw = subprocess.run(cmd_upload, capture_output=True, text=True)
    if res2_raw.returncode != 0:
        print(f"❌ Bước 2 (upload) thất bại: {res2_raw.stderr}")
        sys.exit(1)
    print(f"   ✅ Tải file lên rupload hoàn tất: {res2_raw.stdout.strip()}")

    # BƯỚC 3: Xuất bản Reel (upload_phase=finish)
    print(f"   📢 Đang xuất bản (publish) Reel...")
    finish_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/video_reels"
    res3 = run_curl([
        "-X", "POST",
        "--data-urlencode", "upload_phase=finish",
        "--data-urlencode", f"video_id={video_id}",
        "--data-urlencode", "video_state=PUBLISHED",
        "--data-urlencode", f"description={description}",
        "--data-urlencode", f"access_token={token}",
        finish_url
    ])

    if "error" in res3:
        print(f"❌ Bước 3 (finish) thất bại: {res3['error']}")
        sys.exit(1)
    print(f"   🎉 Xuất bản thành công: {res3}")

    # BƯỚC 4: Kiểm tra trạng thái xử lý video (polling)
    print("   ⏳ Kiểm tra trạng thái xử lý video từ Meta...")
    status_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{video_id}?fields=status&access_token={token}"
    for attempt in range(1, 6):
        time.sleep(3)
        try:
            status_res = run_curl([status_url])
            video_status = status_res.get("status", {}).get("video_status")
            print(f"      [Lần {attempt}] Trạng thái: {video_status}")
            if video_status in ("ready", "complete"):
                break
        except Exception:
            pass

    reel_link = f"https://www.facebook.com/reel/{video_id}"
    print(f"🔗 Link Facebook Reel: {reel_link}")
    return video_id


def main():
    parser = argparse.ArgumentParser(description="Upload video lên Facebook Reels cho Trang.")
    parser.add_argument("--file", required=True, help="Đường dẫn tới file video .mp4")
    parser.add_argument("--title", default="", help="Tiêu đề video")
    parser.add_argument("--description", default="", help="Mô tả / Caption cho Reel")
    parser.add_argument("--description-file", help="File chứa mô tả video hoặc file JSON metadata")
    parser.add_argument("--history-key", help="Khóa định danh để lưu vào facebook_uploaded_history.json")
    parser.add_argument("--token", help="Page Access Token của Facebook")
    parser.add_argument("--page-id", help="Page ID (mặc định lấy từ /me)")
    parser.add_argument("--force", action="store_true", help="Bắt buộc upload lại kể cả khi đã có trong lịch sử")

    args = parser.parse_args()

    video_path = Path(args.file).resolve()
    if not video_path.exists():
        print(f"❌ Không tìm thấy file video: {video_path}")
        sys.exit(1)

    # Đọc mô tả
    desc_text = args.description.strip()
    title_text = args.title.strip()

    if args.description_file and Path(args.description_file).exists():
        raw_content = Path(args.description_file).read_text(encoding="utf-8").strip()
        try:
            meta = json.loads(raw_content)
            if isinstance(meta, dict):
                title_text = meta.get("title", title_text)
                desc_text = meta.get("description", desc_text)
            else:
                desc_text = raw_content
        except Exception:
            desc_text = raw_content

    desc_parts = []
    if title_text:
        desc_parts.append(title_text)
    if desc_text and desc_text != title_text:
        desc_parts.append(desc_text)

    final_description = "\n\n".join(desc_parts).strip()
    if not final_description and title_text:
        final_description = title_text

    # Kiểm tra lịch sử
    history = load_history()
    if args.history_key and not args.force:
        if args.history_key in history:
            print(f"⏭️ {args.history_key} đã được upload lên Facebook Reel trước đó (Video ID: {history[args.history_key].get('video_id')}). Bỏ qua.")
            sys.exit(0)

    token = get_token(args.token)
    page_id, page_name = get_page_info(token, args.page_id)

    video_id = upload_reel(
        video_path=video_path,
        description=final_description,
        token=token,
        page_id=page_id,
        page_name=page_name
    )

    if args.history_key:
        history[args.history_key] = {
            "video_id": video_id,
            "page_id": page_id,
            "page_name": page_name,
            "file": str(video_path),
            "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        save_history(history)
        print(f"💾 Đã lưu lịch sử upload vào facebook_uploaded_history.json (key: {args.history_key})")


if __name__ == "__main__":
    main()

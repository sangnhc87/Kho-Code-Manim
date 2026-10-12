#!/usr/bin/env python3
"""
Script upload video lên Facebook Reels cho Trang (Facebook Page) tự động.
Hỗ trợ tích hợp với GitHub Actions và quy trình render Manim.

Tác giả: Thầy Nguyễn Văn Sang
Trang mặc định: ConicTypst (Page ID: 1249523211575010)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
import urllib.parse
import urllib.request
import urllib.error

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
HISTORY_FILE = REPO_ROOT / "facebook_uploaded_history.json"
GRAPH_API_VERSION = "v20.0"


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
    """Lấy Page ID và tên Trang từ token hoặc page_id."""
    target_id = page_id or os.environ.get("FB_PAGE_ID") or "me"
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{target_id}?fields=id,name&access_token={token}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return str(data.get("id")), data.get("name", "Unknown Page")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"❌ Lỗi khi xác thực token Facebook: {e.code} - {error_body}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Lỗi kết nối Graph API: {e}")
        sys.exit(1)


def upload_reel(
    video_path: Path,
    description: str,
    token: str,
    page_id: str,
    page_name: str
) -> str:
    """Quy trình 3 bước đẩy video lên Facebook Reels."""
    file_size = video_path.stat().st_size
    print(f"🎬 Bắt đầu đăng Facebook Reel:")
    print(f"   - File: {video_path.name} ({file_size / 1024 / 1024:.2f} MB)")
    print(f"   - Trang: {page_name} (ID: {page_id})")

    # BƯỚC 1: Khởi tạo phiên upload (upload_phase=start)
    start_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/video_reels"
    start_payload = urllib.parse.urlencode({
        "upload_phase": "start",
        "access_token": token
    }).encode("utf-8")

    try:
        req = urllib.request.Request(start_url, data=start_payload, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            video_id = str(res_data["video_id"])
            upload_url = res_data["upload_url"]
            print(f"   ✅ Khởi tạo phiên upload thành công: video_id={video_id}")
    except urllib.error.HTTPError as e:
        print(f"❌ Bước 1 (start) thất bại: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)

    # BƯỚC 2: Tải dữ liệu video lên rupload.facebook.com
    print(f"   🚀 Đang tải file nhị phân lên Meta rupload...")
    with open(video_path, "rb") as f:
        video_data = f.read()

    upload_req = urllib.request.Request(upload_url, data=video_data, method="POST")
    upload_req.add_header("Authorization", f"OAuth {token}")
    upload_req.add_header("offset", "0")
    upload_req.add_header("file_size", str(file_size))
    upload_req.add_header("Content-Type", "application/octet-stream")

    try:
        with urllib.request.urlopen(upload_req, timeout=300) as resp:
            raw = resp.read().decode("utf-8")
            print(f"   ✅ Tải file lên rupload hoàn tất: {raw}")
    except urllib.error.HTTPError as e:
        print(f"❌ Bước 2 (upload) thất bại: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)

    # BƯỚC 3: Xuất bản Reel (upload_phase=finish)
    print(f"   📢 Đang xuất bản (publish) Reel...")
    finish_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/video_reels"
    finish_payload = urllib.parse.urlencode({
        "upload_phase": "finish",
        "video_id": video_id,
        "video_state": "PUBLISHED",
        "description": description,
        "access_token": token
    }).encode("utf-8")

    try:
        req = urllib.request.Request(finish_url, data=finish_payload, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            finish_res = json.loads(resp.read().decode("utf-8"))
            print(f"   🎉 Xuất bản thành công: {finish_res}")
    except urllib.error.HTTPError as e:
        print(f"❌ Bước 3 (finish) thất bại: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)

    # BƯỚC 4: Kiểm tra trạng thái xử lý video (polling 3 lần)
    print("   ⏳ Kiểm tra trạng thái xử lý video từ Meta...")
    status_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{video_id}?fields=status&access_token={token}"
    for attempt in range(1, 4):
        time.sleep(3)
        try:
            req = urllib.request.Request(status_url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                status_res = json.loads(resp.read().decode("utf-8"))
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
    parser.add_argument("--description-file", help="File chứa mô tả video")
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
    desc_parts = []
    if args.title:
        desc_parts.append(args.title)
    if args.description_file and Path(args.description_file).exists():
        desc_parts.append(Path(args.description_file).read_text(encoding="utf-8").strip())
    elif args.description:
        desc_parts.append(args.description.strip())

    final_description = "\n\n".join(desc_parts).strip()
    if not final_description and args.title:
        final_description = args.title

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

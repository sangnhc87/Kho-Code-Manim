#!/usr/bin/env python3
"""
Script xuất bản video tự động lên YouTube theo Khóa Học / Chuyên Đề:
1. Series Trải Phẳng Hình Học Không Gian (20 bài)
2. Series Đại Số Tổ Hợp & Xác Suất (25 bài)

Tác giả: Thầy Nguyễn Văn Sang
Hỗ trợ: Tự động gắn metadata chuẩn SEO, tự động thêm vào Playlist,
quản lý lịch sử tránh trùng lặp và xử lý giới hạn Quota an toàn.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Import metadata khóa học
try:
    from scripts.courses_metadata import (
        PLAYLIST_TRAI_PHANG,
        TRAI_PHANG_LESSONS,
        PLAYLIST_TO_HOP,
        TO_HOP_LESSONS,
        AUTHOR_INFO,
    )
except ImportError:
    from courses_metadata import (
        PLAYLIST_TRAI_PHANG,
        TRAI_PHANG_LESSONS,
        PLAYLIST_TO_HOP,
        TO_HOP_LESSONS,
        AUTHOR_INFO,
    )

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtubepartner",
]

HISTORY_FILE = Path("youtube_uploaded_history.json")


def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def get_youtube_client():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        # Fallback thử đọc từ ~/.youtube_secrets.json nếu có
        secrets_file = Path.home() / ".youtube_secrets.json"
        if secrets_file.exists():
            data = json.loads(secrets_file.read_text(encoding="utf-8"))
            client_id = data.get("client_id")
            client_secret = data.get("client_secret")
            refresh_token = data.get("refresh_token")

    if not client_id or not client_secret or not refresh_token:
        print("❌ Thiếu thông tin xác thực YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET hoặc YOUTUBE_REFRESH_TOKEN.")
        sys.exit(1)

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )

    return build("youtube", "v3", credentials=credentials)


def get_or_create_playlist(youtube, title, description):
    """Tìm hoặc tạo playlist theo tên bài giảng"""
    try:
        # Tìm danh sách playlist hiện có
        request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
        response = request.execute()
        for item in response.get("items", []):
            if item["snippet"]["title"] == title:
                return item["id"]

        # Nếu chưa có thì tạo mới
        create_req = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {"title": title, "description": description},
                "status": {"privacyStatus": "public"},
            },
        )
        res = create_req.execute()
        print(f"📁 Đã tạo mới Playlist: {title} (ID: {res['id']})")
        return res["id"]
    except Exception as e:
        print(f"⚠️ Không thể tạo/lấy Playlist (có thể do scope hoặc quota): {e}")
        return None


def add_video_to_playlist(youtube, playlist_id, video_id):
    if not playlist_id:
        return
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        ).execute()
        print(f"📋 Đã thêm video vào Playlist thành công!")
    except Exception as e:
        print(f"⚠️ Chưa thêm được vào Playlist: {e}")


def upload_single_file(youtube, video_path, title, description, tags, privacy="public", category_id="27"):
    if not os.path.exists(video_path):
        print(f"❌ File video không tồn tại: {video_path}")
        return None, None

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"\n==================================================")
    print(f"🚀 BẮT ĐẦU ĐĂNG TẢI:")
    print(f"   🎬 Tiêu đề: {title}")
    print(f"   📁 File:    {video_path} ({file_size_mb:.2f} MB)")
    print(f"   🌐 Chế độ:  {privacy.upper()}")
    print(f"==================================================")

    tag_list = [t.strip() for t in tags] if isinstance(tags, list) else [t.strip() for t in tags.split(",") if t.strip()]

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tag_list,
            "categoryId": category_id,
            "defaultLanguage": "vi",
            "defaultAudioLanguage": "vi",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        chunksize=4 * 1024 * 1024,
        resumable=True,
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    retry_count = 0
    max_retries = 5

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                percent = int(status.progress() * 100)
                print(f"   ⏳ Đang tải lên: {percent}%...", end="\r")
        except HttpError as e:
            if "quotaExceeded" in str(e):
                print("\n\n⚠️ ĐÃ ĐẠT GIỚI HẠN QUOTA YOUTUBE HÔM NAY (10.000 điểm).")
                print("Lịch sử đã được lưu lại an toàn. Ngày mai hệ thống Google reset quota, thầy chỉ cần chạy lại lệnh là sẽ tự động đăng tiếp các bài còn lại!")
                return None, None
            if e.resp.status in [500, 502, 503, 504]:
                retry_count += 1
                if retry_count > max_retries:
                    raise
                wait_time = 2 ** retry_count
                print(f"\n⚠️ Lỗi mạng máy chủ ({e.resp.status}). Đang thử lại sau {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"

    print(f"\n🎉 XUẤT BẢN THÀNH CÔNG!")
    print(f"🔗 Xem video tại: {video_url}")
    print(f"🆔 Video ID:     {video_id}")

    # Ghi nhận biến môi trường cho GitHub Actions nếu có
    github_env = os.environ.get("GITHUB_ENV")
    if github_env and os.path.exists(github_env):
        with open(github_env, "a", encoding="utf-8") as f:
            f.write(f"YOUTUBE_VIDEO_ID={video_id}\n")
            f.write(f"YOUTUBE_VIDEO_URL={video_url}\n")

    return video_id, video_url


def locate_trai_phang_video(lesson_num):
    base_dir = Path("Manim-Typst/SeriesTraiPhang")
    num_str = f"{lesson_num:02d}"
    matches = list(base_dir.glob(f"trai_phang_{num_str}_*1080p*.mp4"))
    if not matches:
        matches = list(base_dir.glob(f"trai_phang_{num_str}_*.mp4"))
    return matches[0] if matches else None


def locate_to_hop_video(lesson_num):
    base_dir = Path("Series-Dai-So-To-Hop")
    num_str = f"{lesson_num:02d}"
    # Ưu tiên COMBxx_V2...
    matches = list(base_dir.glob(f"COMB{num_str}_*.mp4"))
    if not matches:
        matches = list(base_dir.glob(f"COMB{num_str}.mp4"))
    return matches[0] if matches else None


def handle_series_upload(youtube, series_name, privacy="public", limit=None):
    history = load_history()
    count = 0

    if series_name == "trai_phang":
        print(f"\n🎯 BẮT ĐẦU XỬ LÝ KHÓA HỌC: TRẢI PHẲNG HÌNH HỌC KHÔNG GIAN (20 BÀI)")
        playlist_info = PLAYLIST_TRAI_PHANG
        lessons = TRAI_PHANG_LESSONS
        finder = locate_trai_phang_video
    elif series_name == "to_hop":
        print(f"\n🎯 BẮT ĐẦU XỬ LÝ KHÓA HỌC: ĐẠI SỐ TỔ HỢP & XÁC SUẤT (25 BÀI)")
        playlist_info = PLAYLIST_TO_HOP
        lessons = TO_HOP_LESSONS
        finder = locate_to_hop_video
    else:
        print(f"❌ Khóa học không hợp lệ: {series_name}")
        return

    playlist_id = get_or_create_playlist(youtube, playlist_info["title"], playlist_info["description"])

    for lesson_num in sorted(lessons.keys()):
        key = f"{series_name}_{lesson_num:02d}"
        if key in history:
            print(f"⏩ Bỏ qua {key}: Đã đăng tải trước đó ({history[key]['url']})")
            continue

        meta = lessons[lesson_num]
        video_path = finder(lesson_num)

        if not video_path:
            print(f"⚠️ Chưa tìm thấy file MP4 cho bài {lesson_num} ({key}). Bỏ qua.")
            continue

        desc = meta.get("description")
        if not desc:
            desc = f"""Khóa học: {playlist_info['title']}
Bài học: {meta['title']}

{AUTHOR_INFO}
#Toan10 #Toan11 #Toan12 #ThayNguyenVanSang #Manim"""

        vid_id, vid_url = upload_single_file(
            youtube=youtube,
            video_path=video_path,
            title=meta["title"],
            description=desc,
            tags=meta["tags"],
            privacy=privacy,
        )

        if vid_id:
            add_video_to_playlist(youtube, playlist_id, vid_id)
            history[key] = {
                "id": vid_id,
                "url": vid_url,
                "title": meta["title"],
                "file": str(video_path),
                "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            save_history(history)
            count += 1

            if limit and count >= limit:
                print(f"⏹️ Đã đạt giới hạn số video tải trong phiên này ({limit} video). Tạm dừng.")
                break
        else:
            # Gặp lỗi (ví dụ hết quota) -> dừng lại an toàn
            break

    print(f"\n📊 TỔNG KẾT: Đã đăng tải thành công {count} video mới!")


def main():
    parser = argparse.ArgumentParser(description="YouTube Uploader cho Khóa Học Manim & Typst")
    parser.add_argument("--file", help="Đường dẫn trực tiếp file MP4")
    parser.add_argument("--title", help="Tiêu đề video")
    parser.add_argument("--description", default="", help="Mô tả video")
    parser.add_argument("--tags", default="", help="Tags video (ngăn cách bằng dấu phẩy)")
    parser.add_argument("--privacy", choices=["public", "unlisted", "private"], default="public", help="Chế độ hiển thị (mặc định: public)")
    parser.add_argument("--series", choices=["trai_phang", "to_hop"], help="Chạy theo chuỗi khóa học (trai_phang hoặc to_hop)")
    parser.add_argument("--lesson", type=int, help="Chỉ định số bài cần tải (ví dụ: --lesson 1)")
    parser.add_argument("--limit", type=int, default=6, help="Số lượng video tối đa tải trong 1 lần chạy (mặc định: 6 video)")

    args = parser.parse_args()
    youtube = get_youtube_client()

    if args.series:
        if args.lesson:
            # Tải đúng 1 bài cụ thể trong series
            lessons = TRAI_PHANG_LESSONS if args.series == "trai_phang" else TO_HOP_LESSONS
            meta = lessons.get(args.lesson)
            finder = locate_trai_phang_video if args.series == "trai_phang" else locate_to_hop_video
            video_path = finder(args.lesson)
            if not meta or not video_path:
                print(f"❌ Không tìm thấy thông tin hoặc file video cho bài {args.lesson}")
                sys.exit(1)
            desc = meta.get("description", f"{meta['title']}\n{AUTHOR_INFO}")
            upload_single_file(
                youtube=youtube,
                video_path=video_path,
                title=meta["title"],
                description=desc,
                tags=meta["tags"],
                privacy=args.privacy,
            )
        else:
            handle_series_upload(youtube, args.series, privacy=args.privacy, limit=args.limit)
    elif args.file:
        title = args.title or Path(args.file).stem.replace("_", " ")
        upload_single_file(
            youtube=youtube,
            video_path=args.file,
            title=title,
            description=args.description,
            tags=args.tags,
            privacy=args.privacy,
        )
    else:
        print("Vui lòng cung cấp --series [trai_phang|to_hop] hoặc --file [duong_dan_mp4]")


if __name__ == "__main__":
    main()

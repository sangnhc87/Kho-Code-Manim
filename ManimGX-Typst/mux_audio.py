import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def build_master_audio(events, video_duration, out_wav: Path):
    if not events:
        raise RuntimeError("Không có đoạn audio nào.")

    inputs, filters, labels = [], [], []
    for i, (start, path) in enumerate(events):
        inputs += ["-i", str(path)]
        ms = max(0, int(round(start * 1000)))
        filters.append(f"[{i}:a]adelay={ms}|{ms},aresample=48000[a{i}]")
        labels.append(f"[a{i}]")

    fc = (
        ";".join(filters)
        + ";"
        + "".join(labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        *inputs,
        "-filter_complex",
        fc,
        "-map",
        "[m]",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-t",
        f"{video_duration:.3f}",
        str(out_wav),
    ]
    subprocess.run(cmd, check=True)


def mux_audio(video_path: Path, audio_path: Path, out_path: Path):
    cmd = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(out_path),
    ]
    subprocess.run(cmd, check=True)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def main():
    video_raw = ROOT / "raw_video.mp4"
    if not video_raw.exists():
        video_raw = Path("raw_video.mp4")
    if not video_raw.exists():
        print(f"Lỗi: Không tìm thấy video raw tại {video_raw}")
        sys.exit(1)

    timeline_file = ROOT / "scene_timeline.json"
    if not timeline_file.exists():
        print(f"Lỗi: Không tìm thấy {timeline_file}")
        sys.exit(1)

    timeline = json.loads(timeline_file.read_text(encoding="utf-8"))
    events = []
    for item in timeline:
        start = item["start"]
        audio_path = Path(item["audio_path"])
        if audio_path.exists():
            events.append((start, audio_path))
        else:
            print(f"Cảnh báo: Audio không tồn tại {audio_path}")

    video_duration = probe_duration(video_raw)
    print(f"Thời lượng video gốc: {video_duration:.2f}s")

    master_audio = ROOT / "master_audio.wav"
    print("-> Đang ghép các đoạn thuyết minh thành Master Audio Track...")
    build_master_audio(events, video_duration, master_audio)

    output_final = ROOT / "bai_toan_san_xuat_mu_1080p_WITH_AUDIO.mp4"
    print(f"-> Muxing video và audio vào {output_final} ...")
    mux_audio(video_raw, master_audio, output_final)

    final_dur = probe_duration(output_final)
    final_size = output_final.stat().st_size
    print(f"=== XUẤT VIDEO THÀNH CÔNG ===")
    print(f"File: {output_final}")
    print(f"Thời lượng: {final_dur:.2f}s | Kích thước: {final_size / (1024*1024):.2f} MB")


if __name__ == "__main__":
    main()

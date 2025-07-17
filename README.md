# youtube_downloader

# 🎬 Modern Video Downloader (GUI powered by yt-dlp + customtkinter)

A modern, user-friendly desktop application built using Python and `customtkinter`, designed to download videos and audio from YouTube and hundreds of other sites using `yt-dlp`. It supports high-quality downloads, subtitle embedding, and site-specific format selection.

---

## 🚀 Features

- ✅ Download videos or extract audio (MP3)
- ✅ Supports 1080p/4K/8K video where available
- ✅ Embed subtitles, metadata, and thumbnails
- ✅ Modern and clean GUI with light/dark theme toggle
- ✅ Format selection for video and audio
- ✅ Multi-site support powered by [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)

---

## 🖥️ Preview

> GUI interface with dark/light mode, format selection, and progress tracking.

---

## 🛠️ Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/download.html)
- Required Python libraries:
  ```bash
  pip install yt-dlp customtkinter pillow requests

## 🌐 Supported Sites
This downloader supports hundreds of video/audio platforms, including:

YouTube

Instagram

SonyLIV (Free content up to 1080p)

Zee5 (Free content up to 720p or 1080p)

Twitter/X, Facebook, Vimeo, and many more...

👉 Check all supported sites using:

```bash
yt-dlp --list-extractors


## ⚠️ Known Limitations
Some videos may fail to download due to:

DRM restrictions

Server-side protection

yt-dlp limitations or bugs

🔄 If a download fails:

Try downloading the same resolution 4–5 times, or switch to a different format.

📦 Also, update yt-dlp regularly:

```bash
yt-dlp -U


## 💡 Tips
You can choose between video or audio (MP3) download types.

Select the format manually from available resolutions/bitrates.

Use the embedded theme switch to toggle light/dark mode.

Downloads are saved to your default Downloads folder (or the selected output path).


## 🧩 Contributions
Have an idea? Want to fix bugs or add new features?

Fork this repo

Create a feature branch

Submit a pull request

✅ We welcome all contributions!

## 📩 Issues & Feedback
If you encounter a bug or need help:

Open an issue on GitHub

Or suggest improvements/enhancements

## 📜 License
This project is open-source and free to use under the MIT License.

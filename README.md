# 🎬 YouTube Downloader

## Modern Video Downloader (GUI powered by yt-dlp + customtkinter)

A modern, user-friendly desktop application built using Python and `customtkinter`, designed to download videos and audio from YouTube and hundreds of other sites using `yt-dlp`. It supports high-quality downloads, subtitle embedding, and site-specific format selection.

---

## 🚀 Features

- ✅ Download videos or extract audio (MP3)
- ✅ Supports 1080p / 4K / 8K video (where available)
- ✅ Embed subtitles, metadata, and thumbnails
- ✅ Modern and clean GUI with light/dark theme toggle
- ✅ Format selection for video and audio
- ✅ Multi-site support powered by [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)

---

## 🖥️ Preview

> GUI interface with light/dark mode, format selection, and download progress display.

---

## 🛠️ Requirements

- Python 3.8 or newer
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/download.html) (required for audio extraction, merging, etc.)

### 📦 Install dependencies

```bash
pip install yt-dlp customtkinter pillow requests
````

---

## 🔧 Setup FFmpeg on Windows

1. Download FFmpeg from: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
2. Extract the ZIP file.
3. Copy the full path of the `bin` folder (e.g., `C:\ffmpeg\bin`)
4. Add it to your system’s **Environment Variables** → **Path**
5. Confirm setup:

```bash
ffmpeg -version
```

If you see version info, FFmpeg is correctly configured.

---

## 🚀 How to Run

Clone this repository and run the script:

```bash
git clone https://github.com/your-username/modern-video-downloader.git
cd modern-video-downloader
python yt_downloader.py
```

> Downloads will be saved to your **Downloads** folder by default (or the output directory you choose).

---

## 🌐 Supported Sites

This downloader supports **hundreds of websites**, including:

* **YouTube**
* **Instagram**
* **SonyLIV** *(Free content up to 1080p)*
* **Zee5** *(Free content up to 720p or 1080p)*
* **Twitter/X**
* **Facebook**
* **Vimeo**, and many more...

👉 To list all supported sites:

```bash
yt-dlp --list-extractors
```

---

## ⚠️ Known Limitations

Some videos **may not download** due to:

* ❌ DRM or encryption
* 🔐 Server-side protections
* ⚠️ `yt-dlp` errors or limitations

💡 **If a download fails**, try:

* Retrying the **same resolution 4–5 times**
* Choosing a different format (lower resolution)
* Updating `yt-dlp`:

```bash
yt-dlp -U
```

---

## 💡 Tips & Tricks

* Choose between **video (MP4)** or **audio (MP3)** downloads
* Manually select desired resolution or bitrate
* Use the **theme toggle** to switch between light and dark modes
* Preview video info and thumbnail before downloading

---

## 🧩 Contributions

Want to help improve the project?

1. Fork this repository
2. Create a new feature/bugfix branch
3. Submit a pull request

✅ All contributions are welcome!

---

## 📩 Issues & Feedback

* Found a bug? Suggesting a new feature?
* Open an [issue](https://github.com/your-username/modern-video-downloader/issues)

---

## 📜 License

This project is licensed under the **MIT License**. You’re free to use, modify, and distribute it.

---

## 🙌 Special Thanks

* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [FFmpeg](https://ffmpeg.org/)
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [Pillow](https://pillow.readthedocs.io/)

---

```

---

Let me know if you'd like:
- A matching `requirements.txt`
- `.gitignore` for PyInstaller builds
- Or help turning this into a `.exe` for easy use on Windows!
```

import customtkinter as ctk
from PIL import Image, ImageTk
import requests
import subprocess
import threading
import json
import os
import sys
from pathlib import Path
import re
from io import BytesIO
import tkinter as tk
from tkinter import messagebox, filedialog
import time

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "system" (default), "dark", "light"

class ModernYouTubeDownloader:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Modern Video Downloader")
        self.root.geometry("1200x900")
        self.root.minsize(1100, 800)
        
        # Variables
        self.url_var = tk.StringVar()
        self.download_type = tk.StringVar(value="video")  # "video" or "audio"
        self.selected_format = tk.StringVar()
        self.output_dir = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.video_info = {}
        self.formats_data = {}
        self.formats = []  # Added missing formats list
        self.current_process = None
        self.format_vars = {}  # Store radio button variables
        
        self.setup_ui()
        self.check_ytdlp()
    
    def setup_ui(self):
        """Setup the main UI components"""
        # Create main container with padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable container for main content
        self.scrollable_container = ctk.CTkScrollableFrame(main_frame, corner_radius=10)
        self.scrollable_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Title section
        self.setup_top_bar(self.scrollable_container)

        # URL Input Section
        self.setup_url_section(self.scrollable_container)

        # Main content area with proper layout
        content_frame = ctk.CTkFrame(self.scrollable_container, corner_radius=10)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel (30% width)
        self.left_panel = ctk.CTkFrame(content_frame, corner_radius=10)
        self.left_panel.pack(side="left", fill="both", expand=False, padx=(10, 5), pady=10)
        self.left_panel.configure(width=350)

        # Right panel (70% width)
        self.right_panel = ctk.CTkFrame(content_frame, corner_radius=10)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # Setup sections
        self.setup_video_preview_section(self.left_panel)
        self.setup_download_directory_section(self.left_panel)
        self.setup_output_section(self.left_panel)
        
        self.setup_download_type_section(self.right_panel)
        self.setup_format_section(self.right_panel)
        self.setup_download_controls(self.right_panel)
        self.setup_progress_section(self.right_panel)

    def setup_top_bar(self, parent):
        """Top bar with title and theme toggle"""
        top_bar = ctk.CTkFrame(parent, height=60, corner_radius=10)
        top_bar.pack(fill="x", padx=10, pady=(10, 20))

        title_label = ctk.CTkLabel(
            top_bar,
            text="🎬 Modern YouTube Downloader",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left", padx=20, pady=15)

        # Theme toggle
        self.theme_mode = tk.StringVar(value="Dark")
        theme_toggle = ctk.CTkSwitch(
            top_bar,
            text="Light Mode",
            command=self.toggle_theme,
            variable=self.theme_mode,
            onvalue="Light",
            offvalue="Dark"
        )
        theme_toggle.pack(side="right", padx=20, pady=15)

    def toggle_theme(self):
        """Switch between dark/light mode"""
        mode = self.theme_mode.get().lower()
        ctk.set_appearance_mode(mode)

    def setup_url_section(self, parent):
        """Setup URL input section"""
        url_frame = ctk.CTkFrame(parent, corner_radius=10)
        url_frame.pack(fill="x", padx=10, pady=(0, 20))

        # Section title
        url_label = ctk.CTkLabel(
            url_frame, 
            text="🔗 Video URL", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        url_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Input container
        input_container = ctk.CTkFrame(url_frame, fg_color="transparent")
        input_container.pack(fill="x", padx=20, pady=(0, 20))

        # URL Entry
        self.url_entry = ctk.CTkEntry(
            input_container, 
            textvariable=self.url_var, 
            height=45,
            font=ctk.CTkFont(size=14),
            placeholder_text="Enter YouTube URL here...",
            corner_radius=8
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))

        # Fetch Button
        self.fetch_btn = ctk.CTkButton(
            input_container,
            text="📥 Fetch Info",
            command=self.fetch_video_info,
            height=45,
            width=150,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        self.fetch_btn.pack(side="right")

    def setup_video_preview_section(self, parent):
        """Setup video preview section"""
        self.preview_frame = ctk.CTkFrame(parent, corner_radius=10)
        self.preview_frame.pack(fill="x", padx=10, pady=(0, 15))
        self.preview_frame.pack_forget()  # Hide initially
        
        # Section title
        preview_label = ctk.CTkLabel(
            self.preview_frame, 
            text="📹 Video Preview", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Thumbnail container
        thumbnail_container = ctk.CTkFrame(self.preview_frame, corner_radius=8)
        thumbnail_container.pack(fill="x", padx=15, pady=(0, 10))
        
        self.thumbnail_label = ctk.CTkLabel(
            thumbnail_container, 
            text="Loading thumbnail...", 
            width=320, 
            height=180,
            corner_radius=8
        )
        self.thumbnail_label.pack(padx=10, pady=10)
        
        # Video info container
        info_container = ctk.CTkFrame(self.preview_frame, corner_radius=8)
        info_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self.title_label = ctk.CTkLabel(
            info_container,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=300,
            justify="left",
            anchor="w"
        )
        self.title_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.duration_label = ctk.CTkLabel(
            info_container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray70",
            anchor="w"
        )
        self.duration_label.pack(anchor="w", padx=15, pady=(0, 5))
        
        self.uploader_label = ctk.CTkLabel(
            info_container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray70",
            anchor="w"
        )
        self.uploader_label.pack(anchor="w", padx=15, pady=(0, 15))

    def setup_download_directory_section(self, parent):
        """Setup download directory section"""
        dir_frame = ctk.CTkFrame(parent, corner_radius=10)
        dir_frame.pack(fill="x", padx=10, pady=(10, 15))

        # Section title
        dir_label = ctk.CTkLabel(
            dir_frame, 
            text="📁 Output Directory", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        dir_label.pack(anchor="w", padx=15, pady=(15, 10))

        # Directory selection container
        dir_container = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_container.pack(fill="x", padx=15, pady=(0, 15))

        self.dir_entry = ctk.CTkEntry(
            dir_container,
            textvariable=self.output_dir,
            height=40,
            font=ctk.CTkFont(size=12),
            corner_radius=8
        )
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            dir_container,
            text="📂 Browse",
            command=self.browse_directory,
            height=40,
            width=100,
            corner_radius=8
        )
        browse_btn.pack(side="right")

    def setup_output_section(self, parent):
        """Setup output log section"""
        self.output_frame = ctk.CTkFrame(parent, corner_radius=10)
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Section title
        output_label = ctk.CTkLabel(
            self.output_frame,
            text="📝 Output Log",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        output_label.pack(anchor="w", padx=15, pady=(15, 10))

        # Output text area
        self.output_text = ctk.CTkTextbox(
            self.output_frame, 
            height=200, 
            font=ctk.CTkFont(size=11),
            corner_radius=8
        )
        self.output_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def setup_download_type_section(self, parent):
        """Setup download type selection"""
        self.type_frame = ctk.CTkFrame(parent, corner_radius=10)
        self.type_frame.pack(fill="x", padx=10, pady=(10, 15))
        self.type_frame.pack_forget()  # Hide initially
        
        # Section title
        type_label = ctk.CTkLabel(
            self.type_frame, 
            text="📦 Download Type", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        type_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Type selection container
        type_container = ctk.CTkFrame(self.type_frame, fg_color="transparent")
        type_container.pack(fill="x", padx=15, pady=(0, 15))
        
        # Radio buttons for download type
        self.video_radio = ctk.CTkRadioButton(
            type_container,
            text="🎥 Video (MP4)",
            variable=self.download_type,
            value="video",
            command=self.on_download_type_change,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.video_radio.pack(side="left", padx=(10, 30))
        
        self.audio_radio = ctk.CTkRadioButton(
            type_container,
            text="🎵 Audio (MP3)",
            variable=self.download_type,
            value="audio",
            command=self.on_download_type_change,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.audio_radio.pack(side="left", padx=(0, 10))

    def setup_format_section(self, parent):
        """Setup format selection section"""
        self.format_frame = ctk.CTkFrame(parent, corner_radius=10)
        self.format_frame.pack(fill="both", expand=True, padx=10, pady=(0, 15))
        self.format_frame.pack_forget()  # Hide initially
        
        # Section title
        format_label = ctk.CTkLabel(
            self.format_frame, 
            text="⚙️ Available Formats", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        format_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Scrollable frame for formats
        self.format_scroll = ctk.CTkScrollableFrame(
            self.format_frame, 
            height=350,
            corner_radius=8
        )
        self.format_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def setup_download_controls(self, parent):
        """Setup download controls section"""
        self.controls_frame = ctk.CTkFrame(parent, corner_radius=10)
        self.controls_frame.pack(fill="x", padx=10, pady=(0, 15))
        self.controls_frame.pack_forget()  # Hide initially

        # Download button
        self.download_btn = ctk.CTkButton(
            self.controls_frame,
            text="⬇️ Start Download",
            command=self.start_download,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10
        )
        self.download_btn.pack(fill="x", padx=15, pady=15)

    def setup_progress_section(self, parent):
        """Setup progress section"""
        self.progress_frame = ctk.CTkFrame(parent, corner_radius=10)
        self.progress_frame.pack(fill="x", padx=15, pady=(15, 10))
        self.progress_frame.pack_forget()  # Hide initially
        
        # Section title
        progress_label = ctk.CTkLabel(
            self.progress_frame, 
            text="📊 Download Progress", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        progress_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame, 
            height=25,
            corner_radius=10
        )
        self.progress_bar.pack(fill="x", padx=15, pady=(15, 10))
        self.progress_bar.set(0)
        
        # Progress text
        self.progress_text = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to download...",
            font=ctk.CTkFont(size=12)
        )
        self.progress_text.pack(padx=15, pady=(15, 10))
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self.progress_frame,
            text="❌ Cancel Download",
            command=self.cancel_download,
            height=40,
            fg_color="red",
            hover_color="darkred",
            corner_radius=8
        )
        self.cancel_btn.pack(fill="x", padx=15, pady=(15, 10))

    def check_ytdlp(self):
        """Check if yt-dlp is available"""
        try:
            result = subprocess.run(
                ['yt-dlp', '--version'], 
                capture_output=True, 
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            version = result.stdout.decode().strip()
            self.log_output(f"✅ yt-dlp is available (version: {version})")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log_output("❌ ERROR: yt-dlp not found. Please install it using: pip install yt-dlp")
            messagebox.showerror("Error", "yt-dlp not found.\n\nPlease install it using:\npip install yt-dlp")

    def log_output(self, message):
        """Add message to output log"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.output_text.insert("end", formatted_message)
        self.output_text.see("end")

    def fetch_video_info(self):
        """Fetch video information and display preview"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        self.fetch_btn.configure(state="disabled", text="🔄 Fetching...")
        self.log_output(f"🔍 Fetching video info for: {url}")
        
        def fetch_info():
            try:
                cmd = ['yt-dlp', '-j', '--no-warnings', url]
                result = subprocess.run(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                
                if result.returncode == 0:
                    self.video_info = json.loads(result.stdout)
                    self.root.after(0, self.on_video_info_success)
                else:
                    self.video_info = None
                    self.root.after(0, lambda: self.on_video_info_error(result.stderr))
            except Exception as e:
                self.video_info = None
                self.root.after(0, lambda: self.on_video_info_error(str(e)))
        
        threading.Thread(target=fetch_info, daemon=True).start()

    def on_video_info_success(self):
        """Handle successful video info fetch"""
        self.fetch_btn.configure(state="normal", text="📥 Fetch Info")
        self.display_video_info()
        self.load_thumbnail()
        self.fetch_formats()
        
        # Show preview and other sections
        self.preview_frame.pack(fill="x", padx=10, pady=(0, 15))
        self.type_frame.pack(fill="x", padx=10, pady=(10, 15))
        self.format_frame.pack(fill="both", expand=True, padx=10, pady=(0, 15))
        self.controls_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        self.log_output("✅ Video info fetched successfully")

    def on_video_info_error(self, error_msg):
        """Handle video info fetch error"""
        self.fetch_btn.configure(state="normal", text="📥 Fetch Info")
        self.log_output(f"❌ Error fetching video info: {error_msg}")
        messagebox.showerror("Error", f"Failed to fetch video info:\n{error_msg}")

    def display_video_info(self):
        """Display video information"""
        if not self.video_info:
            self.title_label.configure(text="Video Info: Not available")
            self.duration_label.configure(text="")
            self.uploader_label.configure(text="")
            return

        title = self.video_info.get('title', 'Unknown Title')
        duration = self.video_info.get('duration')
        uploader = self.video_info.get('uploader', 'Unknown')

        self.title_label.configure(text=title)
        
        if duration:
            duration_str = self.format_duration(duration)
            self.duration_label.configure(text=f"⏱ Duration: {duration_str}")
        else:
            self.duration_label.configure(text="")
        
        if uploader:
            self.uploader_label.configure(text=f"📺 Channel: {uploader}")
        else:
            self.uploader_label.configure(text="")

    def load_thumbnail(self):
        """Load and display video thumbnail"""
        if not self.video_info:
            return
            
        try:
            thumbnail_url = self.video_info.get('thumbnail')
            if thumbnail_url:
                def load_thumb():
                    try:
                        response = requests.get(thumbnail_url, timeout=10)
                        if response.status_code == 200:
                            # Load and resize image
                            image = Image.open(BytesIO(response.content))
                            # Maintain aspect ratio
                            image.thumbnail((320, 180), Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(image)
                            
                            # Update thumbnail label
                            self.root.after(0, lambda: self.thumbnail_label.configure(image=photo, text=""))
                            self.root.after(0, lambda: setattr(self.thumbnail_label, 'image', photo))
                        else:
                            self.root.after(0, lambda: self.thumbnail_label.configure(text="❌ Thumbnail unavailable"))
                    except Exception as e:
                        self.root.after(0, lambda: self.log_output(f"⚠️ Could not load thumbnail: {str(e)}"))
                        self.root.after(0, lambda: self.thumbnail_label.configure(text="❌ Thumbnail failed to load"))
                
                threading.Thread(target=load_thumb, daemon=True).start()
        except Exception as e:
            self.log_output(f"⚠️ Thumbnail error: {str(e)}")

    def format_duration(self, seconds):
        """Format duration from seconds to readable format"""
        if not seconds:
            return "Unknown"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def fetch_formats(self):
        """Fetch available formats"""
        url = self.url_var.get().strip()
        if not url:
            return
        
        self.log_output("🔍 Fetching available formats...")
        
        def fetch_formats_thread():
            try:
                cmd = ['yt-dlp', '-F', '--no-warnings', url]
                result = subprocess.run(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                
                if result.returncode == 0:
                    self.formats = result.stdout.splitlines()
                    self.root.after(0, self.parse_formats)  # Call parse_formats without arguments
                    self.root.after(0, self.display_formats)
                else:
                    self.formats = []
                    self.root.after(0, lambda: self.log_output(f"❌ Error fetching formats: {result.stderr}"))
            except Exception as e:
                self.formats = []
                self.root.after(0, lambda: self.log_output(f"❌ Error fetching formats: {str(e)}"))
        
        threading.Thread(target=fetch_formats_thread, daemon=True).start()

    def parse_formats(self):
        """Parse the format output from yt-dlp -F command"""
        self.formats_data = {"video": [], "audio": []}
        
        if not self.formats:
            return
        
        for line in self.formats:
            # Skip header lines and empty lines
            if not line.strip() or line.startswith("format") or re.match(r"^\s*ID\s+EXT", line) or line.startswith("["):
                continue
            
            # Parse the line - yt-dlp format: ID EXT RESOLUTION FPS FILESIZE TBR PROTO VCODEC ACODEC MORE_INFO
            parts = line.split()
            if len(parts) < 3:
                continue
            
            format_id = parts[0]
            ext = parts[1]
            
            # Extract various format details
            resolution = self.extract_resolution_from_line(line)
            filesize = self.extract_filesize_from_line(line)
            fps = self.extract_fps_from_line(line)
            vcodec = self.extract_vcodec_from_line(line)
            acodec = self.extract_acodec_from_line(line)
            abr = self.extract_abr_from_line(line)
            
            format_info = {
                "id": format_id,
                "ext": ext,
                "resolution": resolution,
                "filesize": filesize,
                "fps": fps,
                "vcodec": vcodec,
                "acodec": acodec,
                "abr": abr,
                "codec": vcodec if vcodec != "none" else acodec,
                "full": line,
            }
            
            # Improved audio/video classification
            is_audio_only = (
                vcodec == "none" or 
                "audio only" in line.lower() or 
                resolution == "audio only" or
                ext in ['m4a', 'mp3', 'aac', 'ogg', 'opus', 'wav'] or
                (resolution == "N/A" and acodec != "none" and acodec != "unknown")
            )
            
            is_video_only = (
                acodec == "none" or 
                "video only" in line.lower() or
                (resolution != "audio only" and resolution != "N/A" and acodec == "none")
            )
            
            # Classify formats
            if is_audio_only:
                self.formats_data["audio"].append(format_info)
            elif is_video_only or (resolution != "audio only" and resolution != "N/A"):
                self.formats_data["video"].append(format_info)
            else:
                # If unclear, check if it has both video and audio
                if acodec != "none" and vcodec != "none":
                    self.formats_data["video"].append(format_info)
                elif acodec != "none":
                    self.formats_data["audio"].append(format_info)
        
        # Sort formats
        self.formats_data["video"].sort(key=lambda x: self.get_resolution_sort_key(x["resolution"]), reverse=True)
        self.formats_data["audio"].sort(key=lambda x: self.extract_bitrate_value(x["abr"]), reverse=True)


    def extract_bitrate_value(self, bitrate_str):
        """Extract numeric bitrate value for sorting"""
        if not bitrate_str or bitrate_str == "N/A":
            return 0
        
        # Extract numeric value from strings like "128k", "192k", etc.
        match = re.search(r'(\d+)', bitrate_str)
        if match:
            return int(match.group(1))
        
        return 0

    def extract_resolution_from_line(self, line):
        """Extract resolution from format line"""
        # Look for patterns like 1920x1080, 720p, etc.
        resolution_match = re.search(r'\b(\d{3,4}x\d{3,4})\b', line)
        if resolution_match:
            return resolution_match.group(1)
        
        # Look for patterns like 720p, 1080p
        p_match = re.search(r'\b(\d{3,4}p)\b', line)
        if p_match:
            return p_match.group(1)
        
        # Check if it's audio only
        if "audio only" in line.lower() or re.search(r'\bvcodec\s*:\s*none\b', line):
            return "audio only"
        
        return "N/A"

    def extract_filesize_from_line(self, line):
        """Extract filesize from format line"""
        # Look for patterns like 123.45MiB, 1.23GiB, etc.
        size_match = re.search(r'\b(\d+(?:\.\d+)?(?:KiB|MiB|GiB|TiB|KB|MB|GB|TB))\b', line)
        if size_match:
            return size_match.group(1)
        
        # Look for patterns like ~123MB
        approx_match = re.search(r'~(\d+(?:\.\d+)?(?:KB|MB|GB|TB))', line)
        if approx_match:
            return f"~{approx_match.group(1)}"
        
        return "N/A"

    def extract_fps_from_line(self, line):
        """Extract FPS from format line"""
        fps_match = re.search(r'\b(\d+(?:\.\d+)?)fps\b', line)
        if fps_match:
            return f"{fps_match.group(1)}fps"
        return "N/A"

    def extract_vcodec_from_line(self, line):
        """Extract video codec from format line"""
        # Common video codecs
        codecs = ['h264', 'h265', 'vp9', 'vp8', 'av01', 'avc1', 'hevc', 'none']
        for codec in codecs:
            if codec in line.lower():
                return codec
        return "unknown"

    def extract_acodec_from_line(self, line):
        """Extract audio codec from format line"""
        # Common audio codecs
        codecs = ['aac', 'mp3', 'opus', 'vorbis', 'mp4a', 'none']
        for codec in codecs:
            if codec in line.lower():
                return codec
        return "unknown"

    def extract_abr_from_line(self, line):
        """Extract audio bitrate from format line"""
        # Look for patterns like 128k, 192k, etc.
        abr_match = re.search(r'\b(\d+)k\b', line)
        if abr_match:
            return f"{abr_match.group(1)}k"
        return "N/A"

    def get_resolution_sort_key(self, resolution):
        """Convert resolution to numeric value for sorting"""
        if resolution == "audio only":
            return 0
        if resolution == "N/A":
            return 1
        
        # Extract numeric value from resolution
        match = re.search(r'(\d+)', resolution)
        if match:
            return int(match.group(1))
        
        return 0
    
    def display_formats(self):
        """Display formats based on selected download type"""
        for widget in self.format_scroll.winfo_children():
            widget.destroy()

        download_type = self.download_type.get()
        formats = self.formats_data.get(download_type, [])

        if not formats:
            no_label = ctk.CTkLabel(
                self.format_scroll,
                text=f"❌ No {download_type} formats found",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="red"
            )
            no_label.pack(pady=20)
            return

        for i, format_info in enumerate(formats):
            format_frame = ctk.CTkFrame(self.format_scroll, corner_radius=8)
            format_frame.pack(fill="x", padx=5, pady=5)

            radio = ctk.CTkRadioButton(
                format_frame,
                text="",
                variable=self.selected_format,
                value=format_info['id'],
                width=20
            )
            radio.pack(side="left", padx=10, pady=10)

            info_frame = ctk.CTkFrame(format_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)

            id_label = ctk.CTkLabel(
                info_frame,
                text=f"ID: {format_info['id']} ({format_info['ext']})",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            id_label.pack(anchor="w")

            # Build quality text
            quality_parts = []
            if download_type == 'video':
                if format_info['resolution'] != 'N/A':
                    quality_parts.append(f"Resolution: {format_info['resolution']}")
                if format_info['fps'] != 'N/A':
                    quality_parts.append(f"FPS: {format_info['fps']}")
                if format_info['vcodec'] != 'unknown':
                    quality_parts.append(f"Video: {format_info['vcodec']}")
            elif download_type == 'audio':
                if format_info['abr'] != 'N/A':
                    quality_parts.append(f"Bitrate: {format_info['abr']}")
                if format_info['acodec'] != 'unknown':
                    quality_parts.append(f"Audio: {format_info['acodec']}")

            if format_info['filesize'] != 'N/A':
                quality_parts.append(f"Size: {format_info['filesize']}")

            quality_text = " | ".join(quality_parts) if quality_parts else "No details available"

            quality_label = ctk.CTkLabel(
                info_frame,
                text=quality_text,
                font=ctk.CTkFont(size=11),
                text_color="gray70",
                anchor="w"
            )
            quality_label.pack(anchor="w")

        # Auto-select first format
        if formats:
            self.selected_format.set(formats[0]['id'])

        self.log_output(f"✅ Loaded {len(formats)} {download_type} formats")


    def create_format_option(self, fmt, is_audio=False):
        rb = ctk.CTkRadioButton(
            self.format_frame,
            text="",
            variable=self.selected_format,
            value=fmt["id"]
        )
        rb.pack(anchor="w", padx=10)

        details = f"{fmt['resolution']} | {fmt['size']} | {fmt['codec']} | {fmt['ext']}"
        label = ctk.CTkLabel(self.format_frame, text=details, anchor="w")
        label.pack(anchor="w", padx=40)


    def on_download_type_change(self):
        """Handle download type change"""
        self.display_formats()
    
    def browse_directory(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
    
    def start_download(self):
        """Start the download process"""
        if not self.selected_format.get():
            messagebox.showerror("Error", "Please select a format to download")
            return
        
        if not os.path.exists(self.output_dir.get()):
            messagebox.showerror("Error", "Output directory does not exist")
            return
        
        # Reset progress state
        self.progress_bar.set(0)
        self.progress_text.configure(text="Starting download...")
        
        # Show progress frame and disable download button
        self.download_btn.configure(state="disabled", text="⏳ Downloading...")
        self.progress_frame.pack(fill="x", pady=(0, 20))
        
        url = self.url_var.get().strip()
        format_id = self.selected_format.get()
        output_dir = self.output_dir.get()
        
        self.log_output(f"🚀 Starting download - Format: {format_id}")
        
        def download_thread():
            try:
                # Build command
                cmd = ['yt-dlp']

                if self.download_type.get() == "video":
                    # Use selected video format ID + best audio
                    # This handles cases where format IDs are not numeric
                    selected_format = format_id
                    format_string = f"{selected_format}+bestaudio/best"
                    cmd += ['-f', format_string]
                else:  # audio download
                    cmd += ['-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3']
                
                # Common options
                cmd += [
                    '--embed-subs',
                    '--sub-langs', 'all',
                    '--embed-metadata',
                    '--embed-thumbnail',
                    '-o', os.path.join(output_dir, '%(title)s.%(ext)s'),
                   url
                ]

                
                # Start download process
                self.current_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                
                # Read output
                for line in iter(self.current_process.stdout.readline, ''):
                    if line:
                        self.root.after(0, lambda l=line: self.log_output(l.strip()))
                        # Update progress if possible
                        if '%' in line:
                            try:
                                percent = re.search(r'(\d+(?:\.\d+)?)%', line)
                                if percent:
                                    progress = float(percent.group(1)) / 100
                                    self.root.after(0, lambda p=progress: self.progress_bar.set(p))
                                    self.root.after(0, lambda l=line: self.progress_text.configure(text=l.strip()))
                            except:
                                pass
                
                self.current_process.stdout.close()
                return_code = self.current_process.wait()
                
                if return_code == 0:
                    self.root.after(0, self.download_success)
                else:
                    self.root.after(0, self.download_failed)
                    
            except Exception as e:
                self.root.after(0, lambda: self.download_error(str(e)))
            finally:
                # Always cleanup
                self.root.after(0, self.cleanup_download)
        
        threading.Thread(target=download_thread, daemon=True).start()

    def download_success(self):
        """Handle successful download completion"""
        self.progress_bar.set(1)
        self.progress_text.configure(text="✅ Download completed successfully!")
        self.log_output("✅ Download completed successfully!")
        messagebox.showinfo("Success", "Download completed successfully!")

    def download_failed(self):
        """Handle failed download"""
        self.progress_text.configure(text="❌ Download failed")
        self.log_output("❌ Download failed")

    def download_error(self, error_msg):
        """Handle download error"""
        self.log_output(f"❌ Download error: {error_msg}")
        self.progress_text.configure(text="❌ Download failed")

    def cleanup_download(self):
        """Clean up after download completion"""
        self.download_btn.configure(state="normal", text="⬇️ Start Download")
        self.current_process = None
        # Reset progress after a short delay
        self.root.after(3000, self.reset_progress_display)

    def reset_progress_display(self):
        """Reset progress display after download"""
        if self.current_process is None:  # Only reset if no download is running
            self.progress_bar.set(0)
            self.progress_text.configure(text="Ready to download...")

    def cancel_download(self):
        """Cancel the current download"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=5)  # Wait up to 5 seconds for process to terminate
            except subprocess.TimeoutExpired:
                self.current_process.kill()  # Force kill if it doesn't terminate
            except Exception as e:
                self.log_output(f"Error cancelling download: {str(e)}")
            finally:
                self.current_process = None
                self.progress_text.configure(text="❌ Download cancelled")
                self.log_output("❌ Download cancelled by user")
                self.download_btn.configure(state="normal", text="⬇️ Start Download")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function to run the application"""
    try:
        app = ModernYouTubeDownloader()
        app.run()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        messagebox.showerror("Error", f"Error starting application: {str(e)}")

if __name__ == "__main__":
    main()

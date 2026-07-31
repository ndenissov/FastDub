# FastDub

[![PyPI version](https://img.shields.io/pypi/v/fastdub.svg)](https://pypi.org/project/fastdub/)
[![Downloads](https://static.pepy.tech/badge/fastdub)](https://pepy.tech/project/fastdub)
[![Python versions](https://img.shields.io/pypi/pyversions/fastdub.svg)](https://pypi.org/project/fastdub/)
[![License](https://img.shields.io/pypi/l/fastdub.svg)](https://github.com/ndenissov/FastDub/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/ndenissov/FastDub)](https://github.com/ndenissov/FastDub/stargazers)

FastDub is a Python package and command-line utility for automated subtitle voiceovers, video dubbing, audio ducking, dynamic voice changing, subtitle translation, and YouTube integration.

---

## Features

- **Automated Video Dubbing**: Generate speech from subtitle files (.srt, .vtt) and embed the audio into videos (.mp4, .mkv).
- **Audio Ducking (Sidechain Compression)**: Dynamically lower original background audio level while speech is active.
- **Dynamic Voice Changing**: Switch voices mid-track using subtitle anchors (`!:`).
- **Subtitle Translation**: Auto-translate subtitles to target languages using Google Translate or alternative services.
- **YouTube Integration**: Download video playlists/channels, search YouTube directly from CLI, and upload dubbed videos back to YouTube with translated titles and descriptions.
- **Cross-Platform**: Support for SAPI voices on Windows and eSpeak/RHVoice on Linux.

---

## Installation

### System Dependencies

#### Ubuntu / Debian

```bash
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y python3 python3-pip ffmpeg espeak libxml2-dev libxslt1-dev
```

#### macOS

```bash
brew install ffmpeg espeak
```

### Installing FastDub

#### Via PyPI with pip

```bash
# Core package
pip install FastDub

# Install all optional dependencies (Translation + YouTube support)
pip install "FastDub[ALL]"
```

#### Extra Feature Bundles

| Extra | Description | Command |
| :--- | :--- | :--- |
| `TR` | Subtitle translation support | `pip install "FastDub[TR]"` |
| `YT` | YouTube downloading and search | `pip install "FastDub[YT]"` |
| `YTU` | YouTube video uploading | `pip install "FastDub[YTU]"` |
| `tortoise` | Tortoise-TTS engine support (Heavy) | `pip install "FastDub[tortoise]"` |
| `ALL` | All optional features combined | `pip install "FastDub[ALL]"` |

#### Via Poetry

```bash
poetry add fastdub --extras "all"
```

---

## Quick Start

### Basic Local Video Dubbing

To voiceover all videos in a target directory:

```bash
fastdub -i ./input_folder -v "Yuriy" --no-sidechain -sf srt -vf mp4
```

Or using python module invocation:

```bash
python -m fastdub -i ./input_folder -l ru
```

### Subtitle Translation

Translate subtitles to Russian before voice acting:

```bash
fastdub -i ./input_folder -tr -l ru -ts google
```

### YouTube Download & Dubbing

Process a single YouTube video:

```bash
fastdub -yt -i "https://youtu.be/DD5UKQggXTc" -l ru
```

Process videos from a YouTube Search query:

```bash
fastdub -yt -yts -i "#python" -yts-l 5 -l ru
```

Process an entire YouTube channel:

```bash
fastdub -yt -i "c/UCi-5OZ2tYuwMLIcEyOsbdRA" -l ru
```

### YouTube Upload Setup

To upload processed videos to YouTube (`FastDub[YTU]`):

1. Go to [Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials).
2. Create OAuth 2.0 Client ID for Desktop App.
3. Download the JSON credentials file and place it in your working directory as `client_secrets.json`.
4. Run FastDub with upload flags:

```bash
fastdub -i ./input_folder -ytu -ytu-ps private -ytu-t
```

---

## Advanced Usage

### Dynamic Voice Anchors

Change the active voice actor for specific sections by inserting anchor tokens in your subtitle file.

Example SRT subtitle content:

```srt
1
00:00:01,000 --> 00:00:04,000
!:Yuriy Hello, welcome to this video!

2
00:00:04,500 --> 00:00:08,000
!:Elena Here is the next speaker.
```

If voice anchors are updated and cached files need to be refreshed, clear the cache using `-rc`:

```bash
fastdub -i ./input_folder -rc 1
```

### Tortoise-TTS Support

FastDub now supports [Tortoise-TTS](https://github.com/neonbjb/tortoise-tts) for high-quality voice cloning and text-to-speech. Tortoise generates highly realistic voices but requires significantly more processing power (CUDA is highly recommended).

1. **Install with Tortoise support**:
   ```bash
   pip install "FastDub[tortoise]"
   ```
2. **Use the Tortoise engine**:
   Specify `--tts-engine tortoise`. You can use any Tortoise voice preset (e.g., `random`, `angie`, `train_atkins`) as the voice argument.
   ```bash
   fastdub -i ./input_folder -te tortoise -v random
   ```
3. **Tortoise Presets (Quality vs Speed)**:
   By default, FastDub uses the `fast` preset for Tortoise. You can change this using the `--tortoise-preset` argument:
   ```bash
   fastdub -i ./input_folder -te tortoise -tp high_quality -v angie
   ```
   *Available presets*: `ultra_fast`, `fast`, `standard`, `high_quality`.

---

## Command Line Arguments Reference

```text
usage: fastdub [-h] [-rc {0,1,2}] [-ra | --cleanup-audio | -n-ra | --no-cleanup-audio]
               [-ev | --export-video | -n-ev | --no-export-video] [-l LANGUAGE]
               [-ll {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
               [-tc THREADS_COUNT] -i INPUT [-vf VIDEO_FORMAT] [-sf SUBTITLES_FORMAT]
               [-En EXCLUDE [EXCLUDE ...]] [-Eu EXCLUDE_UNDERSCORE]
               [-sc | --sidechain | -n-sc | --no-sidechain]
               [-sc-args SIDECHAIN_FFMPEG_PARAMS] [-sc-lvl SIDECHAIN_LEVEL_SC]
               [-v VOICE] [-a ALIGN] [-v-set-a VOICE_SET_ANCHOR]
               [-fll {trace,debug,verbose,info,warning,error,fatal,panic,quiet}]
               [-y | --confirm | -n-y | --no-confirm] [-af AUDIO_FORMAT] [-wm WATERMARK]
               [-tb | --traceback | -n-tb | --no-traceback] [-yt]
               [-ak API_KEYS [API_KEYS ...]] [-yts] [-yts-l YOUTUBE_SEARCH_LIMIT]
               [-yts-rg YOUTUBE_SEARCH_REGION] [-ytu]
               [-ytu-ps {private,public,unlisted}] [-ytu-t] [-tr] [--rewrite-srt | --no-rewrite-srt]
               [-ts TRANSLATE_SERVICE]
```

---

## Python API Usage

FastDub modules can be imported directly into Python applications:

```python
from fastdub import GlobalSettings, dubber

GlobalSettings.language = "ru"
GlobalSettings.threads_count = 4

# Perform dubbing operation programmatically
dubber.dub(
    input_dir="./media",
    voice="Yuriy",
    export_video=True,
    sidechain=True
)
```

---

## Development & Publishing

FastDub uses [Poetry](https://python-poetry.org/) for build backend management.

### Build Package

```bash
poetry build
```

### Publish Package

```bash
poetry publish
```

---

## Issues & Support

If you encounter any issues or have feature requests, please open an issue on [GitHub Issues](https://github.com/ndenissov/FastDub/issues).

---

## License

Distributed under the MIT License. See [LICENSE](https://github.com/ndenissov/FastDub/blob/main/LICENSE) for details.

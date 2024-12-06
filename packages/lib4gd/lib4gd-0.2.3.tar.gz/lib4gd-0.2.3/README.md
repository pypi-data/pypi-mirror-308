# lib4gd

**lib4gd** is a Python library designed for efficient image handling, Google Drive, and SFTP file downloading. It also provides resource management for consistent concurrency control.

## Features

- **Image Handling:** 
  - Convert images between Base64, PIL, and OpenCV formats.
  - Batch process images with efficient concurrency.

- **File Downloading:**
  - Download files from Google Drive using service account credentials.
  - Download files from SFTP servers with parallel processing.

- **Resource Management:**
  - Centralized control of thread pools and semaphores for consistent concurrency management across the library.

## Installation

### Install via SSH
```bash
pip install git+ssh://git@github.com/4dg-ai/lib4gd.git
```

### Install via HTTPS with Personal Access Token
```bash
pip install git+https://<username>:<token>@github.com/4dg-ai/lib4gd.git
```

Replace `<username>` with your GitHub username and `<token>` with your Personal Access Token.

## Submodules

- [Image Handling](lib4gd/image_handling/README.md)
- [Google Drive Downloading](lib4gd/image_downloading/README.md#google-drive-downloading)
- [SFTP Downloading](lib4gd/image_downloading/README.md#sftp-downloading)
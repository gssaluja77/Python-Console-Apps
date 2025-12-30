import yt_dlp
import os
import sys


def download_playlist(playlist_url):
    """Download an entire YouTube playlist."""
    if getattr(sys, "frozen", False):
        app_dir = os.path.dirname(sys.executable)
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(
            app_dir, "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
        ),
        "noplaylist": False,
        "ignoreerrors": True,
        "quiet": False,
        "no_warnings": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print("\n🎬 Starting playlist download...\n")
            ydl.download([playlist_url])
            print("\n✅ Playlist download completed!\n")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")


def download_single_video(video_url):
    """Download a single YouTube video."""
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        app_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        app_dir = os.path.dirname(os.path.abspath(__file__))

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(app_dir, "YT_Videos/%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print("\n🎬 Starting video download...\n")
            ydl.download([video_url])
            print("\n✅ Video download completed!\n")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")


def main():
    """Main function to handle user input and download choice."""
    os.system("clear" if os.name != "nt" else "cls")

    print("=" * 50)
    print("🎥 YouTube Downloader")
    print("=" * 50)
    print("\nChoose an option:")
    print("1. Download a single video")
    print("2. Download a playlist")
    print("3. Exit")
    print("-" * 50)

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        video_url = input("\nEnter the YouTube video URL: ").strip()
        if video_url:
            download_single_video(video_url)
        else:
            print("\n❌ No URL provided. Exiting...\n")

    elif choice == "2":
        playlist_url = input("\nEnter the YouTube playlist URL: ").strip()
        if playlist_url:
            download_playlist(playlist_url)
        else:
            print("\n❌ No URL provided. Exiting...\n")

    elif choice == "3":
        print("\n👋 Goodbye!\n")

    else:
        print("\n❌ Invalid choice. Please run the script again.\n")


if __name__ == "__main__":
    main()

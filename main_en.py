import argparse
import os
import sys
import time

import fpstimer

# hide pygame's startup banner
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# settings
FPS = 30
FRAME_DURATION = 1.0 / FPS  # seconds per frame
CACHE_FILE = "TextFiles/bad_apple_all.txt"
MP3_PATH = "bad-apple-audio.mp3"
MIDI_PATH = "alstroemeria_records_bad_apple.mid"


def load_frames(file_path):
    """Load ASCII data and return a list of frames."""
    if not os.path.exists(file_path):
        print(f"Error: '{file_path}' not found.")
        print("Check the TextFiles folder and file name.")
        return []

    print("Loading text file... please wait.")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
    except OSError as e:
        print(f"Error: failed to read the file: {e}")
        return []

    # split by <<<FRAME>>> and drop empty frames
    frames = [frame for frame in data.split("\n<<<FRAME>>>\n") if frame.strip()]
    if not frames:
        print("Error: frame data is empty. The file may be corrupted.")
        return []
    print(f"Loaded {len(frames)} frames.")
    return frames


def init_audio():
    """Initialize pygame's audio. Returns False on failure."""
    try:
        pygame.init()
        pygame.mixer.init(44100, -16, 2, 2048)
        return True
    except Exception as e:
        print(f"[Error] Failed to initialize audio: {e}")
        return False


def play_audio(audio_path):
    """Load and start playing an audio file. Returns False on failure."""
    if not os.path.exists(audio_path):
        print(f"[Error] Audio file '{audio_path}' not found.")
        return False
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        return True
    except Exception as e:
        print(f"[Error] Failed to play audio '{audio_path}': {e}")
        return False


def stop_audio():
    """Stop the currently playing audio."""
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass


def play_video(frames):
    """Render frames in sync with the audio playback position at 30 FPS."""
    if not frames:
        return

    sys.stdout.write("\033[2J")
    last_frame_index = -1

    try:
        # use the audio playback position (ms) to compute which frame to draw
        # get_pos() returns -1 before playback starts, so wait until it is >= 0
        while pygame.mixer.music.get_pos() < 0:
            time.sleep(0.005)

        while True:
            elapsed_ms = pygame.mixer.music.get_pos()
            if elapsed_ms < 0:
                # track ended (or was stopped)
                break

            target_index = int(elapsed_ms / 1000.0 / FRAME_DURATION)
            if target_index >= len(frames):
                break

            # avoid redrawing the same frame; skip ahead to stay in sync
            if target_index != last_frame_index:
                sys.stdout.write("\033[H" + frames[target_index])
                sys.stdout.flush()
                last_frame_index = target_index

            # wait until the next frame time (fpstimer keeps an accurate interval)
            next_time = (target_index + 1) * FRAME_DURATION
            timer = fpstimer.FPSTimer(FPS)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n[Error] Something went wrong during playback: {e}")
    finally:
        stop_audio()
        sys.stdout.write("\n" * 5)
        print("Playback finished!")


def main():
    parser = argparse.ArgumentParser(description="Play Bad Apple!! as ASCII art on the console")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--mp3", action="store_true", help="play with mp3 immediately (skip menu)")
    group.add_argument("--midi", action="store_true", help="play with MIDI immediately (skip menu)")
    args = parser.parse_args()

    frames = load_frames(CACHE_FILE)
    if not frames:
        sys.exit(1)

    if not init_audio():
        sys.exit(1)

    # skip the menu and play directly when an argument is given
    if args.mp3:
        if play_audio(MP3_PATH):
            play_video(frames)
        return
    if args.midi:
        if play_audio(MIDI_PATH):
            play_video(frames)
        return

    while True:
        print("\n" + "=" * 40)
        print(" Playback options")
        print(" 1) play with mp3")
        print(" 2) play with MIDI")
        print(" 3) exit")
        print("=" * 40)

        choice = input("Enter a number (1-3): ").strip()

        if choice == "1":
            if play_audio(MP3_PATH):
                play_video(frames)
        elif choice == "2":
            if play_audio(MIDI_PATH):
                play_video(frames)
        elif choice == "3":
            print("Exiting")
            break
        else:
            print("Invalid input, choose 1, 2, or 3")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop_audio()
        print("\nForced exit")
        sys.exit(0)

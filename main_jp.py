import argparse
import os
import sys
import time

import fpstimer

# pygame の起動メッセージを消す
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# 設定
FPS = 30
FRAME_DURATION = 1.0 / FPS  # 1フレームの秒数
CACHE_FILE = "TextFiles/bad_apple_all.txt"
MP3_PATH = "bad-apple-audio.mp3"
MIDI_PATH = "alstroemeria_records_bad_apple.mid"


def load_frames(file_path):
    """アスキーデータを読み込んでフレームのリストを返す。"""
    if not os.path.exists(file_path):
        print(f"エラー: '{file_path}' が見つからないよ。")
        print("TextFilesフォルダとかファイル名が合ってるか確認してみて。")
        return []

    print("テキストファイルを読み込み中... ちょっと待ってね。")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
    except OSError as e:
        print(f"エラー: ファイルの読み込みに失敗したみたい: {e}")
        return []

    # <<<FRAME>>> で分割し、空っぽのフレームは捨てる
    frames = [frame for frame in data.split("\n<<<FRAME>>>\n") if frame.strip()]
    if not frames:
        print("エラー: フレームデータが空っぽだよ。ファイルが壊れてないか確認して。")
        return []
    print(f"よし、{len(frames)} フレームのデータを読み込んだよ。")
    return frames


def init_audio():
    """pygame の音声機能を初期化する。失敗時は False を返す。"""
    try:
        pygame.init()
        pygame.mixer.init(44100, -16, 2, 2048)
        return True
    except Exception as e:
        print(f"[エラー] 音声の初期化に失敗したみたい: {e}")
        return False


def play_audio(audio_path):
    """音声ファイルを読み込んで再生開始する。失敗時は False を返す。"""
    if not os.path.exists(audio_path):
        print(f"[エラー] 音声ファイル '{audio_path}' が見つからないよ。")
        return False
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        return True
    except Exception as e:
        print(f"[エラー] オーディオ '{audio_path}' の再生に失敗したみたい: {e}")
        return False


def stop_audio():
    """再生中の音声を止める。"""
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass


def play_video(frames):
    """音声の再生位置に合わせてフレームを 30FPS でコンソールに出力する。"""
    if not frames:
        return

    sys.stdout.write("\033[2J")
    last_frame_index = -1

    try:
        # 音声の再生位置（ミリ秒）を基準に、今描くべきフレームを計算する
        # get_pos() は再生開始前は -1 を返すので、0 以上になるまで待つ
        while pygame.mixer.music.get_pos() < 0:
            time.sleep(0.005)

        while True:
            elapsed_ms = pygame.mixer.music.get_pos()
            if elapsed_ms < 0:
                # 曲が終わった（stop された）ら抜ける
                break

            target_index = int(elapsed_ms / 1000.0 / FRAME_DURATION)
            if target_index >= len(frames):
                break

            # 同じフレームなら再描画せず、飛ばすべき分は一気に進めて同期を維持
            if target_index != last_frame_index:
                sys.stdout.write("\033[H" + frames[target_index])
                sys.stdout.flush()
                last_frame_index = target_index

            # 次のフレーム時刻まで待つ（fpstimer で正確な間隔を死守）
            next_time = (target_index + 1) * FRAME_DURATION
            timer = fpstimer.FPSTimer(FPS)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n[エラー] 再生中に問題が起きたみたい: {e}")
    finally:
        stop_audio()
        sys.stdout.write("\n" * 5)
        print("再生終了！")


def main():
    parser = argparse.ArgumentParser(description="コンソールで Bad Apple!! をアスキーアート再生")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--mp3", action="store_true", help="mp3で即再生（メニューを省略）")
    group.add_argument("--midi", action="store_true", help="MIDIで即再生（メニューを省略）")
    args = parser.parse_args()

    frames = load_frames(CACHE_FILE)
    if not frames:
        sys.exit(1)

    if not init_audio():
        sys.exit(1)

    # 引数指定があればメニューを省略して即再生
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
        print(" 再生の方法")
        print(" 1) mp3で再生")
        print(" 2) MIDIで再生")
        print(" 3) 終了する")
        print("=" * 40)

        choice = input("番号を入力 (1-3): ").strip()

        if choice == "1":
            if play_audio(MP3_PATH):
                play_video(frames)
        elif choice == "2":
            if play_audio(MIDI_PATH):
                play_video(frames)
        elif choice == "3":
            print("終了")
            break
        else:
            print("無効な入力、1、2、3のどれかを選んでください")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop_audio()
        print("\n強制終了")
        sys.exit(0)

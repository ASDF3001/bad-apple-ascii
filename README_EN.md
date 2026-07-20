# bad-apple

A Python program that plays Bad Apple!! as ASCII art on the console (terminal).

Works on both Windows and Linux.

> For the Japanese version, see [README_JP.md](README_JP.md).

---

## File structure

```
.
├── main_jp.py                           # Japanese playback program
├── main_en.py                           # English playback program
├── requirements.txt                     # required libraries
├── memo.txt                             # usage notes (Japanese)
├── bad-apple-audio.mp3                  # audio for mp3 playback
├── alstroemeria_records_bad_apple.mid   # audio for MIDI playback
└── TextFiles/
    └── bad_apple_all.txt                # ASCII art data
```

The ASCII data is bundled into a single file `TextFiles/bad_apple_all.txt`; the program reads only this file.

## How to run

1. Install the required libraries:

   ```
   pip install -r requirements.txt
   ```

2. Run the program:

   ```
   python main_en.py
   ```

   (use `python3 main_en.py` if `python` is not available)

3. Choose a playback option from the menu:

   - `1` play with mp3
   - `2` play with MIDI
   - `3` exit

Press `Ctrl+C` during playback to stop.

## Notes

- Playback runs at 30 FPS.
- When playing MIDI, if no sound comes out (e.g. on Linux), you may need to install a MIDI sound font — see `memo.txt` for details.

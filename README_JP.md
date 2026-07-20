# bad-apple

コンソール（ターミナル）に Bad Apple!! をアスキーアートで再生する Python プログラム。

Windows / Linux の両方で動作します。

> 英語版は [README_EN.md](README_EN.md) を参照してください。

---

## ファイル構成 / File structure

```
.
├── main_jp.py                           # 日本語版再生プログラム / Japanese playback program
├── main_en.py                           # 英語版再生プログラム / English playback program
├── requirements.txt                     # 必要なライブラリ一覧 / required libraries
├── memo.txt                             # 動かし方メモ / usage notes
├── bad-apple-audio.mp3                  # 音声ファイル（mp3再生用）/ audio for mp3 playback
├── alstroemeria_records_bad_apple.mid   # 音声ファイル（MIDI再生用）/ audio for MIDI playback
└── TextFiles/
    └── bad_apple_all.txt                # アスキーアートのデータ / ASCII art data
```

アスキーデータは `TextFiles/bad_apple_all.txt` 1 本にまとまっていて、プログラムはこのファイルだけを読み込みます。

## 動かし方

1. 必要なライブラリをインストールします。

   ```
   pip install -r requirements.txt
   ```

2. プログラムを実行します。

   ```
   python main_jp.py
   ```

   （環境によっては `python3 main_jp.py` としてください）

3. メニューで再生方法を選びます。:

   - `1` mp3 で再生 
   - `2` MIDI で再生
   - `3` 終了 

再生中は `Ctrl+C` で停止できます。

## 動作の注意点 

- 30FPS で再生されます。
- MIDI を再生する場合、Linux 環境などで音が鳴らないときは音源の導入が必要です（詳しくは `memo.txt` を参照。
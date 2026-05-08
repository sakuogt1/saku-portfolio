import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

# パスの設定（ご自身の環境に合わせて調整してください）
SOURCE_DIR = Path.home() / "Desktop/portfolio/cover art"
DEST_DIR = Path.home() / "Desktop/portfolio/webp cover art"

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
            self.convert_image(event.src_path)

    def convert_image(self, file_path):
        try:
            # フォルダがなければ作成
            DEST_DIR.mkdir(parents=True, exist_ok=True)
            
            with Image.open(file_path) as img:
                # リサイズ処理（横幅最大700px、比率維持）
                if img.width > 700:
                    ratio = 700 / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    img = img.resize((700, new_height), Image.Resampling.LANCZOS)
                
                # 出力ファイル名の作成
                target_path = DEST_DIR / f"{Path(file_path).stem}.webp"
                
                # 保存
                img.save(target_path, "WEBP", quality=80)
                print(f"Converted: {target_path.name}")
        except Exception as e:
            print(f"Error converting {file_path}: {e}")

if __name__ == "__main__":
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, str(SOURCE_DIR), recursive=False)
    observer.start()
    print(f"Monitoring: {SOURCE_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
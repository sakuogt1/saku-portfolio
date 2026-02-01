import os
from PIL import Image
import sys

def process_image(input_path, output_folder):
    try:
        with Image.open(input_path) as img:
            # 1. リサイズ（横幅最大700px、アスペクト比維持）
            if img.width > 700:
                ratio = 700 / float(img.width)
                new_height = int(float(img.height) * ratio)
                img = img.resize((700, new_height), Image.Resampling.LANCZOS)
            
            # 2. ファイル名と保存先の設定
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_folder, f"{base_name}.webp")
            
            # 3. WebPとして保存
            img.save(output_path, "WEBP")
            print(f"Success: {output_path}")
            
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

if __name__ == "__main__":
    # 引数からファイルパスを受け取る（フォルダアクション用）
    if len(sys.argv) > 1:
        # 保存先フォルダをここで指定（デスクトップの 'converted' フォルダなど）
        save_dir = os.path.expanduser("~/Desktop/portfolio/webp cover art")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        for file_path in sys.argv[1:]:
            process_image(file_path, save_dir)
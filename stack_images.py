import os
import sys
from PIL import Image

def get_image_files(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith('.png')]
    if not files:
        sys.exit('no png files found in {}'.format(folder))
    try:
        files.sort(key=lambda f: int(os.path.splitext(f)[0]))
    except ValueError:
        files.sort()
    return [os.path.join(folder, f) for f in files]

def create_canvas(image_paths):
    sizes = [Image.open(p).size for p in image_paths]
    widths, heights = zip(*sizes)
    return Image.new('RGBA', (max(widths), sum(heights)), (0, 0, 0, 0))

def stack_images(image_paths, output_path):
    canvas = create_canvas(image_paths)
    y_offset = 0
    for path in image_paths:
        img = Image.open(path).convert('RGBA')
        canvas.paste(img, (0, y_offset), img)
        y_offset += img.size[1]
    canvas.save(output_path)

if __name__ == '__main__':
    output = 'stacked.png'
    image_paths = get_image_files(os.getcwd())
    stack_images(image_paths, output)


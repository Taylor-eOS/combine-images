import os
import re
import sys
from PIL import Image

def get_image_files(folder):
    files=[f for f in os.listdir(folder) if f.lower().endswith('.png')]
    if not files:
        sys.exit('no png files found in {}'.format(folder))
    def num(f):
        base=os.path.splitext(f)[0]
        m=re.match(r'(\d+)$',base)
        return int(m.group(1)) if m else float('inf')
    files.sort(key=num)
    return [os.path.join(folder,f) for f in files]

def create_canvas(image_paths):
    sizes = [Image.open(p).size for p in image_paths]
    widths, heights = zip(*sizes)
    return Image.new('RGBA', (max(widths), sum(heights)), (0, 0, 0, 0))

def stack_images(image_paths,output_path):
    canvas=Image.open(image_paths[0]).convert('RGBA')
    for path in image_paths[1:]:
        img=Image.open(path).convert('RGBA')
        w=max(canvas.width,img.width)
        h=canvas.height+img.height
        new_canvas=Image.new('RGBA',(w,h),(0,0,0,0))
        new_canvas.paste(canvas,(0,0),canvas)
        new_canvas.paste(img,(0,canvas.height),img)
        canvas=new_canvas
    bg=Image.new('RGB',canvas.size,(255,255,255))
    bg.paste(canvas,(0,0),canvas)
    bg.save(output_path,'JPEG')

if __name__ == '__main__':
    output = 'stacked.png'
    image_paths = get_image_files(os.getcwd())
    stack_images(image_paths, output)


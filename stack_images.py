import os
import re
import sys
from PIL import Image

def get_image_files(folder):
    files=[f for f in os.listdir(folder) if f.lower().endswith('.png')]
    if not files:
        sys.exit('no png files found in {}'.format(folder))
    num_pat=re.compile(r'^(\d+)\.png$',re.IGNORECASE)
    scr_pat=re.compile(r'^Screenshot_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.png$')
    num_files=[]; scr_files=[]
    for f in files:
        if num_pat.match(f):
            num_files.append(f)
        elif scr_pat.match(f):
            scr_files.append(f)
        else:
            print('Omitting {}: name does not match numeric or Screenshot format.'.format(f))
    if num_files and scr_files:
        print('Both numeric and Screenshot files detected; using numeric ones only.')
        chosen=num_files
        sort_key=lambda f:int(num_pat.match(f).group(1))
    elif num_files:
        chosen=num_files
        sort_key=lambda f:int(num_pat.match(f).group(1))
    elif scr_files:
        chosen=scr_files
        sort_key=lambda f:scr_pat.match(f).group(1)
    else:
        sys.exit('no properly named png files found in {}'.format(folder))
    chosen.sort(key=sort_key)
    return [os.path.join(folder,f) for f in chosen]

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


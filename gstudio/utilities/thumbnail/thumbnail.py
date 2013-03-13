from PIL import Image
import glob, os

for infile in glob.glob("*.jpg"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    width, height = im.size
    sizem = 1024,height
    if int(width) > 1024:
        imm.thumbnail(sizem, Image.ANTIALIAS)
        imm.save(file + "_display_1024","JPEG")
    else:
        imm.thumbnail(width,height,Image.ANTIALIAS)
        imm.save(file + "_display_1024","JPEG")

for infile in glob.glob("*.png"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    width, height = im.size
    sizem = 1024,height
    if int(width) > 1024:
        imm.thumbnail(sizem, Image.ANTIALIAS)
        imm.save(file + "_display_1024","JPEG")
    else:
        imm.thumbnail(width,height,Image.ANTIALIAS)
        imm.save(file + "_display_1024","JPEG")

for infile in glob.glob("*.tif"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    width, height = im.size
    sizem = 1024,height
    if int(width) > 1024:
        imm.thumbnail(sizem, Image.ANTIALIAS)
        imm.save(file + "_display_1024","JPEG")
    else:
        imm.thumbnail(width,height,Image.ANTIALIAS)
        imm.save(file + "_display_1024","JPEG")

from PIL import Image
import glob, os

#for infile in glob.glob("100-extremely-detailed-macro-insect-photos56jpg"):
for infile in glob.glob("damitr/*.*"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    width, height = im.size
    sizem = 1024,height
    if int(width) > 1024:
        im.thumbnail(sizem, Image.ANTIALIAS)
        im.save(file + "_display_1024","JPEG")
    else:
        im.thumbnail(im.size,Image.ANTIALIAS)
        im.save(file + "_display_1024","JPEG")




from PIL import ImageFont, ImageDraw, Image

image = Image.open('certificate.jpg')
draw = ImageDraw.Draw(image)

widths = [610, 530, 140, 170]
heights = [40, 90, 16, 15]

startx = [210, 250, 700, 720]
starty = [450, 300, 590, 70]

txts = ["Behaviour of Something Stuff and Data Analysis", "Bishu Das", "12/13/2876", "EXTSD-83434-E@ASD-333getout"]
size = [10,10,10,10]
ttf  = ["Gabriola.ttf", "mighty.otf", "DejaVuSans.ttf", "DejaVuSans.ttf"]
fonts = [ImageFont.truetype(ttf[i], size[i]) for i in range(4)]


for i in range(4):
    iw,ih = widths[i],heights[i]
    while True:
        fw,fh = fonts[i].getsize(txts[i])
        if fw>iw or fh>ih:
            break
        size[i]+=1
        fonts[i] = ImageFont.truetype(ttf[i], size[i])
    alpha = 255 if i!=3 else 120
    r = 0 if i!=1 else 126
    g = 0 if i!=1 else 27
    b = 0 if i!=1 else 50
    dx = iw-fw if iw-fw>=0 else 0
    dy = ih-fh if ih-fh>=0 else 0
    sx = startx[i]+(dx//2)
    sy = starty[i]+(dy//2)
    draw.text((sx,sy), txts[i], font=fonts[i], fill=(r,g,b,alpha))
    print("final size", i, size[i])
image.save('fontest2.jpg')

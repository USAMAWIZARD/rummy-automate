from PIL import Image,ImageFilter

img = Image.open("2.png")
img = img.convert("L")
img = img.filter(ImageFilter.FIND_EDGES)
img.save("result.png")

#0.00999903678894043-0.05800223350524902
#520*0.00999903678894043=0.05800223350524902
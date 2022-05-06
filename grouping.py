from PIL import Image,ImageFilter

img = Image.open("2.png")
img = img.convert("L")
img = img.filter(ImageFilter.FIND_EDGES)
img.save("result.png")
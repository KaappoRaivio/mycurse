from PIL import ImageFont, Image, ImageDraw, ImageColor



# with open("opacity/FiraCode-Regular.ttf") as file:
#     for i in file:
#         print(i)


image = Image.new("RGB", (640, 400), ImageColor.getrgb("white"))
draw = ImageDraw.Draw(image, "RGB")

font = ImageFont.truetype("opacity/FiraCode-Regular.ttf")


mask = font.getmask("testi", "1")
print(dir(mask))
mask.show()


draw.text((10, 10), "hello", (0, 0, 0), font=font)

image.show()
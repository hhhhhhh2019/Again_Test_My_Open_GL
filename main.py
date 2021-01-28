from camera import *
from model import *
from bmp_image import *
import cProfile


Infinity = (2**31)

img = Image(800, 800)
zbuffer = [-Infinity] * (img.width * img.height)
zbuffer_img = Image(img.width, img.height)

camera = Camera(np.array([0, 0, 0]), img.width, img.height)

objects = [
    load_obj(np.array([0, 0, 0]), 'object.obj')
]

print("drawing models")
for i in objects:
    i.draw(img, zbuffer, camera)

print("save image")
img.save("image.bmp")

print("draw zbuffer")
for i in range(len(zbuffer)):
    x = i % img.width
    y = i // img.width
    zbuffer_img.point(x, y, zbuffer[i])

print("save zbuffer")
zbuffer_img.save("zbuffer.bmp")
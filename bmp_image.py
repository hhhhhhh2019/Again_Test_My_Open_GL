import math

def list_to_string(s):
	str1 = ""
	for i in s:
		str1 += i
	return str1


class Image:
    def __init__(self, w, h, c = [0, 0, 0, 255]):
        self.width, self.height = w, h
        self.data = [c] * (w * h)

    def save(self, filename):
        with open(filename, "w+b") as f:
            f.write(b"BM")
            # 122 - размер настроек bmp
            f.write((122 + self.width * self.height * 3).to_bytes(4,byteorder="little"))
            f.write((0).to_bytes(2,byteorder="little")) # неисп.
            f.write((0).to_bytes(2,byteorder="little")) # неисп.
            f.write((122).to_bytes(4,byteorder="little")) # смещение до цветов(размер настроек)
            f.write((108).to_bytes(4,byteorder="little")) # кол-во байт в DIB заголовке
            f.write((self.width).to_bytes(4,byteorder="little")) # ширина
            f.write((self.height).to_bytes(4,byteorder="little")) # высота
            f.write((1).to_bytes(2,byteorder="little")) # кол-во использ. цветовых плостостей
            f.write((32).to_bytes(2,byteorder="little")) # кол-во бит на пиксель
            f.write((3).to_bytes(4,byteorder="little")) # без сжатия
            f.write((32).to_bytes(4,byteorder="little")) # размер необработанных данных растрового изображения (включая заполнение)
            f.write((2835).to_bytes(4,byteorder="little")) # разрешение печати изображения
            f.write((2835).to_bytes(4,byteorder="little")) # не понял зачем это, но так надо
            f.write((0).to_bytes(4,byteorder="little")) # 0 цветов в палитре
            f.write((0).to_bytes(4,byteorder="little")) # 0 важных цветов(все цвета важны)
            f.write(b"\x00\x00\xFF\x00") # красная маска
            f.write(b"\x00\xFF\x00\x00") # зеленая маска
            f.write(b"\xFF\x00\x00\x00") # синяя маска
            f.write(b"\x00\x00\x00\xFF") # маска прозрачности
            f.write(b" niW") # "Win " LCS_WINDOWS_COLOR_SPACE
            f.write((0).to_bytes(36,byteorder="little")) # неисп. с Win
            f.write((0).to_bytes(4,byteorder="little")) # неисп. с Win
            f.write((0).to_bytes(4,byteorder="little")) # неисп. с Win
            f.write((0).to_bytes(4,byteorder="little")) # неисп. с Win

            for i in self.data:
                color = b""
                for c in i:
                    c = 0 if not math.isfinite(c) else int(c)
                    c = min(255, max(0, c))
                    cl = list(hex(c)[2:])
                    if len(cl) == 1:
                        cl.insert(0, "0")
                    color += bytes.fromhex(list_to_string(cl))

                f.write(color)
    
    def point(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            if not (isinstance(color, list) or isinstance(color, tuple)):
                color = [color]

            color, x, y = list(color), int(x), int(y)

            for i in color:
                i = int(i)

            if len(color) == 1:
                color = [color[0], color[0], color[0]]

            if len(color) == 4:
                a = color[:3]
                a.reverse()
                color = a + color[3]

            if len(color) == 3:
                color.reverse()
                color += [255]

            self.data[x+y*self.width] = color
    
    def get(self, x, y):
        x, y = int(x), int(y)
        x = min(0, max(self.width - 1, x))
        y = min(0, max(self.height - 1, y))
        return self.data[x+y*self.width]
    
    def flip_horizontal(self):
        max_h = self.height // 2
        if not self.height % 2 == 0:
            max_h += 1
        
        for y in range(max_h):
            for x in range(self.width):
                a = self.data[x+(self.height - 1 - y)*self.width]
                
                self.data[x+(self.height - 1 - y)*self.width] = self.data[x+y*self.width]

                self.data[x+y*self.width] = a
    
    def flip_vertical(self):
        max_w = self.width // 2
        if not self.width % 2 == 0:
            max_w += 1
        
        for x in range(max_w):
            for y in range(self.height):
                a = self.data[x+(self.height - 1 - y)*self.width]
                
                self.data[x+(self.height - 1 - y)*self.width] = self.data[x+y*self.width]

                self.data[x+y*self.width] = a
    
    def line(self, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)


        steep = False

        if abs(x0-x1) < abs(y0-y1):
            x0, y0 = y0, x0
            x1, y1, = y1, x1
            steep = True
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dx = x1 - x0
        dy = y1 - y0
        derror2 = abs(dy) * 2
        error2 = 0
        y = y0
        for x in range(x0, x1):
            if steep:
                self.point(y, x, color)
            else:
                self.point(x, y, color)
            
            error2 += derror2

            if error2 > dx:
                y += 1 if y1 > y0 else -1
                error2 -= dx * 2
    
    def polygon(self, polygon, color):
        last_point = polygon[0]

        for p in polygon:
            self.line(*last_point, *p, color)
            last_point = p
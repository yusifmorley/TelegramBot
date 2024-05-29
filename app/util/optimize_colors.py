import math
import colorsys


def hex_to_rgb(hex_color):
    """Convert a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb_color):
    """Convert an RGB tuple to a hex color string."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


def rgb_to_relative_luminance(r, g, b):
    """Calculate the relative luminance of an RGB color."""
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r = adjust(r)
    g = adjust(g)
    b = adjust(b)

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(l1, l2):
    """Calculate the contrast ratio between two luminances."""
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)


class HColor:
    """
    :param r: 0-255
    :param g: 0-255
    :param b: 0-255
    """

    def __init__(self, r, g, b):
        r /= 255.0
        g /= 255.0
        b /= 255.0

        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        self.h = h * 360  # 0-360
        self.s = s  # 0-1
        self.v = v  # 0-1

    def plus_H(self, hv: int):
        self.h = (self.h + hv) % 360  # Ensure h is within 0-360
        return self.h

    def get_difference_from_hsv(self, h, s, v):
        return math.sqrt((self.h - h) ** 2 + (self.s - s) ** 2 + (self.v - v) ** 2)

    def get_contrasting(self):
        contrasting_h = (self.h + 180) % 360  # Ensure h is within 0-360
        return contrasting_h, self.s, self.v

    def to_rgb(self):
        r, g, b = colorsys.hsv_to_rgb(self.h / 360, self.s, self.v)
        return int(r * 255), int(g * 255), int(b * 255)

    def to_relative_luminance(self):
        r, g, b = self.to_rgb()
        return rgb_to_relative_luminance(r, g, b)


def adjust_font_color(bg_color, font_color):
    """Adjust font color to ensure adequate contrast with the background color."""
    bg_luminance = bg_color.to_relative_luminance()
    font_luminance = font_color.to_relative_luminance()

    if contrast_ratio(bg_luminance, font_luminance) < 4.5:
        # If contrast is too low, adjust the font color
        new_h = (font_color.h + 180) % 360
        font_color.h = new_h
        font_color.s = min(1.0, font_color.s * 1.2)
        font_color.v = min(1.0, font_color.v * 1.2)

    return font_color


def optimize_colors(bg_hex, font_hex1, font_hex2):
    bg_rgb = hex_to_rgb(bg_hex)
    font_rgb1 = hex_to_rgb(font_hex1)
    font_rgb2 = hex_to_rgb(font_hex2)

    bg_color = HColor(*bg_rgb)
    font_color1 = HColor(*font_rgb1)
    font_color2 = HColor(*font_rgb2)

    font_color1 = adjust_font_color(bg_color, font_color1)
    font_color2 = adjust_font_color(bg_color, font_color2)

    optimized_bg = bg_color.to_rgb()
    optimized_font1 = font_color1.to_rgb()
    optimized_font2 = font_color2.to_rgb()

    return rgb_to_hex(optimized_bg), rgb_to_hex(optimized_font1), rgb_to_hex(optimized_font2)


# 示例用法
# bg_hex = "#1e1e1e"  # 背景色
# font_hex1 = "#646464"  # 字体颜色1
# font_hex2 = "#c8c8c8"  # 字体颜色2
#
# optimized_bg, optimized_font1, optimized_font2 = optimize_colors(bg_hex, font_hex1, font_hex2)
# print("优化后的颜色：")
# print("背景色：", optimized_bg)
# print("字体颜色1：", optimized_font1)
# print("字体颜色2：", optimized_font2)

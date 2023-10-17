
def parse_hex(hex_str):
    return int(hex_str, 16)

def parse_color(color):
    if len(color) != 6:
        return None

    red = parse_hex(color[0:2])
    green = parse_hex(color[2:4])
    blue = parse_hex(color[4:6])

    return [red, green, blue]

def is_light(rgb):
    r, g, b = rgb
    yiq = (r * 299 + g * 587 + b * 114) / 1000
    return yiq >= 128


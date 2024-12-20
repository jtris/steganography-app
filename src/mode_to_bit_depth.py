
_mode_to_bd = {
        "1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32,
        "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32
        }


def get_bit_depth(mode: str) -> int:
    return _mode_to_bd[mode]


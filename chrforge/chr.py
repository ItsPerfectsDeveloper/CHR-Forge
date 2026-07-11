import os

def decode_tile(tile_data):
    pixels = []

    for y in range(8):
        row = []

        plane0 = tile_data[y]
        plane1 = tile_data[y + 8]

        for x in range(8):
            bit0 = (plane0 >> (7 - x)) & 1
            bit1 = (plane1 >> (7 - x)) & 1

            color = bit0 | (bit1 << 1)

            row.append(color)

        pixels.append(row)

    return pixels


def load_chr_file(filename):
    with open(filename, "rb") as f:
        data = f.read()

    tiles = []

    for i in range(0, len(data), 16):
        tile = data[i:i + 16]

        if len(tile) == 16:
            tiles.append(decode_tile(tile))

    return tiles
def load_nes_file(filename):
    with open(filename, "rb") as f:
        rom = f.read()

    if rom[0:4] != b"NES\x1A":
        raise ValueError("Not a valid iNES ROM")

    prg_banks = rom[4]
    chr_banks = rom[5]

    if chr_banks == 0:
        raise ValueError("ROM uses CHR RAM")

    prg_size = prg_banks * 16384
    chr_size = chr_banks * 8192

    chr_offset = 16 + prg_size

    chr_data = rom[chr_offset:chr_offset + chr_size]

    tiles = []

    for i in range(0, len(chr_data), 16):
        tile = chr_data[i:i + 16]

        if len(tile) == 16:
            tiles.append(decode_tile(tile))

    return tiles
def encode_tile(pixels):
    tile = bytearray(16)

    for y in range(8):
        plane0 = 0
        plane1 = 0

        for x in range(8):
            color = pixels[y][x]

            plane0 |= (color & 1) << (7 - x)
            plane1 |= ((color >> 1) & 1) << (7 - x)

        tile[y] = plane0
        tile[y + 8] = plane1

    return tile

def load_tiles(filename):
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".chr":
        return load_chr_file(filename)

    if ext == ".nes":
        return load_nes_file(filename)

    raise ValueError(f"Unsupported file type: {ext}")
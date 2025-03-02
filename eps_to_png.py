import os
import struct
import zlib


def read_eps_file(eps_file):
    with open(eps_file, 'rb') as f:
        return f.read()

def convert_eps_to_png(eps_data):
    lines = eps_data.decode('latin-1').split('\n')
    width, height = 0, 0
    paths = []
    current_path = []

    for line in lines:
        if line.startswith('%%BoundingBox:'):
            parts = line.split()
            width = int(parts[3]) - int(parts[1])
            height = int(parts[4]) - int(parts[2])
        elif 'moveto' in line or 'lineto' in line:
            parts = line.split()
            x, y = int(parts[0]), int(parts[1])
            current_path.append((x, y))
        elif 'stroke' in line:
            paths.append(current_path)
            current_path = []

    png_data = bytearray()
    png_data.extend(b'\x89PNG\r\n\x1a\n')
    png_data.extend(struct.pack('>I', 13))
    png_data.extend(b'IHDR')
    png_data.extend(struct.pack('>I', width))
    png_data.extend(struct.pack('>I', height))
    png_data.extend(b'\x08\x02\x00\x00\x00')
    crc = zlib.crc32(png_data[12:])
    png_data.extend(struct.pack('>I', crc))

    idat_data = bytearray()
    for y in range(height):
        idat_data.append(0)
        for x in range(width):
            if any((x, y) in path for path in paths):
                idat_data.extend(b'\x00\x00\x00')
            else:
                idat_data.extend(b'\xff\xff\xff')

    compressed_data = zlib.compress(idat_data)
    png_data.extend(struct.pack('>I', len(compressed_data)))
    png_data.extend(b'IDAT')
    png_data.extend(compressed_data)
    crc = zlib.crc32(png_data[-(len(compressed_data) + 4):])
    png_data.extend(struct.pack('>I', crc))

    png_data.extend(struct.pack('>I', 0))
    png_data.extend(b'IEND')
    crc = zlib.crc32(b'IEND')
    png_data.extend(struct.pack('>I', crc))

    return png_data


def save_png(png_data, png_file):
    with open(png_file, 'wb') as f:
        f.write(png_data)

import os
import struct

def read_eps_file(eps_file):
    with open(eps_file, 'rb') as f:
        return f.read()

def extract_preview_bitmap(eps_data):
    header = eps_data[:30]
    if header[:4] != b'%!PS':
        raise ValueError("Not a valid EPS file")
    
    tiff_header_offset = struct.unpack('>I', header[4:8])[0]
    tiff_length = struct.unpack('>I', header[8:12])[0]
    
    if tiff_header_offset == 0 or tiff_length == 0:
        raise ValueError("No preview bitmap found")
    
    return eps_data[tiff_header_offset:tiff_header_offset + tiff_length]

def convert_eps_to_png(eps_data):
    # Placeholder for EPS to PNG conversion logic
    return b''

def save_png(png_data, png_file):
    with open(png_file, 'wb') as f:
        f.write(png_data)

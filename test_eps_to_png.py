import urllib.request
import eps_to_png

def test_eps_to_png():
    url = "https://people.sc.fsu.edu/~jburkardt/data/eps/circle.eps"
    eps_file = "circle.eps"
    png_file = "circle.png"

    # Download the EPS file
    urllib.request.urlretrieve(url, eps_file)

    # Read the EPS file
    eps_data = eps_to_png.read_eps_file(eps_file)

    # Convert the EPS data to PNG
    png_data = eps_to_png.convert_eps_to_png(eps_data)

    # Save the PNG data to a file
    eps_to_png.save_png(png_data, png_file)

    # Check if the output file is a valid PNG file
    try:
        with open(png_file, 'rb') as f:
            header = f.read(8)
            if header[:8] != b'\x89PNG\r\n\x1a\n':
                raise ValueError("Not a valid PNG file")
    except ValueError as e:
        print(f"Error: {e}")

    print(f"Converted {eps_file} to {png_file}")

if __name__ == "__main__":
    test_eps_to_png()

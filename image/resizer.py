from PIL import Image

def resize_image(input_path, output_path, new_size):
    try:
        with Image.open(input_path) as img:
            resized = img.resize(new_size)
            resized.save(output_path)
            print(f"saved resized image to {output_path}")
    except Exception as e:
        print(f"error occured: {e}")

if __name__ == "__main__":
    input_image = "input.jpeg"
    output_image = "output.jpeg"
    new_size = (800, 600)
    resize_image(input_image, output_image, new_size)
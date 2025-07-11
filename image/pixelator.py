from PIL import Image

def pixelate_image(input_path, output_path, pixel_size):
    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size

            small_width = max(1, original_width // pixel_size)
            small_height = max(1, original_height // pixel_size)

            shrunk = img.resize((small_width, small_height), resample=Image.NEAREST)
            img_pixelated = shrunk.resize((original_width, original_height), Image.NEAREST)
            img_pixelated.save(output_path)
            print(f"saved pixelated image to {output_path}")
    except Exception as e:
        print(f"error occured: {e}")

if __name__ == "__main__":
    input_image = "input.jpeg"
    output_image = "pixelated.jpeg"
    pixel_size = 10 # higher value gives more pixelation -k

    pixelate_image(input_image, output_image, pixel_size)
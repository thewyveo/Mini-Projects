from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
import numpy as np

def extract_palette(image_path, num_colors=5):
    '''
    k means: each pixel is treated as a point in 3d rgb space,
    clustered into k clusters (num_colors) where each cluster
    represents a dominant color. these are then sorted by prominence (how many pixels belong to each cluster).
    '''
    img = Image.open(image_path).convert('RGB') # convert to RGB mode
    pixels = np.array(img).reshape(-1, 3)  # flatten to list of pixels [shape:(num_pixels, 3)]

    kmeans = KMeans(n_clusters=num_colors, n_init=10)   # algorithm runs n_init times to find best solution
    kmeans.fit(pixels) # fit the kmeans model to the pixel data

    # Get RGB tuples, sorted by prominence
    counts = np.bincount(kmeans.labels_)    # count how many pixels belong to each cluster
    sorted_indices = np.argsort(-counts)    # sort by count
    colors = [tuple(map(int, kmeans.cluster_centers_[i])) for i in sorted_indices]  # convert cluster centroids to RGB tuples
                                # (cluster centroids being the average position of pixels (position being rgb value) in the rgb space)
    return colors

def show_palette(colors, swatch_size=100, save=False):
    width = swatch_size * len(colors)   # calculate total width of samples of colors (total width = swatch width * number of colors)
    height = swatch_size    # set height to swatch size for squares
    palette_img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(palette_img)
    ## a swatch is just a term used to define a sample/single color

    for i, color in enumerate(colors):
        draw.rectangle([i*swatch_size, 0, (i+1)*swatch_size, height], fill=color)

    palette_img.show()

    if save:
        palette_img.save('palette.png')
        print("color palette saved as palette.png'")

if __name__ == "__main__":
        image_path = "input.jpeg"
        num_colors = int(input("amount of colors to extract: "))
        save = input("save palette image? (y/n): ").strip().lower() == 'y'

        colors = extract_palette(image_path, num_colors=num_colors)
        for color in colors:
            print(color)

        show_palette(colors, save=save)
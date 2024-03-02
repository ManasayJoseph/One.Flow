from PIL import Image, ImageOps

def make_image_white(image_path):
    """Converts an image to pure white using grayscale and thresholding."""
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    threshold = 200  # Adjust this value as needed
    image = image.point(lambda p: p > threshold and 255)  # Set pixels above threshold to white
    return image

# Example usage:
new_image = make_image_white("./public/wand.png")
new_image.save("white_wand.png") 

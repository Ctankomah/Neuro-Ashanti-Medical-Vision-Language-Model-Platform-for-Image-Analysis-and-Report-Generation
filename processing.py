from PIL import Image
import numpy as np
from skimage.transform import resize
from skimage.exposure import rescale_intensity

class Preprocessor:
    def __init__(self, target_size=(128, 128)):
        self.target_size = target_size

    def load_image(self, file_path):
        try:
            image = Image.open(file_path)
            image = image.convert("RGB")
            return np.array(image)
        except Exception as e:
            raise ValueError(f"Error loading image: {e}")

    def preprocess_image(self, image):
        # Resizing the image
        resized_image = resize(image, self.target_size, anti_aliasing=True)
        # Normalizing image
        normalized_image = rescale_intensity(resized_image, out_range=(0, 1))

        return (normalized_image * 255).astype(np.uint8)
    
    # call this method to load and preprocess an image file
    def preprocess_file(self, file_path):
        image = self.load_image(file_path)
        preprocessed_image = self.preprocess_image(image)
        return Image.fromarray(preprocessed_image)
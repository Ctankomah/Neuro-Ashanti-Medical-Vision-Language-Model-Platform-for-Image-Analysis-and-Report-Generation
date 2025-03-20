from PIL import Image
import numpy as np
import pydicom
from skimage.transform import resize
from skimage.exposure import rescale_intensity

class Preprocessor:
    def __init__(self, target_size=(128, 128)):
        self.target_size = target_size

    def load_image(self, file_path):
        try:
            if file_path.name.lower().endswith(".dcm"):
                return self.load_dicom(file_path)
            else:
                return self.load_normal_image(file_path)
        except Exception as e:
            raise ValueError(f"Error loading image: {e}")

    # load normal images
    def load_normal_image(self, file_path):
        image = Image.open(file_path).convert("RGB")
        return np.array(image)
    
    # load dicom image
    def load_dicom(self, file_path):
        dicom_data = pydicom.dcmread(file_path)
        image_array = dicom_data.pixel_array

        # 3D images
        if image_array.ndim == 3:  
            mid_slice = image_array.shape[0] // 2 
            image_array = image_array[mid_slice]  

        # Normalize pixel values
        image_array = image_array.astype(np.float32)
        image_array = rescale_intensity(image_array, out_range=(0, 255))
        # convert to RGB
        image_array = np.stack([image_array] * 3, axis=-1)  

        return image_array.astype(np.uint8)

    def preprocess_image(self, image):
        resized_image = resize(image, self.target_size, anti_aliasing=True)
        normalized_image = rescale_intensity(resized_image, out_range=(0, 1))

        return (normalized_image * 255).astype(np.uint8)
    
    def preprocess_file(self, file_path):
        image = self.load_image(file_path)
        preprocessed_image = self.preprocess_image(image)
        return Image.fromarray(preprocessed_image)
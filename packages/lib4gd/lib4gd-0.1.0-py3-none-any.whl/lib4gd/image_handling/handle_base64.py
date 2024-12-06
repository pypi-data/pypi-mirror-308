import base64
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import cv2
import numpy as np
import asyncio
from lib4gd.resource_manager import ResourceManager

class ImageHandler:
    def __init__(self, max_workers: int = 10):
        """
        Initialize the ImageHandler class with a default number of workers for batch processing.

        :param max_workers: The maximum number of threads for batch processing. Default is 10.
        """
        # Use shared thread pool from ResourceManager
        self.thread_pool = ResourceManager.get_thread_pool(max_workers)

    def base64_to_pil(self, base64_string: str) -> Image.Image:
        """
        Convert a base64 string to a PIL Image object.

        :param base64_string: A base64-encoded string representing the image.
        :return: A PIL Image object.
        """
        try:
            decoded_data = base64.b64decode(base64_string)
            return Image.open(BytesIO(decoded_data))
        except (base64.binascii.Error, UnidentifiedImageError) as e:
            return f"Invalid base64 string or image error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def pil_to_base64(self, pil_image: Image.Image) -> str:
        """
        Convert a PIL Image object to a base64 string.

        :param pil_image: A PIL Image object.
        :return: A base64-encoded string of the image.
        """
        try:
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
        except Exception as e:
            return f"Failed to convert PIL image to base64: {str(e)}"

    def base64_to_cv2(self, base64_string: str) -> np.ndarray:
        """
        Convert a base64 string to an OpenCV image (NumPy array).

        :param base64_string: A base64-encoded string representing the image.
        :return: An OpenCV (NumPy) image.
        """
        try:
            decoded_data = base64.b64decode(base64_string)
            np_data = np.frombuffer(decoded_data, np.uint8)
            return cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        except (base64.binascii.Error, cv2.error) as e:
            return f"Invalid base64 string or OpenCV image error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def cv2_to_base64(self, cv2_image: np.ndarray) -> str:
        """
        Convert an OpenCV (NumPy) image to a base64 string.

        :param cv2_image: An OpenCV (NumPy) image.
        :return: A base64-encoded string of the image.
        """
        try:
            _, buffer = cv2.imencode('.png', cv2_image)
            return base64.b64encode(buffer).decode('utf-8')
        except Exception as e:
            return f"Failed to convert OpenCV image to base64: {str(e)}"

    async def _process_batch_async(self, inputs: list, conversion_type: str) -> list:
        """
        Internal method for processing a batch of images asynchronously.

        :param inputs: A list of images or base64 strings to process.
        :param conversion_type: The type of conversion to apply ("base64_to_cv2", "cv2_to_base64", etc.).
        :return: A list of processed results.
        """
        loop = asyncio.get_event_loop()

        # Select the appropriate worker function based on the conversion type
        conversion_func = self._select_conversion_function(conversion_type)

        tasks = [loop.run_in_executor(self.thread_pool, conversion_func, input_item) for input_item in inputs]
        results = await asyncio.gather(*tasks)
        return results

    def _select_conversion_function(self, conversion_type: str):
        """
        Select the appropriate conversion function based on the conversion type.

        :param conversion_type: The type of conversion ("base64_to_cv2", "cv2_to_base64", etc.).
        :return: The corresponding conversion function.
        :raises ValueError: If the conversion type is unsupported.
        """
        if conversion_type == "base64_to_cv2":
            return self.base64_to_cv2
        elif conversion_type == "cv2_to_base64":
            return self.cv2_to_base64
        elif conversion_type == "base64_to_pil":
            return self.base64_to_pil
        elif conversion_type == "pil_to_base64":
            return self.pil_to_base64
        else:
            raise ValueError(f"Unsupported conversion type: {conversion_type}")

    def process_batch(self, inputs: list, conversion_type: str) -> list:
        """
        Process a batch of images or base64 strings synchronously.

        :param inputs: A list of images (OpenCV/PIL) or base64 strings to process.
        :param conversion_type: The type of conversion to apply ("base64_to_cv2", "cv2_to_base64", etc.).
        :return: A list of processed results.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self._process_batch_async(inputs, conversion_type))

    def process_single(self, input_data, conversion_type: str):
        """
        Process a single image or base64 string synchronously.

        :param input_data: A single image (OpenCV/PIL) or base64 string to process.
        :param conversion_type: The type of conversion to apply ("base64_to_cv2", "cv2_to_base64", etc.).
        :return: The processed result.
        """
        conversion_func = self._select_conversion_function(conversion_type)
        return conversion_func(input_data)

from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        project_root = Path(__file__).resolve().parents[3]

        model_path = project_root /  "model" / "model.h5"
        if not model_path.exists():
            model_path = project_root / "model" / "model.h5"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at: {model_path}")

        model = load_model(str(model_path))

        img_path = Path(self.filename)
        if not img_path.is_absolute():
            img_path = project_root / img_path

        if not img_path.exists():
            raise FileNotFoundError(f"Image not found: {img_path}")

        test_image = image.load_img(str(img_path), target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0) / 255.0

        pred = model.predict(test_image, verbose=0)
        result = np.argmax(pred, axis=1)[0]
        prediction = "Tumor" if result == 1 else "Normal"

        return {"prediction": prediction}
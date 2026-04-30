import os, numpy as np

_BASE  = os.path.join(os.path.dirname(__file__), "..", "models")
_model = None   # lazy-loaded on first call

CLASS_NAMES = [
    "Pepper Bell — Bacterial Spot",     # 0
    "Pepper Bell — Healthy",            # 1
    "Potato — Early Blight",            # 2
    "Potato — Late Blight",             # 3
    "Potato — Healthy",                 # 4
    "Tomato — Bacterial Spot",          # 5
    "Tomato — Early Blight",            # 6
    "Tomato — Late Blight",             # 7
    "Tomato — Leaf Mold",               # 8
    "Tomato — Septoria Leaf Spot",      # 9
    "Tomato — Spider Mites",            # 10
    "Tomato — Target Spot",             # 11
    "Tomato — Yellow Leaf Curl Virus",  # 12
    "Tomato — Mosaic Virus",            # 13
    "Tomato — Healthy",                 # 14
]

def _load():
    global _model
    if _model is None:
        import tensorflow as tf
        _model = tf.keras.models.load_model(
            os.path.join(_BASE, "leaf_disease_model.h5")
        )
    return _model

def predict_disease(img_path: str):
    """
    Returns (disease_name: str, confidence: float 0-1)
    """
    from tensorflow.keras.preprocessing import image as kimage
    model  = _load()
    img    = kimage.load_img(img_path, target_size=(128, 128))
    arr    = kimage.img_to_array(img) / 255.0
    arr    = np.expand_dims(arr, axis=0)
    preds  = model.predict(arr, verbose=0)[0]
    idx    = int(np.argmax(preds))
    return CLASS_NAMES[idx], float(preds[idx])

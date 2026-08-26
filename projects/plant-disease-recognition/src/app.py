"""Streamlit demo for a trained plant-disease classifier."""

from pathlib import Path
import json

import numpy as np
import streamlit as st
import tensorflow as tf

MODEL = Path("models/plant_disease_mobilenetv2.keras")
LABELS = Path("models/plant_disease_labels.json")

st.set_page_config(page_title="Plant Disease Recognition", page_icon="🌱", layout="centered")
st.title("🌱 Plant Disease Recognition")
st.caption("Upload a leaf image to run inference with a locally trained model.")

if not MODEL.exists() or not LABELS.exists():
    st.warning("Model artifacts are not present yet. Run the transfer-learning workflow first.")
    st.code("python src/train_transfer.py --data-dir data/plantvillage --output-dir models")
    st.stop()


@st.cache_resource
def load_artifacts():
    return tf.keras.models.load_model(MODEL), json.loads(LABELS.read_text(encoding="utf-8"))


model, labels = load_artifacts()
upload = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])

if upload:
    shape = model.input_shape
    image_size = (int(shape[1]), int(shape[2]))
    image = tf.keras.utils.load_img(upload, target_size=image_size)
    st.image(image, caption="Input image", use_container_width=True)

    array = tf.keras.utils.img_to_array(image)
    array = tf.keras.applications.mobilenet_v2.preprocess_input(array)
    probabilities = model.predict(np.expand_dims(array, 0), verbose=0)[0]
    top = np.argsort(probabilities)[::-1][:3]

    st.subheader("Prediction")
    st.success(labels[int(top[0])])
    st.metric("Confidence", f"{probabilities[int(top[0])] * 100:.2f}%")

    st.subheader("Top predictions")
    for index in top:
        st.write(f"**{labels[int(index)]}** — {probabilities[int(index)] * 100:.2f}%")

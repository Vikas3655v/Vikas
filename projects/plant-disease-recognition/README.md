# 🌱 Plant Disease Recognition using Deep Learning

A reproducible image-classification project for recognizing plant diseases from leaf images using TensorFlow and transfer learning.

## ✨ What it demonstrates

- PlantVillage-style directory dataset workflow
- MobileNetV2 transfer learning
- Training/validation split and augmentation
- Early stopping and best-model checkpointing
- Saved model and class-label artifacts
- Precision, recall, F1-score and confusion-matrix evaluation
- Command-line prediction
- Interactive Streamlit inference

## 🏗️ Pipeline

```text
Dataset
  ↓
Preprocessing + Augmentation
  ↓
MobileNetV2 Transfer Learning
  ↓
Validation + Best Checkpoint
  ↓
Evaluation
  ↓
Saved Model + Labels
  ↓
CLI / Streamlit Inference
```

## 📁 Structure

```text
plant-disease-recognition/
├── data/                       # Local dataset; not committed
├── models/                     # Generated model artifacts; ignored
├── src/
│   ├── train_transfer.py       # Recommended training workflow
│   ├── train.py                # Small CNN baseline
│   ├── evaluate.py             # Metrics + confusion matrix
│   ├── predict.py              # CLI inference
│   └── app.py                  # Streamlit demo
├── colab_train.py              # Colab guidance
├── requirements.txt
└── README.md
```

## ⚙️ Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## 📦 Dataset

Download a permitted PlantVillage dataset and place the class folders under `data/plantvillage/`. Do not commit the dataset or credentials.

## 🧠 Recommended Training

```bash
python src/train_transfer.py --data-dir data/plantvillage --output-dir models --epochs 8
```

This produces:

- `models/plant_disease_mobilenetv2.keras`
- `models/plant_disease_labels.json`
- `models/training_metrics.json`

## 📊 Evaluate

```bash
python src/evaluate.py --data-dir data/plantvillage --model models/plant_disease_mobilenetv2.keras
```

No accuracy or performance number is claimed until the model is actually trained and evaluated.

## 🔬 CLI Inference

```bash
python src/predict.py --model models/plant_disease_mobilenetv2.keras --image path/to/leaf.jpg
```

## 🌐 Streamlit Demo

```bash
streamlit run src/app.py
```

Upload a leaf image to see the predicted class, confidence and top predictions.

## ⚠️ Limitations

Results depend on dataset quality, class balance, image conditions and training configuration. A model trained on controlled images may not generalize to field conditions. This is an educational/research project and not a substitute for professional agricultural diagnosis.

## 🚀 Future Improvements

- Fine-tune the MobileNetV2 backbone
- Add a fully held-out test set
- Add Grad-CAM explanations
- Track experiments and datasets
- Validate the model on field images
- Deploy only after appropriate model validation

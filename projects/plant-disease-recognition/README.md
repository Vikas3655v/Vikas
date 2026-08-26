# 🌱 Plant Disease Recognition using Deep Learning

A recruiter-friendly, reproducible image-classification project for recognizing plant diseases from leaf images.

## 🔎 What the project demonstrates

- PlantVillage-style directory dataset workflow
- MobileNetV2 transfer learning
- Training/validation split and augmentation
- Early stopping and best-model checkpointing
- Accuracy/loss tracking
- Precision, recall, F1-score and confusion matrix evaluation
- Saved model/class-label artifacts
- Interactive Streamlit inference application

## 🏗️ Pipeline

```text
Dataset → preprocessing → augmentation → MobileNetV2 → validation
→ best checkpoint → evaluation → saved model → Streamlit inference
```

## 📁 Structure

```text
plant-disease-recognition/
├── data/                 # Dataset downloaded locally; not committed
├── models/               # Generated model artifacts; ignored by Git
├── src/
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── app.py
├── requirements.txt
└── README.md
```

## 📦 Dataset

Download the public **PlantVillage** dataset from Kaggle or its original source. Put the class folders under `data/plantvillage/`. Do not commit the dataset or credentials.

## ⚙️ Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## 🧠 Train

```bash
python src/train.py --data-dir data/plantvillage --output models/plant_disease_mobilenetv2.keras
```

## 📊 Evaluate

```bash
python src/evaluate.py --data-dir data/plantvillage --model models/plant_disease_mobilenetv2.keras
```

The evaluation script produces precision, recall, F1-score and a confusion matrix. **No accuracy or performance number is claimed until the model is actually run.**

## 🔬 Inference

```bash
python src/predict.py --model models/plant_disease_mobilenetv2.keras --image path/to/leaf.jpg
```

## 🌐 Interactive Demo

After training:

```bash
streamlit run src/app.py
```

Upload a leaf image to see the predicted class, confidence and top-3 predictions.

## ⚠️ Limitations

Results depend on dataset quality, class balance, image conditions and training configuration. A model trained on controlled images may not generalize to field conditions. This is an educational/research project, not a substitute for professional agricultural diagnosis.

## 🚀 Future Improvements

- Fine-tune the MobileNetV2 backbone
- Add a held-out test set
- Add Grad-CAM explanations
- Track experiments
- Deploy a validated model

## License

Add the license required by the selected dataset/source before redistribution.

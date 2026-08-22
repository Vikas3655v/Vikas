# 🌱 Plant Disease Recognition using Deep Learning

An image-classification pipeline for experimenting with plant disease recognition from leaf images.

## Workflow

1. Prepare a directory-based image dataset.
2. Create training/validation splits with TensorFlow utilities.
3. Resize and normalize images.
4. Train a compact CNN baseline.
5. Evaluate validation performance.
6. Save the trained model locally and use the prediction script for inference.

## Dataset

Do **not** commit the dataset or trained weights. Place a compatible image dataset locally under `data/` using one directory per class, or adapt the loader to your dataset layout.

Example:

```text
data/plantvillage/
├── class_a/
├── class_b/
└── class_c/
```

## Requirements

```bash
pip install -r requirements.txt
```

## Train

```bash
python src/train.py --data-dir data/plantvillage --output models/plant_disease.keras
```

## Predict

```bash
python src/predict.py --model models/plant_disease.keras --image path/to/leaf.jpg
```

## Evaluation

The training script reports validation accuracy and loss. Add precision, recall, F1-score and a confusion matrix when running a complete experiment. No performance number is claimed by this repository until the model is actually trained and evaluated.

## Limitations

A model trained on a controlled dataset may not generalize to field conditions, lighting changes, different cameras, or unseen diseases. This project is for learning and experimentation and should not be treated as an agricultural diagnosis system without further validation.

"""Colab-friendly entry point.

Run after downloading/extracting PlantVillage into /content/plantvillage.
"""
from pathlib import Path
from src.train_transfer import main

# In Colab, call the training script directly, e.g.:
# python src/train_transfer.py --data-dir /content/plantvillage --epochs 8

if __name__ == "__main__":
    print("Run: python src/train_transfer.py --data-dir /content/plantvillage --epochs 8")
    print("Then run: python src/evaluate.py --data-dir /content/plantvillage --model models/plant_disease_mobilenetv2.keras")

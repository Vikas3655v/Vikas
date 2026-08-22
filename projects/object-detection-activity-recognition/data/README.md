# Dataset setup

Use a labelled object-detection dataset compatible with Ultralytics YOLO. Do not commit large image archives or trained weights.

Create a YAML file such as `retail.yaml` pointing to the local train/validation image and label directories, then run:

```bash
python train.py --data data/retail.yaml --epochs 30
```

For the retail portfolio version, SKU-110K is a suitable research dataset for dense shelf-product detection. Download it from its public dataset source and follow its license/terms.

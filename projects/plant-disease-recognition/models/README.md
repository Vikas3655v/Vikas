# Model Artifacts

Generated model weights are intentionally not committed to Git. Run the training workflow locally or in a GPU runtime to create the artifacts.

Expected artifacts:

- `plant_disease_mobilenetv2.keras`
- `plant_disease_labels.json`
- `training_metrics.json`

Only measured metrics should be added to the project README after training completes. The repository includes an interactive Streamlit app that automatically uses these files when present.

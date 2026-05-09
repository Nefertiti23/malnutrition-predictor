**Data folders (data/)**<br>
`raw/` — original, untouched data files<br>
`processed/` — cleaned/transformed data ready for training<br>
`external/` — third-party or supplementary datasets<br>

**Source code (src/)**<br>
`data/make_dataset.py` — scripts to download or generate datasets<br>
`features/build_features.py` — feature engineering (transformations, encodings, etc.)<br>
`models/train_model.py` — training logic<br>
`models/predict_model.py` — inference/prediction logic<br>
`utils/helpers.py` — shared utility functions used across the above<br>

**Other folders**<br>
`notebooks/` — Jupyter notebooks for exploration and experimentation (not production code)<br>
`models/` — serialized trained model files (.pkl, .joblib) saved after training<br>
`configs/` — hyperparameters and settings in YAML so you're not hardcoding them<br>
`tests/` — unit tests for data pipelines and model behavior<br>

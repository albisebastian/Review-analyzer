# Drop your Keras model here

Copy these files into this folder:

| File | Required | Notes |
|------|----------|-------|
| `customer_review_analyzer.keras` | yes | Any `*.keras` file works; this exact name is preferred, then `sentiment_model.keras`, then the first `*.keras` found. |
| `sentiment_classes.json` | no | Class order of the model's output, e.g. `["negative","neutral","positive"]`. Defaults to that order, which is what the training notebook produces. |

Then restart the app, or open the **engine** pill (top right of the web page) and click **Reload model**.

The model must accept a raw review string and return class probabilities, i.e. the
`TextVectorization` layer is saved inside the model, as in `training/train_model.py`
and the Colab notebook. TensorFlow must be installed (`pip install -r requirements-keras.txt`).

`*.keras` files are ignored by git (see `.gitignore`) because they are large.

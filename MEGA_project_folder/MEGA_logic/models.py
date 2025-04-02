import tensorflow as tf
#from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import regularizers, models, layers, Sequential
#from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from scikeras.wrappers import KerasRegressor
from sklearn.decomposition import PCA
from sklearn.compose import TransformedTargetRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from MEGA_project_folder.MEGA_logic.data import df_de_merged
from preproc import *
import joblib

"""
- initializes a deep neural network.
"""

# initialize model
def initialize_model(input_shape: tuple):
    reg = regularizers.l1_l2(l1=0.005)
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Dense(100, activation="relu", kernel_regularizer=reg))
    model.add(layers.BatchNormalization(momentum=0.9))
    model.add(layers.Dense(50, activation="relu"))
    model.add(layers.BatchNormalization(momentum=0.9))
    model.add(layers.Dropout(rate=0.3))
    model.add(layers.Dense(1, activation="linear"))
    print("✅ model initialized")
    return model

input_shape = (X_train_processed.shape[1],)
model = initialize_model(input_shape)
model.summary()

# compile model
learning_rate = 0.0005
batch_size = 256
optimizer = Adam(learning_rate=learning_rate)
model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["mae"])

# early stopping callback
es = EarlyStopping(
    monitor="val_loss",
    patience=2,
    restore_best_weights=True,
    verbose=1
)

# train on scaled targets
history = model.fit(
    X_train_processed,
    y_train_scaled,
    validation_data=(X_val_processed, y_val_scaled),
    epochs=100,
    batch_size=batch_size,
    callbacks=[es],
    verbose=1
)
model_and_pipeline = {
    'features_pipeline': features_pipeline,
    'target_scaler': target_scaler
}
# export the model
#model.save('/root/code/senetan/MEGA_project/models/MEGA_model.h5')

#joblib.dump(features_pipeline, '/root/code/senetan/MEGA_project/models/features_pipeline.pkl')
#joblib.dump(target_scaler, '/root/code/senetan/MEGA_project/models/target_scaler.pkl')

# evaluate in scaled units
val_metrics_scaled = model.evaluate(X_val_processed, y_val_scaled, verbose=0)
test_metrics_scaled = model.evaluate(X_test_processed, y_test_scaled, verbose=0)
print("mae val (scaled):", round(val_metrics_scaled[1], 2))
print("mae test (scaled):", round(test_metrics_scaled[1], 2))

# predict on test set (reverse scaled to find back the right, unscaled units)
y_pred_scaled = model.predict(X_test_processed)
# inverse transform predictions and test targets to original gco2eq/kwh units
y_pred = target_scaler.inverse_transform(y_pred_scaled)
y_test_original = target_scaler.inverse_transform(y_test_scaled)

mse = mean_squared_error(y_test_original, y_pred)
mae = mean_absolute_error(y_test_original, y_pred)
print("mae test (gco2eq/kwh):", round(mae, 2))
print("mse test (gco2eq/kwh):", round(mse, 2))

# compute the average carbon intensity over the period
mean_carbon = df_de_merged['carbonIntensity'].mean()
print("mean carbon intensity (gco2eq/kwh):", round(mean_carbon, 2))

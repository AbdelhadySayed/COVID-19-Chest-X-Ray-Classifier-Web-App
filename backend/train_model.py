import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import os

# Paths to dataset
DATASET_PATH = 'COVID19-DATASET/'
TRAIN_DIR = os.path.join(DATASET_PATH, 'train')
VALID_DIR = os.path.join(DATASET_PATH, 'valid')
TEST_DIR = os.path.join(DATASET_PATH, 'test')

# Hyperparameters
BATCH_SIZE = 32
IMAGE_SIZE = (224, 224)
EPOCHS = 10

# 1. Data Augmentation and Preprocessing
train_datagen = ImageDataGenerator(rescale=1.0/255, 
                                   rotation_range=20,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

valid_datagen = ImageDataGenerator(rescale=1.0/255)
test_datagen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_datagen.flow_from_directory(TRAIN_DIR, 
                                                    target_size=IMAGE_SIZE, 
                                                    batch_size=BATCH_SIZE, 
                                                    class_mode='binary')

valid_generator = valid_datagen.flow_from_directory(VALID_DIR, 
                                                    target_size=IMAGE_SIZE, 
                                                    batch_size=BATCH_SIZE, 
                                                    class_mode='binary')

test_generator = test_datagen.flow_from_directory(TEST_DIR, 
                                                  target_size=IMAGE_SIZE, 
                                                  batch_size=BATCH_SIZE, 
                                                  class_mode='binary')

# 2. Load Pre-trained ResNet50 (Replacing ResNet18 with ResNet50 from Keras)
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the base model
for layer in base_model.layers:
    layer.trainable = False

# Add custom layers on top
x = base_model.output
x = Flatten()(x)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
output = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=output)

# 3. Compile the Model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 4. Train the Model
history = model.fit(train_generator,
                    validation_data=valid_generator,
                    epochs=EPOCHS)

# 5. Save the Fine-tuned Model
model.save('model/resnet50_finetuned.h5')

# 6. Evaluate the Model
loss, accuracy = model.evaluate(test_generator)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# 7. Plot Training History
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy')
plt.savefig('evaluation_results.png')
plt.show()

import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras.optimizers
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import pickle

print(tf.__version__)

TRAIN_FILE_PATH = '/MyDrive/train/'
TEST_FILE_PATH = '/MyDrive/test/'
VALIDATION_FILE_PATH = '/MyDrive/validation/'

def test_working_image() -> None:
    img = image.load_img( TEST_FILE_PATH +'Screenshot 2022-08-20 at 08.57.39.png')
    plt.imshow(img)

def test_file_paths() -> None:
    for filename in os.listdir(TEST_FILE_PATH):
        full_path = os.path.join(TEST_FILE_PATH, filename)
        if 'DS_Store' in filename or '.ipynb' in filename:
            print('DS_Store / .ipnyb file is not supposed to be here, skipping')
        else:
            print(filename)
            print(full_path)
            print(cv2.imread(full_path).shape)

class Pipeline:
    def __init__(self) -> None:
        pass

    def split_datasets(self): 
        train = ImageDataGenerator(rescale=1/255)
        validation = ImageDataGenerator(rescale=1/255)

        train_dataset = train.flow_from_directory(TRAIN_FILE_PATH,
                                            target_size = (500,500),
                                            class_mode = 'binary',
                                            batch_size = 3)
        validation_dataset = validation.flow_from_directory(VALIDATION_FILE_PATH,
                                            target_size = (500,500),
                                            class_mode = 'binary',
                                            batch_size = 3)   
        print(train_dataset.class_indices)
        print(validation_dataset.class_indices)
        return train_dataset, validation_dataset

    def generate_model(self, train_dataset, validation_dataset) -> None:
        model = tf.keras.models.Sequential()
        # Increased number of strides to get lower-resolution understanding
        model.add(tf.keras.layers.Conv2D(filters = 32, kernel_size = (5,5), strides = (2,2), padding = 'valid', input_shape = (500,500, 3))) 
        model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
        # Further Increase the learners 
        model.add(tf.keras.layers.Conv2D(filters = 64, kernel_size = (5,5), strides = (1,1), padding = 'valid'))
        model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
        # Expand learners
        model.add(tf.keras.layers.Conv2D(filters = 128, kernel_size = (3,3), strides = (1,1), padding = 'valid'))
        model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
        # Flattern to allow for multi dimensional input -> single dimension 
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(1, activation = 'sigmoid'))
        model.summary()
        model.compile(tf.keras.optimizers.Adam(learning_rate=1e-3), loss=tf.keras.losses.BinaryCrossentropy(), metrics=[tf.keras.metrics.BinaryAccuracy()])
        model_fit = model.fit(train_dataset, epochs = 25, validation_data = validation_dataset, steps_per_epoch=3)
        pickle.dump(model_fit, open('livingOrDeadTreesModel.sav', 'wb'))
    
    def predict_output(self, file_name = 'Screenshot 2022-08-20 at 15.54.09.png') -> None:
        model = pickle.load(open('livingOrDeadTreesModel.sav', 'rb'))
        img = image.load_img(TEST_FILE_PATH + file_name)
        image_array = image.img_to_array(img)
        expanded_image_array = np.expand_dims(image_array, axis = 0)
        images = np.vstack([expanded_image_array])
        resized_image = tf.image.resize(
            images,
            size = (500,500))
        prediction = model.predict(resized_image)
        print(prediction)
        if prediction == [[1.]]:
            print('Dead forrest')
        else:
            print('Alive forrest')

    def run_model_generation(self):
        train_dataset, validation_dataset = self.split_datasets()
        self.generate_model(train_dataset, validation_dataset)

if __name__ == '__main__':
    Pipeline.run_model_generation()
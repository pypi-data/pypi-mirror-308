def program(num):
    if num == 1:
        print("""#EXP 1 : IMAGE CLASSIFICATION

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
test_datagen = ImageDataGenerator(rescale=1./255)
x_train = train_datagen.flow_from_directory(
    r"/content/trainset",
    target_size=(64, 64),
    batch_size=32,
    class_mode="categorical"
)
x_test = test_datagen.flow_from_directory(
    r"/content/testset",
    target_size=(64, 64),
    batch_size=32,
    class_mode="categorical"
)

from google.colab import drive
drive.mount('/content/drive')
print(x_train.class_indices)

model=Sequential ()
model .add(Convolution2D(32, (3,3),input_shape=(64,64,3),activation="relu") )
model. add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten() )
model.add(Dense(units=128, activation="relu"))
model.add(Dense(units=5, activation="softmax" ) )

model.summary( )

model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
model. fit(x_train,steps_per_epoch=47, epochs=1, validation_data=x_test,validation_steps=20)
model.save("animal.h5")

from tensorflow.keras.models import load_model
from keras.preprocessing import image
import numpy as np
model=load_model("animal.h5")
img=image.load_img(r"/content/trainset/racoons/F1 (103).jpg",target_size=(64,64))
img

x=image.img_to_array(img)
x

x.shape

x=np.expand_dims(x,axis=0)
x.shape

y=model.predict(x)
pred=np.argmax(y, axis=1)

y

pred

x_train.class_indices

index=['bears', 'crows', 'elephants', 'racoons', 'rats']
result=str(index[pred[0]])
result""")

    elif num==2:
        print("""#EXP 2 MODEL PERFORMANCE
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16, ResNet50, DenseNet121
import numpy as np

input_shape = (224, 224, 3)

def create_alexnet():
    model = Sequential()

    model.add(Conv2D(96, (11, 11), strides=(4, 4), input_shape=input_shape, padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Conv2D(256, (5, 5), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Conv2D(384, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(384, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    return model




def create_densenet121():
    base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=input_shape)
    x = base_model.output
    x = Flatten()(x)
    x = Dense(4096, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(2, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)


    for layer in base_model.layers:
        layer.trainable = False

    return model


train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
test_datagen = ImageDataGenerator(rescale=1./255)


x_train = train_datagen.flow_from_directory(
    "/content/drive/MyDrive/CV exp1 dataset/Quality Dataset/train",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical"
)


x_test = test_datagen.flow_from_directory(
    "/content/drive/MyDrive/CV exp1 dataset/Quality Dataset/test",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical"
)




x_train_samples = next(x_train)
x_test_samples = next(x_test)

print("Training batch shape:", x_train_samples[0].shape)
print("Testing batch shape:", x_test_samples[0].shape)


print("Training AlexNet...")
alexnet_model = create_alexnet()
alexnet_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

try:
    alexnet_model.fit(
        x_train,
        steps_per_epoch=len(x_train),
        epochs=5,
        validation_data=x_test,
        validation_steps=len(x_test)
    )
except AttributeError as e:
    print(f"Error during training AlexNet: {e}")

    print("Training AlexNet without validation data...")
    alexnet_model.fit(
        x_train,
        steps_per_epoch=len(x_train),
        epochs=5
    )

alexnet_model.save("AlexNet.h5")



x_train_samples = next(x_train)
x_test_samples = next(x_test)

print("Training batch shape:", x_train_samples[0].shape)
print("Testing batch shape:", x_test_samples[0].shape)


print("Training DenseNet121...")
densenet121_model = create_densenet121()
densenet121_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

try:
    densenet121_model.fit(
        x_train,
        steps_per_epoch=len(x_train),
        epochs=5,
        validation_data=x_test,
        validation_steps=len(x_test)
    )
except AttributeError as e:
    print(f"Error during training DenseNet121: {e}")

    print(f"Training DenseNet121 without validation data...")
    densenet121_model.fit(
        x_train,
        steps_per_epoch=len(x_train),
        epochs=5
    )

densenet121_model.save("DenseNet121.h5")


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model_name = "DenseNet121"
model = load_model(f"{model_name}.h5")

img_path = r"/content/drive/MyDrive/CV exp1 dataset/Quality Dataset/valid/rotten/images-1-_jpeg.rf.9dfbf252510d9175da106c563bd4e1f9.jpg"
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x /= 255.
y = model.predict(x)
pred = np.argmax(y, axis=1)
index = ['fresh', 'rotten']
result = index[pred[0]]
print("Prediction:", result)

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

model_name = "AlexNet"
model = load_model(f"{model_name}.h5")


img_path = r"/content/drive/MyDrive/CV exp1 dataset/Quality Dataset/valid/rotten/images-1-_jpeg.rf.9dfbf252510d9175da106c563bd4e1f9.jpg"
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x /= 255.


y = model.predict(x)
pred = np.argmax(y, axis=1)
index = ['fresh', 'rotten']
result = index[pred[0]]
print("Prediction:", result)""")

    elif num == 3:
        print("""#EXP 3 : YOLO
!pip install -q kaggle

from g
ogle.colab import userdata
import os
os.environ["KAGGLE_KEY"] = userdata.get('KAGGLE_KEY')
os.environ["KAGGLE_USERNAME"] = userdata.get('KAGGLE_USERNAME')

!kaggle datasets download -d therealpattasubalu/vehicle-dataset

!git clone http://github.com/WongKinYiu/yolov9.git

%cd yolov9

!wget https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c-converted.pt

!mkdir ./data/datasets

!unzip /content/vehicle-dataset.zip -d ./data/datasets

! python train_dual.py --data ./data/datasets/custom_dataset.yaml --weights yolov9-c-converted.pt --device "CPU" --cfg models/detect/yolov9-c.yaml

!python detect.py --source '/content/yolov9/figure/horses_prediction.jpg' --img 640 --device "cpu" --weights './yolov9-c-converted.pt' --name yolo""")

    elif num == 4:
        print("""#EXP 4 : IMAGE CAPTIONING
!pip install -q transformers
!pip install -q pillow
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

image_url = '/content/cv.jpg'  # Local file path
image = Image.open(image_url)  # Open the image directly
image.show()

inputs = processor(image, return_tensors="pt")

outputs = model.generate(**inputs)

caption = processor.decode(outputs[0], skip_special_tokens=True)  # Capitalize 'True'
print("Generated Caption:", caption)""")

    elif num == 5:
        print("""#EXP 5 : IMAGE TO IMAGE TRANSLATION USING GAN
!kaggle datasets download -d alincijov/pix2pix-maps
!unzip /content/pix2pix-maps.zip
import tensorflow as tf
import os
import time
from matplotlib import pyplot as plt
from IPython import display
BUFFER_SIZE=400
BATCH_SIZE=1
IMG_WIDTH=256
IMG_HEIGHT=256
OUTPUT_CHANNELS=3
LAMBDA=100

def load(image_file):
  image = tf.io.read_file(image_file)
  image = tf.image.decode_jpeg(image)
  w = tf.shape(image)[1]
  w = w // 2
  real_image = image[:, :w, :]
  input_image = image[:, w:, :]
  input_image = tf.cast(input_image, tf.float32)
  real_image = tf.cast(real_image, tf.float32)
  return input_image, real_image

def resize(input_image, real_image, height, width):
  input_image = tf.image.resize(input_image, [height, width],method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
  real_image = tf.image.resize(real_image, [height, width],method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
  return input_image, real_image

def random_crop(input_image, real_image):
  stacked_image = tf.stack([input_image, real_image], axis=0)
  cropped_image = tf.image.random_crop(stacked_image, size=[2, IMG_HEIGHT, IMG_WIDTH, 3])
  return cropped_image[0], cropped_image[1]

def normalize(input_image, real_image):
  input_image = (input_image / 127.5) - 1
  real_image = (real_image / 127.5) - 1
  return input_image, real_image


@tf.function()
def random_jitter(input_image, real_image):
  input_image, real_image = resize(input_image, real_image, 286, 286)
  input_image, real_image = random_crop(input_image, real_image)
  if tf.random.uniform(()) > 0.5:
    input_image = tf.image.flip_left_right(input_image)
    real_image = tf.image.flip_left_right(real_image)
  return input_image, real_image

def load_image_train(image_file):
  input_image, real_image = load(image_file)
  input_image, real_image = random_jitter(input_image, real_image)
  input_image, real_image = normalize(input_image, real_image)
  return input_image, real_image


def load_image_test(image_file):
  input_image, real_image = load(image_file)
  input_image, real_image = resize(input_image, real_image,
                                   IMG_HEIGHT, IMG_WIDTH)
  input_image, real_image = normalize(input_image, real_image)
  return input_image, real_image


import tensorflow as tf
# Define the path to your training images
train_path = r'C:\\Users\jeevi\OneDrive\Pictures\\'  # Define train_path if you want to use it for multiple files
# Parameters
BUFFER_SIZE = 1000  # Adjust as needed
BATCH_SIZE = 32     # Adjust as needed
# If you want to load a specific image file
image_path = 'inflating: train/894.jpg'
train_dataset = tf.data.Dataset.from_tensor_slices([image_path])
# Continue with mapping and batching
train_dataset = train_dataset.map(load_image_train, num_parallel_calls=tf.data.experimental.AUTOTUNE)
train_dataset = train_dataset.shuffle(BUFFER_SIZE)
train_dataset = train_dataset.batch(BATCH_SIZE)


import tensorflow as tf
# Define the path to your validation images
val_path = r'C:\\Users\jeevi\OneDrive\Pictures\\'  # Adjust this as needed
# Parameters
BATCH_SIZE = 32  # Adjust as needed
# Load test dataset from a specific image
image_path = 'inflating: val/1036.jpg'
test_dataset = tf.data.Dataset.from_tensor_slices([image_path])
# Continue with mapping and batching
test_dataset = test_dataset.map(load_image_test)
test_dataset = test_dataset.batch(BATCH_SIZE)


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, BatchNormalization, LeakyReLU , Dropout , ReLU ,Conv2DTranspose

def downsample(filters, kernal_size, batch_norm=True):
    layer = Sequential()
    layer.add(Conv2D(filters, kernel_size=kernal_size, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    if batch_norm:
        layer.add(BatchNormalization())
    layer.add(LeakyReLU())
    return layer

def upsample(filters, kernal_size, dropout=False):
    layer=Sequential()
    layer.add(Conv2DTranspose(filters, kernel_size=kernal_size, strides=2, padding='same', kernel_initializer='he_normal', use_bias=False))
    layer.add(BatchNormalization())
    if dropout:
        layer.add(Dropout(0.4))
    layer.add(ReLU())
    return layer


def Generator():
  inputs = tf.keras.layers.Input(shape=[256,256,3])
  down_stack = [
    downsample(64, 4, batch_norm=False), # (bs, 128, 128, 64)
    downsample(128, 4), # (bs, 64, 64, 128)
    downsample(256, 4), # (bs, 32, 32, 256)
    downsample(512, 4), # (bs, 16, 16, 512)
    downsample(512, 4), # (bs, 8, 8, 512)
    downsample(512, 4), # (bs, 4, 4, 512)
    downsample(512, 4), # (bs, 2, 2, 512)
    downsample(512, 4), # (bs, 1, 1, 512)
  ]
  up_stack = [
    upsample(512, 4, dropout=True), # (bs, 2, 2, 1024)
    upsample(512, 4, dropout=True), # (bs, 4, 4, 1024)
    upsample(512, 4, dropout=True), # (bs, 8, 8, 1024)
    upsample(512, 4), # (bs, 16, 16, 1024)
    upsample(256, 4), # (bs, 32, 32, 512)
    upsample(128, 4), # (bs, 64, 64, 256)
    upsample(64, 4), # (bs, 128, 128, 128)
  ]
  initializer = tf.random_normal_initializer(0., 0.02)

  last = tf.keras.layers.Conv2DTranspose(OUTPUT_CHANNELS, 4,
                                         strides=2,
                                         padding='same',
                                         kernel_initializer=initializer,
                                         activation='tanh')

  x = inputs
  skips = []
  for down in down_stack:
    x = down(x)
    skips.append(x)
  skips = reversed(skips[:-1])
  for up, skip in zip(up_stack, skips):
    x = up(x)
    x = tf.keras.layers.Concatenate()([x, skip])
  x = last(x)
  return tf.keras.Model(inputs=inputs, outputs=x)


generator = Generator()
tf.keras.utils.plot_model(generator, show_shapes=True, dpi=64)
def generator_loss(disc_generated_output, gen_output, target):
  gan_loss = loss_object(tf.ones_like(disc_generated_output), disc_generated_output)
  # mean absolute error
  l1_loss = tf.reduce_mean(tf.abs(target - gen_output))
  total_gen_loss = gan_loss + (LAMBDA * l1_loss)
  return total_gen_loss, gan_loss, l1_loss


def Discriminator():
  initializer = tf.random_normal_initializer(0., 0.02)
  inp = tf.keras.layers.Input(shape=[256, 256, 3], name='input_image')
  tar = tf.keras.layers.Input(shape=[256, 256, 3], name='target_image')
  x = tf.keras.layers.concatenate([inp, tar]) # (bs, 256, 256, channels*2)
  down1 = downsample(64, 4, False)(x) # (bs, 128, 128, 64)
  down2 = downsample(128, 4)(down1) # (bs, 64, 64, 128)
  down3 = downsample(256, 4)(down2) # (bs, 32, 32, 256)
  zero_pad1 = tf.keras.layers.ZeroPadding2D()(down3) # (bs, 34, 34, 256)
  conv = tf.keras.layers.Conv2D(512, 4, strides=1,
                                kernel_initializer=initializer,
                                use_bias=False)(zero_pad1) # (bs, 31, 31, 512)

  batchnorm1 = tf.keras.layers.BatchNormalization()(conv)
  leaky_relu = tf.keras.layers.LeakyReLU()(batchnorm1)
  zero_pad2 = tf.keras.layers.ZeroPadding2D()(leaky_relu) # (bs, 33, 33, 512)
  last = tf.keras.layers.Conv2D(1, 4, strides=1,
                                kernel_initializer=initializer)(zero_pad2) # (bs, 30, 30, 1)
  return tf.keras.Model(inputs=[inp, tar], outputs=last)


discriminator = Discriminator()
tf.keras.utils.plot_model(discriminator, show_shapes=True, dpi=64)


def discriminator_loss(disc_real_output, disc_generated_output):
  real_loss = loss_object(tf.ones_like(disc_real_output), disc_real_output)
  generated_loss = loss_object(tf.zeros_like(disc_generated_output), disc_generated_output)
  total_disc_loss = real_loss + generated_loss
  return total_disc_loss

generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)


def generate_images(model, test_input, tar):
  prediction = model(test_input, training=True)
  plt.figure(figsize=(15,15))
  display_list = [test_input[0], tar[0], prediction[0]]
  title = ['Input Image', 'Ground Truth', 'Predicted Image']
  for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.title(title[i])
    # getting the pixel values between [0, 1] to plot it.
    plt.imshow(display_list[i] * 0.5 + 0.5)
    plt.axis('off')
  plt.show()


def train_step(input_image, target, epoch):
  with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
    gen_output = generator(input_image, training=True)
    disc_real_output = discriminator([input_image, target], training=True)
    disc_generated_output = discriminator([input_image, gen_output], training=True)
    gen_total_loss, gen_gan_loss, gen_l1_loss = generator_loss(disc_generated_output, gen_output, target)
    disc_loss = discriminator_loss(disc_real_output, disc_generated_output)
  generator_gradients = gen_tape.gradient(gen_total_loss,
                                          generator.trainable_variables)
  discriminator_gradients = disc_tape.gradient(disc_loss,
                                               discriminator.trainable_variables)
  generator_optimizer.apply_gradients(zip(generator_gradients,
                                          generator.trainable_variables))
  discriminator_optimizer.apply_gradients(zip(discriminator_gradients,
                                              discriminator.trainable_variables))


""")

    elif num == 6:
        print("""#EXP 6 : VIDEO CLASSIFICATION

from tensorflow import keras
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import imageio
import cv2
import os

IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 10

MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

print(f"Total videos for training: {len(train_df)}")
print(f"Total videos for testing: {len(test_df)}")

train_df.sample(10)

def crop_center_square(frame):
    y, x = frame.shape[0:2]

    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y : start_y + min_dim, start_x : start_x + min_dim]

def load_video(path, max_frames=0, resize=(IMG_SIZE, IMG_SIZE)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frames.append(frame)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)

def build_feature_extractor():
    feature_extractor = keras.applications.InceptionV3(weights="imagenet",
                                                       include_top=False, pooling="avg",
                                                       input_shape=(IMG_SIZE, IMG_SIZE, 3))

    preprocess_input = keras.applications.inception_v3.preprocess_input

    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    preprocessed = preprocess_input(inputs)

    outputs = feature_extractor(preprocessed)
    return keras.Model(inputs, outputs, name="feature_extractor")

feature_extractor = build_feature_extractor()


def get_sequence_model():
    class_vocab = label_processor.get_vocabulary()

    frame_features_input = keras.Input((MAX_SEQ_LENGTH, NUM_FEATURES))
    mask_input = keras.Input((MAX_SEQ_LENGTH,), dtype="bool")

    x = keras.layers.GRU(16, frame_features_input, mask=mask_input)
    x = keras.layers.GRU(8)(x)
    x = keras.layers.Dropout(0.4)(x)
    x = keras.layers.Dense(8, activation="relu")(x)
    output = keras.layers.Dense(len(class_vocab), activation="softmax")(x)

    rnn_model = keras.Model([frame_features_input, mask_input], output)

    rnn_model.compile(loss="sparse_categorical_crossentropy",
                      optimizer="adam", metrics=["accuracy"])
    return rnn_model


def run_experiment():
    filepath = "/tmp/video_classifier"
    seq_model = get_sequence_model()
    history = seq_model.fit([train_data[0], train_data[1]], train_labels,
                            validation_split=0.3, epochs=EPOCHS, callbacks=[checkpoint])
    seq_model.load_weights(filepath)
    loss, accuracy = seq_model.evaluate([test_data[0], test_data[1]], test_labels)
    print(f"Test accuracy: {accuracy * 100}")
    return history, seq_model
history, sequence_model = run_experiment()


def prepare_single_video(frames):
    frames = frames[None, ...]
    frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH,), dtype="bool")

    frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES),
                              dtype="float32")
    return frame_features, frame_mask

def sequence_prediction(path):
    class_vocab = label_processor.get_vocabulary()
    frames = load_video(os.path.join("test", path))
    return frames

def to_gif(images):
    converted_images = images.astype(np.uint8)
    imageio.mimsave("animation.gif", converted_images, fps=10)
    return embed.embed_file("animation.gif")

test_video = np.random.choice(test_df["video_name"].values.tolist())
print(f"Test video path: {test_video}")

test_frames = sequence_prediction(test_video)

prepare_single_video(test_frames)

to_gif(test_frames[:MAX_SEQ_LENGTH])


""")
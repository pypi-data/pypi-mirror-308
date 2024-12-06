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
print("Prediction:", result)

from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16, DenseNet121
import numpy as np
from tensorflow.keras.preprocessing import image

# Set input shape
input_shape = (224, 224, 3)

# AlexNet Model
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

# DenseNet121 Model
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

# LeNet Model
def create_lenet():
    model = Sequential()
    model.add(Conv2D(6, kernel_size=(5, 5), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(16, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(120, activation='relu'))
    model.add(Dense(84, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    return model

# VGG16 Model
def create_vgg16():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    x = base_model.output
    x = Flatten()(x)
    x = Dense(4096, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(2, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    for layer in base_model.layers:
        layer.trainable = False
    return model

# Data generators
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

# Training and Saving Models
def train_and_save_model(model, model_name):
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(
        x_train,
        steps_per_epoch=len(x_train),
        epochs=5,
        validation_data=x_test,
        validation_steps=len(x_test)
    )
    model.save(f"{model_name}.h5")
    print(f"{model_name} training complete and saved as {model_name}.h5")

# Train AlexNet
print("Training AlexNet...")
alexnet_model = create_alexnet()
train_and_save_model(alexnet_model, "AlexNet")

# Train DenseNet121
print("Training DenseNet121...")
densenet121_model = create_densenet121()
train_and_save_model(densenet121_model, "DenseNet121")

# Train LeNet
print("Training LeNet...")
lenet_model = create_lenet()
train_and_save_model(lenet_model, "LeNet")

# Train VGG16
print("Training VGG16...")
vgg16_model = create_vgg16()
train_and_save_model(vgg16_model, "VGG16")

# Prediction function
def predict_with_model(model_name, img_path):
    model = load_model(f"{model_name}.h5")
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.
    y = model.predict(x)
    pred = np.argmax(y, axis=1)
    index = ['fresh', 'rotten']
    result = index[pred[0]]
    print(f"Prediction ({model_name}):", result)

# Predict using the models
img_path = r"/content/drive/MyDrive/CV exp1 dataset/Quality Dataset/valid/rotten/images-1-_jpeg.rf.9dfbf252510d9175da106c563bd4e1f9.jpg"
predict_with_model("AlexNet", img_path)
predict_with_model("DenseNet121", img_path)
predict_with_model("LeNet", img_path)
predict_with_model("VGG16", img_path)""")

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
        print("""import cv2
import torch
import torchvision.transforms as transforms
from torchvision import models
from collections import Counter
# Load a pre-trained ResNet model
model = models.resnet50(pretrained=True)
model.eval()
# Define image transformations
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
# Helper function to get labels for ImageNet classes
def load_labels():
    with open("imagenet-simple-labels.txt") as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

labels = load_labels()
# Function to classify a single frame
def classify_frame(frame):
    frame = transform(frame)
    frame = frame.unsqueeze(0)
    with torch.no_grad():
        outputs = model(frame)
    _, predicted = outputs.max(1)
    label = labels[predicted.item()]
    return label
# Function to extract frames and classify video
def classify_video(video_path, frame_interval=30):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    classifications = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            label = classify_frame(frame)
            classifications.append(label)

        frame_count += 1

    cap.release()
    return classifications
# Determine the most common classification
classifications = classify_video("/content/video2.mp4")
common_label = Counter(classifications).most_common(1)[0][0]
print(common_label)
#return common_label
# Usage example
video_path = "/content/video2.mp4"
category = classify_video(video_path)
print(f"Predicted category: {category}")
""")
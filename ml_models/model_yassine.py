# Importing pre-trained model
from keras.applications import ResNet50V2

# Importing important layers of Keras
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model

# Importing data functions
from ml_models.data_library.get_images import get_players_images_cropped
from ml_models.data_library.image_preprocessing import processing_images
from ml_models.data_library.class_preprocessing import preprocessing_classes

# Importing preprocessing functions
from sklearn.model_selection import train_test_split


# Saving the model in a variable
resnet = ResNet50V2(weights='imagenet', include_top=False)

# Processing the data
img_label_dict = get_players_images_cropped()
X, y = processing_images(img_label_dict)
y_cat = preprocessing_classes(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2)


# Add a new classification head
layer = resnet.output
layer = GlobalAveragePooling2D()(layer)
predictions = Dense(y.shape[0], activation='softmax')(layer)

# Create a new model with the added classification head
model = Model(inputs=resnet.input, outputs=predictions)


# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X_train,
          y_train,
          epochs=10,
          validation_split=0.2)

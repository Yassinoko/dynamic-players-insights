# Importing pre-trained model
from keras.applications import ResNet50V2

# Importing important layers of Keras
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model

# Importing data functions
from data_library.data_processing import black_white, crop, delete_face_images, encode

# Importing preprocessing functions
from sklearn.model_selection import train_test_split

directory_path =  "/Users/yassinebouaine/code/Yassinoko/dynamic-players-insights/data_processing/raw_data/faces"

faces_folder = "../data_processing/raw_data/faces/"
cropped_faces_directory = "../data_processing/raw_data/cropped_faces"

# # Processing the data
# black_white(faces_folder)
# crop(faces_folder, cropped_faces_directory)

# delete_face_images(cropped_faces_directory)

labels, players = encode(cropped_faces_directory)

# X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2)

# # Saving the model in a variable
# resnet = ResNet50V2(weights='imagenet', include_top=False)

# # Add a new classification head
# layer = resnet.output
# layer = GlobalAveragePooling2D()(layer)
# predictions = Dense(y.shape[0], activation='softmax')(layer)

# # Create a new model with the added classification head
# model = Model(inputs=resnet.input, outputs=predictions)

# # Compile the model
# model.compile(optimizer='adam',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])

# # Train the model
# model.fit(X_train,
#           y_train,
#           epochs=10,
#           validation_split=0.2)

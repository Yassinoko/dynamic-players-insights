import numpy as np

def get_class_from_array(array):

    predicted_class_index = np.argmax(array)

    unique_classes = ['alexander-arnold', 'benzema','asensio', 'carvajal',
                      'ceballos', 'courtois','henderson', 'lucas vázquez',
                      'mané', 'salah']

    return unique_classes[predicted_class_index]


# TESTING
# print(get_class_from_array(np.array([[8.4230096e-06, 7.5404896e-05, 1.6748409e-05, 7.4644736e-04,
#         4.2725692e-04, 1.9559382e-04, 9.9828511e-01, 9.3248847e-05,
#         1.5041530e-04, 1.3049315e-06]])))

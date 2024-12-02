import nltk
import json
import numpy as np
import random
import pickle
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import load_model

# Descargar recursos de NLTK si no están instalados
nltk.download('punkt')
nltk.download('wordnet')

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Cargar los datos de entrenamiento (intents)
with open('intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)

# Inicializar las listas para las palabras, las clases y los documentos
words = []
classes = []
documents = []

# Recorrer todas las intenciones y sus frases
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenizar cada palabra en las frases
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        
        # Agregar la frase como documento
        documents.append((pattern, intent['tag']))
    
    # Agregar las etiquetas de clases (intenciones)
    classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ['?', '¡', '!', '.', ',', ';', ':']]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Guardar las palabras y clases en archivos para usarlos más tarde
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Crear la matriz de características (bag of words)
training_sentences = []
training_labels = []

for doc in documents:
    # Tokenizar y lematizar el texto
    pattern_words = nltk.word_tokenize(doc[0])
    pattern_words = [lemmatizer.lemmatize(w.lower()) for w in pattern_words]
    
    # Crear la bolsa de palabras para la frase
    bag = []
    for word in words:
        bag.append(1 if word in pattern_words else 0)
    
    # Agregar la bolsa de palabras y la etiqueta de clase
    training_sentences.append(bag)
    training_labels.append(classes.index(doc[1]))

# Convertir las listas en arrays
training_sentences = np.array(training_sentences)
training_labels = np.array(training_labels)

# Dividir los datos en entrenamiento y prueba
train_x, test_x, train_y, test_y = train_test_split(training_sentences, training_labels, test_size=0.2)

# Crear el modelo de la red neuronal
model = Sequential()
model.add(Dense(128, input_dim=len(train_x[0]), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(classes), activation='softmax'))

# Compilar el modelo
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Guardar el modelo entrenado
model.save('chatbot_model.h5')

# Guardar el modelo entrenado
print("Modelo entrenado y guardado con éxito.")

# -*- coding: utf-8 -*-
"""M7 EjercicioFinal ErickSandoval.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zqJm84B1mkFvdq9_MRuDlIugIgsmFiLp

#**Setup**
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from math import sqrt

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

"""# **Set Data**"""

rawData = 'https://raw.githubusercontent.com/Rwyld/Data-Science-Models/main/RedesNeuronales/diabetes%20CSV.csv'

data = pd.read_csv(rawData)
data.head(3)

"""# **Analisis Exploratorio**"""

data.info()

data.describe()

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(10,5))
axes = axes.flat
#data = data.select_dtypes(include=['float64', 'int']).columns

graphData = data.drop('Outcome', axis=1)

for i, colum in enumerate(graphData):
    sns.histplot(
        data    = graphData,
        x       = colum,
        stat    = "count",
        kde     = True,
        color   = (list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
        line_kws= {'linewidth': 2},
        alpha   = 0.3,
        ax      = axes[i]
    )
    axes[i].set_title(colum, fontsize = 10, fontweight = "bold")
    axes[i].tick_params(labelsize = 8)
    axes[i].set_xlabel("")


fig.tight_layout()
plt.subplots_adjust(top = 0.9)
fig.suptitle('Distribución variables numéricas', fontsize = 10, fontweight = "bold");

"""**Resumen:** La data cargada no presenta datos faltantes o nulos. En cuanto a los datos visualizados en histogramas, no se observan posibles datos anomalos y las variables podemos observar una distribucion normal en Glucosa, BMI y BlooPressure.

# **Modelando Keras**

### **Split test/train data**
"""

X = data.drop('Outcome', axis = 1).values
y = data['Outcome'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=2023)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

"""### **Definiendo la red**"""

model = Sequential() 
model.add(Dense(100, activation='relu', input_dim=8)) 
model.add(Dense(50, activation='relu')) 
model.add(Dense(2, activation='sigmoid'))

"""### **Compilando**"""

model.compile(optimizer='adam',
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

"""### **Ajustando**"""

model.fit(X_train, y_train,epochs=150, batch_size=10, verbose = False)

"""# **Predicciones y conclusion**"""

predTraining = model.predict(X_train)
scores = model.evaluate(X_train, y_train, verbose=0)
print('Accuracy con la data train: {}% \n El error de la data de entrenamiento es: {}'.format(scores[1], 1 - scores[1]))   
 
predTesting= model.predict(X_test)
scores2 = model.evaluate(X_test, y_test, verbose=0)
print('Accuracy con la data test: {}% \n El error de la data de testeo es: {}'.format(scores2[1], 1 - scores2[1]))

"""**Conclusión**: La red obtuvo un 89% de precision en los datos de entrenamiento y un 81% en los datos de testeo, a pesar de ser una precision buena, el modelo puede mejorar su precision si se configura con otros hiperparametros y con una mayor cantidad de datos."""
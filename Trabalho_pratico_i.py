
#import libraries 
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

#dados de aprendizagem
url='https://github.com/Diegojfsr/RNA_Trabalho_Pratico_I/blob/main/train.csv?raw=true'
train = pd.read_csv(url)

# remove linhas contendo nan
#train.dropna(inplace=True)

# dados de teste
url='https://github.com/Diegojfsr/RNA_Trabalho_Pratico_I/blob/main/test.csv?raw=true'
test = pd.read_csv(url)

# Dados de envio
url='https://github.com/Diegojfsr/RNA_Trabalho_Pratico_I/blob/main/sample_submission.csv?raw=true'
sample_submission = pd.read_csv(url)

display(train) # Exibe o Dataframe

print(train.info()) # Exibe Informações do Dataframe

### Descobrir se tem valores vazios e a quantidade deles em cada coluna

#print(train.isna().any()) # Exibe como True ou False os valores do Dataframe
print(train.isna().sum()) # Exibe a soma dos valores no Dataframe

############## Tratando variaveis categoricas  ##############

#OneHotEncoding

!pip install category_encoders

import category_encoders as ce
from category_encoders.one_hot import OneHotEncoder, OrdinalEncoder

train.head()
#train.info(verbose=True)

#### Criado um Dataframe com as colunas que seram usadas   
####  Deletendo as colunas  "PassengerId","Name","Transported"  pois nao serao uteis

#dfTrain = train["HomePlanet","CryoSleep", "Cabin","Destination","Age","VIP","RoomService","FoodCourt","ShoppingMall","Spa","VRDeck","Transported"]
dfTrain = train.drop(["PassengerId","Name"], axis = 1)

# Converte os valores False e True da Coluna Transported para 0 e 1

dfTrain.replace({False: 0, True: 1}, inplace=True)

dfTrain.head()
#train.info(verbose=True)

# Converte as demais Colunas para dados Numericos e armazena os valores na variavel OrderEnc
 # A variavel OrderEnc recebe os dados convertidos de Destination // Converte a coluna Destination

OderEnc = OrdinalEncoder(cols =['HomePlanet','CryoSleep','Cabin','Destination','Age','VIP','RoomService','FoodCourt','ShoppingMall','Spa','VRDeck'])

# Faz a junção da coluna convertida com as demais do Dataframe //mas descarta a conversao anterior

OderEncFit = OderEnc.fit_transform(dfTrain)

##### Verificando os valores e colunas #####

#print(OderEncFit.isna().any()) # Exibe como True ou False os valores nan do Dataframe
#print(OderEncFit.isna().sum()) # Exibe a soma dos valores nan no Dataframe
OderEncFit.head()
#OderEncFit.info(verbose=True)
#print(OderEncFit.info())
#OderEncFit.shape
#OderEncFit.isna().sum()
#OderEncFit.isnull().sum()

X = OderEncFit.drop(["Transported",] , axis = 1)
Y = OderEncFit["Transported"]

X.shape

########## Treinando a Rede ##########

#https://keras.io/api/  (Keras Documentation)

import tensorflow as tf 
import keras 
from keras.models import Sequential      #Sequencia entre as camadas: Entrada - Oculta - Saida
from keras.layers import Dense, Dropout  #Iremos utilizar camadas densa na rede neural (full-connection)

#criar a rede neural sequencial 
ann = Sequential()

#definir as camadas de entrada, oculta 
ann.add( Dense(units = 6, activation = 'relu', kernel_initializer = 'random_uniform', input_dim=11))  #primeira camada oculta (nr_neuronios_entradas + nr_neuronios_saida / 2) = (30+1 / 2 = 16);  
                                                                                                       #input_dim = 30  (número de neuronios da camada de entrada = features de X_train)
#definir a camada de saida
ann.add(Dense(units = 1, activation = 'sigmoid'))

#configurar parâmetros da rede 
ann.compile(optimizer = 'adam',             #optimizer -> calculo dos ajustes dos pesos (descida do gradiente), calculo do delta
            loss='binary_crossentropy',     #loss -> calculo ou tratamento do erro      (binary_crossentropy -> para problemas de classificação binária)
            metrics = ['binary_accuracy']   #metrics -> avaliar a metrica do modelo ->   accuracy para problema de classificação binária 
           )

#treinar a rede neural
ann.fit(X, Y, batch_size = 10, epochs = 50)

#Realizando o calculo do loss e da acuracia da rede 

result = ann.evaluate(X, Y)

#Realizando as predições no conjunto de treino 

Ypred = ann.predict(X)  #calcula o valor 
Ypred

YpredBin = np.where(Ypred > 0.5, 1, 0)

resultado = pd.DataFrame()

resultado["Y"] = Y
resultado["Ypred"] = Ypred          #valores preditos para o conjunto de treinamento 
resultado["YpredBin"] = YpredBin
resultado.reset_index(inplace = True, drop=True)
resultado

resultado

sample_submission



submission2 = sample_submission.drop(["Transported"], axis = 1)
submission2.dropna(inplace=True)
submission2

submission3 = resultado.drop(["Y","Ypred"], axis = 1)
submission3.dropna(inplace=True)
submission3.replace({0: False, 1: True}, inplace=True) ### Converte os valores 0/1 em True/False
submission3

# append method
# result = submission2.append(submission3)
# result

submission = pd.concat([submission2, submission3], axis=1, join='inner')
display(submission)

## Converte o Nome da Coluna YpredBin para Transported

submission = submission.rename(columns={'YpredBin': 'Transported'})

submission

#criar um arquivo csv de saída como submit.csv

submission.to_csv("submission.csv", index=False)
print('Submission_final.csv foi salvo!')

#submit_final.csv foi salvo!


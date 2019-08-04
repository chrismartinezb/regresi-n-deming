import pandas as pd
import numpy as np
import math

def trans_path(path):
    
    '''Toma un path hacia un archivo .txt y regresa 2 dataframes, 1 con las mediciones de viento y producción y otro con las mediciones de viento para poder hacer predicciones en base a ellas.
    
    IN:
    path: path al archivo .txt, este debe contener los datos con exactamente el mismo formato especificado por el ejercicio. 
    
    OUT:
    preds y datos Dataframes.
    '''
    datos = pd.read_csv(path, delimiter=' ', header = None, names = ['Fecha','Hora','Producción','Velocidad'],skiprows=1,
                        parse_dates=[['Fecha', 'Hora']])
    
    preds = datos[pd.isnull(datos).any(axis=1)]
    
    #Actualizamos el dataframe para quitar las predicciones.
    datos = datos.dropna()

    #Quitamos la primera columna de 'preds' que no sirve para nada. Solo dice 'predicciones'.

    preds = preds[preds.Fecha_Hora != 'predicciones nan']
    
    preds.columns = ['Fecha','Velocidad', 'Predicción de Producción']
    
    return datos, preds

def f(B, x):
    '''Función lineal y = mx + b
    
    Scipy pasa Beta como una lista por eso usamos los indices en la función.'''
    return B[0]*x + B[1]


def hipotesis(beta0,beta1,x):
    '''
    Calcula el valor de una variable dependiente dadas la pendiente y ordenada de un modelo de regresion.
    
    IN:
       beta0: la ordenada de la hipótesis
       beta1: la pendiente de la hipótesis
       x:variable predictora 
    
    OUT:
       predicción 
    
    '''
    return beta0 + (beta1 * x)

def ema_p(beta0, beta1, X, y):
    ''' Calcula el porcentaje de error medio absoluto entre una serie de observaciones y predicciones.
    
    IN: 
        beta0: la ordenada de la hipotesis
        beta1: la pendiente de la hipotesis
        X:lista de variables predictoras
        y: lista de observaciones o variables dependientes
        
    OUT:
       Porcentaje de error medio absoluto con 2 decimales de precisión.
    
    '''
    ema = 0
    obs = 0

    for (xi,yi) in zip(X,y):
        ema += abs(hipotesis(beta0,beta1,xi) - yi)
        obs += yi
    #Si las suma de las obseraciones es un número muy cerca de 0, regresamos 0
    if obs < 1e-7:
        return 0
    ema_p = (100 / obs) * (ema)
    
    return round(ema_p,2)

def ecm_p(beta0, beta1, X, y):
    ''' Calcula el Porcentaje de error cuadrado medio entre una serie de observaciones y predicciones.
    
    IN: 
        beta0: la ordenada de la hipótesis
        beta1: la pendiente de la hipótesis
        X:lista de variables predictoras
        y: lista de observaciones o variables dependientes
        
    OUT:
       Porcentaje de error cuadrado medio con 2 decimales de precisión.'''
    
    ecm = 0
    obs = 0
    
    for (xi,yi) in zip(X,y):
        obs += yi
        ecm += (hipotesis(beta0,beta1,xi) - yi) ** 2 
        
    #Si las suma de las obseraciones es un número muy cerca de 0, regresamos 0
    if obs < 1e-7:
        return 0 
             
    ecm_p = ((100 * len(X))/obs) * (math.sqrt(ecm / len(X)))
    
    return round(ecm_p, 2)
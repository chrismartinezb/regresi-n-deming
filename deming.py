import funciones_de_ayuda as fda
import scipy.odr
import pandas as pd

class Modelo_Deming:
    
    ''' Inicializa un objeto de regresión con datos proporcionados por un archivo .txt'''
    
    def __init__(self, path):
        self.datos,self.predicciones = fda.trans_path(path) 
        self.y = self.datos.Producción
        self.X = self.datos.Velocidad
        self.s_yy = self.datos.cov()['Producción']['Producción']
        self.s_xx = self.datos.cov()['Velocidad']['Velocidad']
        self.beta0 = None
        self.beta1 = None
        self.ecmxmes = None
        self.emaxmes = None 

        
    def modelar(self):
        ''' Modela una línea de regresión ortogonal, nos regresa la pendiente y ordenada de esta.'''
        
        linear = scipy.odr.Model(fda.f)
        mydata =  scipy.odr.RealData(self.X, self.y, sx=self.s_xx, sy=self.s_yy)
        myodr = scipy.odr.ODR(mydata, linear, beta0=[1., 2.])
        myoutput = myodr.run()
        self.beta0, self.beta1  = myoutput.beta[1], myoutput.beta[0]
    
  
             
    def calcular_error(self):
        '''Calcula el %ECM y %EMA del modelo ortogonal por mes.'''
        if not self.beta0 or not self.beta1:
            print('Use el metodo .modelar(), para calcular el error, o introduzca sus propios valores para la ordenada y la pendiente')
        
        else:
            self.datos['Fecha_Hora'] = pd.to_datetime(self.datos['Fecha_Hora'])
            self.datos['año'] = pd.DatetimeIndex(self.datos.Fecha_Hora).year
            self.datos['mes'] = pd.DatetimeIndex(self.datos.Fecha_Hora).month
            
            self.ecmxmes = round (self.datos.groupby([self.datos.mes, self.datos.año]).apply(lambda row:fda.ecm_p(self.beta0,self.beta1,row['Velocidad'],row['Producción'])).mean(),2)
            
            self.emaxmes = round (self.datos.groupby([self.datos.mes, self.datos.año]).apply(lambda row:fda.ema_p(self.beta0, self.beta1,row['Velocidad'],row['Producción'])).mean(),2)
    
    def predecir(self):
        ''' Predice la producción usando la velocidad de las predicciones dadas por el usuario con base base a una regresión ortogonal'''
        if not self.beta0 or not self.beta1:
            print('Use el metodo .modelar(), para hacer predicciones, o introduzca sus propios valores para la ordenada y la pendiente')
        else:
            self.predicciones['Predicción de Producción'] = self.predicciones['Velocidad'].apply(lambda x: fda. hipotesis(self.beta0, self.beta1,x))
        
    
        
    

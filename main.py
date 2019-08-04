import deming

if __name__ == "__main__":
    print('Introduzca el path al archivo .txt:')
    
    path = str(input())
    
    Modelo = deming.Modelo_Deming(path)
    
    Modelo.modelar()
    Modelo.calcular_error()
    Modelo.predecir()
    
    print(f'La ordenada es {Modelo.beta0} y la pendiente es {Modelo.beta1}')
    print(f' Mes: % ECM:{Modelo.ecmxmes} %EMA: {Modelo.emaxmes}')
    print(Modelo.predicciones)
    
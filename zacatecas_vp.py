import variables_psicrometricas as vp
import pandas as pd

#Lectura del archivo csv para datos de temperatura de bulbo seco, humedad relativa y presión atmosférica
with open("zacatecas.csv", "r", newline="") as file:
    next(file) # Eliminar cabecera
    #Se asignan los datos de cada columna a una tupla con la funcion ZIP 
    TBS, RH, P = zip(*((float(n) for n in line.rstrip().rsplit(",", maxsplit=3)[-3:])for line in file))

#Convertir tupla a lista para operar con  los datos
TBS = list(TBS)
kPa = list(P).copy()
RH_d = list(RH).copy()

for i in range(len(RH_d)):
    RH_d[i] /= 100
    #Convertir hPa a kPa
    kPa[i] /= 10
    
#Listas vacias para almacenar los valores de las variables psicrométricas
PVS = []
PV = []
WS = []
W = []
H = []
TBH = []

#Con la función ZIP se puede recorre varias listas en un mismo bucle
for t,rh,p in zip(TBS,RH_d,kPa) :
    MU = []
    VEH = [] 
    TPR = []

    #Calculo de las variables psicrométricas
    pvs = vp.pres_vapor_sat(t)
    pv = vp.presion_vapor(rh,t)
    ws = vp.razon_hum_saturacion(p,t)
    w = vp.razon_humedad(t,rh,p)
    h = vp.entalpia(t,rh,p)
    tbh = vp.temp_bulbo_humedo1(t,rh)
    
    #Se agrega el valor obtenido a la lista correspondinete 
    PVS.append(pvs)
    PV.append(pv)
    WS.append(ws)
    W.append(w)
    H.append(h)
    TBH.append(tbh)

    for w,ws,pv in zip(W,WS,PV):
        mu = vp.grado_saturacion(w,ws)
        veh = vp.vol_esp_aire_humedo(t,w,p)
        tpr = vp.temp_punto_rocio(t,pv) 
        MU.append(mu)
        VEH.append(veh)
        TPR.append(tpr)

#Guardar la informacion en un archivo CSV usando pandas
#Diccionario de listas 
dict = {'TBS':TBS, 'HR':RH, 'PVS':PVS, 'PV':PV, 'WS':WS, 'W':W, 'MU':MU, 'VEH':VEH, 'TPR':TPR, 'H':H, 'TBH':TBH}
df = pd.DataFrame(dict)
df.to_csv("zacatecas_VP.csv",index=False)
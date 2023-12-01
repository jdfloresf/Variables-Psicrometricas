import variables_psicrometricas as vp
import pandas as pd

#Altitud en metros
Z = 2250

#Lectura del archivo csv para datos de temperatura de bulbo seco y humedad relativa (Media diaria)
#Tomados de la estacion meteorológica de la UACH correspondientes al mes de Abril de 2022

with open("abril.csv", "r", newline="") as file:
    next(file) # Eliminar cabecera
    #Se asigna cada columna de datos para obtener una tupla con la funcion ZIP 
    TBS, RH = zip(*((float(n) for n in line.rstrip().rsplit(",", maxsplit=2)[-2:])for line in file))

#Convertir tupla a lista para operar con  los datos
TBS = list(TBS)
RH_d = list(RH).copy()

for i in range(len(RH_d)):
    RH_d[i] /= 100
    
#Obtener la presión atmóosférica a la altitud Z
P_atm, T_aire = vp.pres_atm_temp(Z)

#Listas vacias para almacenar los valores de las variables psicrométricas
PVS = []
PV = []
WS = []
W = []
H = []
TBH = []

#Con la función ZIP se puede recorre varias listas en un mismo bucle
for t,rh in zip(TBS,RH_d) :
    MU = []
    VEH = [] 
    TPR = []

    #Calculo de las variables psicrométricas
    pvs = vp.pres_vapor_sat(t)
    pv = vp.presion_vapor(rh,t)
    ws = vp.razon_hum_saturacion(P_atm,t)
    w = vp.razon_humedad(t,rh,P_atm)
    h = vp.entalpia(t,rh,P_atm)
    tbh = vp.temp_bulbo_humedo(t,rh,P_atm)
    
    #Se agrega el valor obtenido a la lista correspondinete 
    PVS.append(pvs)
    PV.append(pv)
    WS.append(ws)
    W.append(w)
    H.append(h)
    TBH.append(tbh)

    for w,ws,pv in zip(W,WS,PV):
        mu = vp.grado_saturacion(w,ws)
        veh = vp.vol_esp_aire_humedo(t,w,P_atm)
        tpr = vp.temp_punto_rocio(t,pv) 
        MU.append(mu)
        VEH.append(veh)
        TPR.append(tpr)

#Guardar la informacion en un archivo CSV usando pandas
#Diccionario de listas 
dict = {'TBS':TBS, 'HR':RH, 'PVS':PVS, 'PV':PV, 'WS':WS, 'W':W, 'MU':MU, 'VEH':VEH, 'TPR':TPR, 'H':H, 'TBH':TBH}
df = pd.DataFrame(dict)
df.to_csv("VP.csv",index=False)

#Mostrar los resultados (descomentar para ver en consola)
# print("Presión Atmosferica (kPa): ", P_atm)
# print("\nTemperaturas (°C):\n", tbs)
# print("\nHumedad relativa (%): \n", RH)
# print("\nPresiones de vapor a saturación (Pa):\n", PVS)
# print("\nPresión de vapor (Pa):\n", PV)
# print("\nRazón de húmedad a sarutación:\n", WS)
# print("\nRazón de húmedad:\n", W)
# print("\nGrado de saturación:\n", MU)
# print("\nVolumen especifico del aire humedo (m^3/kg):\n", VEH)
# print("\nTemperatura de punto de rocio (°C):\n", TPR)
# print("\nEntalpía (kJ/kg):\n", H)
# print("\nTemperatura de bulbo humedo:\n ", TBH)
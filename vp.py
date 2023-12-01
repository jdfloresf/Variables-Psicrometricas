import variables_psicrometricas as vp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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
RH = list(RH)
RH_d = RH.copy()

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

############################## Carta Psicrometrica #################################
tbs_array = np.arange(5, 45, 0.1)       #Vector para temperatura de bulbo seco
RH_array = np.arange(0, 1.1, 0.1)       #Vector para Humedad relativa
tbh_array = np.arange(-10, 46, 2)       #Vector para temperatura de bulbo humedo    
entalpia_array = np.arange(0, 100, 5)   #Vector de entalpias 
pathc = []

with open("VP.csv", "r", newline="") as file:
    next(file) # Eliminar cabecera
    #Se asigna cada columna de datos para obtener una tupla con la funcion ZIP 
    TBS, RH, PVS, PV, WS, W,\
    MU, VEH, TPR, H, TBH = zip(*((float(n) for n in line.rstrip().rsplit(",", maxsplit=11)[-11:])for line in file))

#Convertir tupla a lista para operar con  los datos
TBS = list(TBS)
RH = list(RH)
W1 = list(W)
RH_d = RH.copy()

for i in range(len(RH_d)):
    RH_d[i] /= 100

_, ax = plt.subplots()

for rh in RH_array:
    W_array = []
    for tbs in tbs_array:         
        W = vp.razon_humedad(tbs,rh,P_atm)
        W_array.append(W)
    ax.plot(tbs_array, W_array, 'k')


for tbh in tbh_array:
    W_array = []
    tbs_plot = []
    for tbs in tbs_array:
        if tbh <= tbs:
            W = vp.razon_humedad_TBH(tbs,tbh,P_atm)
            W_array.append(W)
            tbs_plot.append(tbs) 
    ax.plot(tbs_plot, W_array, 'b')

for h in entalpia_array:
    W_array = []
    for tbs in tbs_array:
        W = vp.razon_hum_entalpia(tbs,h)
        W_array.append(W)
    ax.plot(tbs_array, W_array, 'g')

ax.vlines([5,10,15,20,25,30,35], ymin= 0, ymax= W_array[9], color='purple') 

ax.plot(TBS, W1, 'x', color="r", label="Datos")

black_patch = mpatches.Patch(color='k', label='Humedad relativa')
pathc.append(black_patch)
blue_patch = mpatches.Patch(color='blue', label='Lineas de saturación')
pathc.append(blue_patch)
green_patch = mpatches.Patch(color='green', label='Entalpía')
pathc.append(green_patch)
purple_patch = mpatches.Patch(color='purple', label='Temp bulbo seco')
pathc.append(purple_patch)
red_patch = mpatches.Patch(color='red', label='Datos')
pathc.append(red_patch)

ax.set(ylim=(0, 0.025), xlim=(5, 40), ylabel=r"Razón de humedad [$kg_{agua}/kg_{aire}$]", xlabel="Temperatura de bulbo seco[°C]")
ax.yaxis.tick_right()
ax.yaxis.set_label_position('right')
plt.title("Carta Psicrométrica")
plt.tight_layout()
plt.legend(handles=pathc)
plt.show()
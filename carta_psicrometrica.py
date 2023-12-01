import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import variables_psicrometricas as vp

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

Z = 0       #Altitud en metros

_, ax = plt.subplots()
P_atm,temp = vp.pres_atm_temp(Z)

#Se generan las lineas de humedad relativa
for rh in RH_array:
    W_array = []
    for tbs in tbs_array:         
        W = vp.razon_humedad(tbs,rh,P_atm)
        W_array.append(W)
    ax.plot(tbs_array, W_array, 'k')

#Se generan las lineas de saturación
for tbh in tbh_array:
    W_array = []
    tbs_plot = []
    for tbs in tbs_array:
        if tbh <= tbs:
            W = vp.razon_humedad_TBH(tbs,tbh,P_atm)
            W_array.append(W)
            tbs_plot.append(tbs) 
    ax.plot(tbs_plot, W_array, 'b')

#Se generan las lineas de entalpia
for h in entalpia_array:
    W_array = []
    for tbs in tbs_array:
        W = vp.razon_hum_entalpia(tbs,h)
        W_array.append(W)
    ax.plot(tbs_array, W_array, 'g')

#Se generan las lineas de temperatura de bulbo seco
ax.vlines([5,10,15,20,25,30,35], ymin= 0, ymax= W_array[9], color='purple') 

#Se grafican los datos con TBS y W
ax.plot(TBS, W1, 'x', color="r", label="Datos")

#Se generan las leyendas 
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

#Se establecen los limites de la grafica 
ax.set(ylim=(0, 0.025), xlim=(5, 40), ylabel=r"Razón de humedad [$kg_{agua}/kg_{aire}$]", xlabel="Temperatura de bulbo seco[°C]")
ax.yaxis.tick_right()
ax.yaxis.set_label_position('right')
plt.title("Carta Psicrométrica")
plt.tight_layout()
plt.legend(handles=pathc)
plt.show()
import math

Ra = 287.055
TOLERANCIA = 0.001      #Tolerancia para las iteraciones para NR
MIN_HUM_RATIO = 1E-7    #Valor mínimo que puede tener la razón de humedad
MAX_ITER = 100 

#Función para calcular la presión atmorférica y temperatura del aire en función de la altitud (Z),
#en el rango de -5000 a 11000 metros
def PresAtmTemp(Z: float) -> float:
    P_atm = 101.325*(1 - 2.25577e-5 * Z)**(5.2559)
    tmp = 15-0.0065*Z
    return P_atm, tmp

#Presión de vapor a saturación en función de la temperatura (K)
def PresVaporSat(tbs: list) -> list:
    Pvs_list = []
    tbs1 = tbs.copy()
    for i in range(len(tbs)):
        if tbs1[i] >= -100 and tbs1[i] <= 0:
            A1 = -5.6745359e03 
            A2 = 6.3925247
            A3 = -9.677843e-03
            A4 = 0.6221570e-06
            A5 = 2.0747825e-09
            A6 = -0.94844024e-12
            A7 = 4.1635019
            
            tbs1[i] += 273.15

            Pvs = math.exp((A1/tbs1[i]) + A2+ A3*(tbs1[i]) + A4*(tbs1[i])**2 + \
                        A5*(tbs1[i])**3 + A6*(tbs1[i])**4 + A7*math.log(tbs1[i]))/1000
            Pvs_list.append(Pvs)

        elif tbs1[i] > 0 and tbs1[i] <= 200:
            A1 = -5.8002206e03 
            A2 = 1.3914993
            A3 = -48.640239e-03
            A4 = 41.764768e-06
            A5 = -14.452093e-09
            A6 = 0.0
            A7 = 6.5459673

            tbs1[i] += 273.15

            Pvs = math.exp((A1/tbs1[i]) + A2+ A3*(tbs1[i]) + A4*(tbs1[i])**2 + \
                        A5*(tbs1[i])**3 + A6*(tbs1[i])**4 + A7*math.log(tbs1[i]))/1000
            Pvs_list.append(Pvs)
    return Pvs_list

#Presión de vapor en función de la HR
def PresionVapor(RH: list, tbs: list) -> list:
    Pv_list = []
    Pvs = PresVaporSat(tbs)
    for i in range(len(RH)):
        RH[i] /= 100
        Pv = RH[i] * Pvs[i]
        Pv_list.append(Pv)
    return Pv_list

#Razón de humedad de agua a saturacion en función de la presión atmosférica y la presión de vapor a saturación
def RazonHumSaturacion(P_atm: float, tbs: list) -> list:
    Ws_list = []
    Pvs = PresVaporSat(tbs)
    for i in range(len(tbs)):
        Ws = 0.62198*Pvs[i] / (P_atm-Pvs[i])
        Ws_list.append(Ws)
    return Ws_list

#Razón de humedad
def RazonHumedad(tbs: list, RH: list, P_atm: float) -> list:
    W_list = []
    Pv = PresionVapor(RH, tbs)
    for i in range(len(tbs)):
        W = 0.622*Pv[i] / (P_atm-Pv[i])
        W_list.append(W)
    return W_list

#Grado de saturación
def GradoSaturacion(W: list, Ws: list) -> list:
    Mu_list = []
    for i in range(len(W)):
        Mu = W[i]/Ws[i]
        Mu_list.append(Mu)
    return Mu_list

#Volumen especifico del aire humedo
def VolEspAireHumedo(T: list, W: list, P: list) -> list:
    Veh_list = []
    for i in range(len(T)):
        Veh = ((Ra*(T[i]+273.15))/(P*1000)) * (1 + 1.6078*W[i])/(1+W[i])
        Veh_list.append(Veh)
    return Veh_list

#Temperatura del punto de rocio, en función de la temperatura en °C y la presion en Pa
def TempPuntoRocio(T: list, Pv: list) -> list:
    Tpr_list= []
    for i in range(len(T)):
        if T[i] > -60 and T[i] <= 0:
            Pv[i] *= 1000
            Tpr = -60.450 + 7.0322*math.log(Pv[i]) + 0.3700*(math.log(Pv[i]))**2
            Tpr_list.append(Tpr)
    
        elif T[i] > 0 and T[i] < 70:
            Pv[i] *= 1000
            Tpr = -35.957 - 1.8726*math.log(Pv[i]) + 1.1689*(math.log(Pv[i]))**2
            Tpr_list.append(Tpr)
    return Tpr_list

#Entalpía
def Entalpia(T: list, W: list) -> list:
    h_list = []
    for i in range(len(T)):
        h = 1.006*T[i] + W[i]*(2501+1.805*T[i])
        h_list.append(h)
    return h_list

def TempBulboHumedo(T, RH):
    tbh_list = []
    for i in range(len(T)):
        RH[i] *= 100
        tbh = T[i]*math.atan(0.151977*(RH[i] + 8.313659)**0.5) + math.atan(T[i] + RH[i]) 
        - math.atan(RH[i] - 1.676331) + 0.00391838*RH[i]**(1.5) * math.atan(0.023101*RH[i]) - 4.686035
        tbh_list.append(tbh)
    return tbh_list
#variables_psicrometricas (version 1.0)

""" variables_psicrometricas.py

Contiene funciones para calcular propiedades termodinámicas de mezclas de 
gas y vapor de forma escalar. Librería desarrollada para la materia de automatización 
de biosistemas, de la carrera de Ingeniería Mecatrónica Agrícola, adecuada para 
aplicaciones de ingeniería, física y meteorología.     

Las funciones de esta librería se encuentran en el capítulo 6 del ASHRAE Fundamentals Handbook (2001).  
Todas las funciones están implementadas para el sistema internacional de unidades (SI).

Example
    >>> import variables_psicrometricas as vp
    >>> # Calcular TempBulboHum  con TempBulboSeco de 20°C y humedad relativa del 50%
    >>> tbh = vp.TempBulboHumedo(20,0.5)
    >>> print(tbh)
    13.699341968988136

Note
    La librería esta basada en la situación 3, donde se tienen como datos la temperatura de bulbo seco, 
    la humedad relativa y la presión atmosférica. Con las funciones se obtiene:
    -Presión de vapor a saturación 
    -Presión de vapor
    -Razón de humedad a saturación
    -Razón de humedad
    -Grado de saturación
    -Volumen especifico del aire humedo 
    -Entalpía
    -Temperatura del punto de roció 
    -Temperatura del bulbo humedo*

    *Se obtiene a partir de una formula en función de la teperatura de bulbo seco y la humedad relativa,
     la presición del resultado se aproxima al valor de THB real obtenido de la carta psicrométrica.
"""

import math

Ra = 287.055            #Constante de los gases ideales

#Función para calcular la presión atmosférica y temperatura del aire en función de la altitud (Z),
#en el rango de -5000 a 11000 metros
def PresAtmTemp(Z: float) -> tuple:
    Z = 101.325 * (1 - 2.25577e-05 * Z)**(5.2559)
    temp = 15-0.0065*Z
    
    return Z, temp

#Presión de vapor a saturación en función de la temperatura (K)
def PresVaporSat(tmp: float) -> float:
    if tmp > -100 and tmp <= 0:
        A1 = -5.6745359e03 
        A2 = 6.3925247
        A3 = -9.677843e-03
        A4 = 0.6221570e-06
        A5 = 2.0747825e-09
        A6 = -0.94844024e-12
        A7 = 4.1635019

        tmp += 273.15

        pvs = math.exp((A1/tmp) + A2+ A3*tmp + A4*tmp**2 + A5*tmp**3 + A6*tmp**4 + A7*math.log(tmp))
        return pvs

    elif tmp > 0 and tmp < 200:
        A1 = -5.8002206e03 
        A2 = 1.3914993
        A3 = -48.640239e-03
        A4 = 41.764768e-06
        A5 = -14.452093e-09
        A6 = 0.0
        A7 = 6.5459673

        tmp += 273.15

        Pvs = (math.exp((A1/tmp) + A2 + A3*tmp + A4*tmp**2 + A5*tmp**3 + A6*tmp**4 + A7*math.log(tmp)))/1000
        return Pvs

#Presión de vapor en función de la HR
def PresionVapor(RH: float, Pvs: float) -> float:
    Pv = RH*Pvs
    return Pv

#Razón de humedad de agua a saturacion en función de la presión atmosférica y la presión de vapor a saturación
def RazonHumSaturacion(P_atm: float, Pvs: float) -> float:
    Ws = 0.62198 * Pvs / (P_atm-Pvs)
    return Ws

#Razón de humedad
def RazonHumedad(P_atm: float, Pv: float) -> float:
    W = 0.622*Pv/(P_atm-Pv)
    return W

#Grado de saturación
def GradoSaturacion(W: float, Ws: float) -> float:
    Mu = W/Ws
    return Mu
    
#Volumen especifico del aire humedo
def VolEspAireHumedo(T: float, W: float, P: float) -> float:
    Veh = (Ra*(T+273.15)/(P*1000)) * (1 + 1.6078*W)/(1+W)
    return Veh

# def temp_punto_rocio(tbs: float, pv: float) -> float:
#     """
#     Retorna la temperatura del punto de roció teniendo la temperatura de bulbo seco 
#     y la presión de vapor.

#     Args:
#         tbs: Temperatura de bulbo seco en °C
#         pv: Presión de vapor en kPa
    
#     Returns:
#         Temperatura de punto de roció en °C
#     """
#     LIM = [-100, 200]
#     #Comprobación: Fuera de los limites no se puede encontrar solución
#     if pv < pres_vapor_sat(LIM[0]) or pv > pres_vapor_sat(LIM[1]):
#         raise ValueError("Presión de vapor de agua esta fuera del rango valido")
    
#     #Usando NR para aproximar
#     tpr = tbs            #tpr para la iteración   
#     lnPV = math.log(pv)  #presión de vapor de agua 

#     i = 1

#     while True:
#         tpr_i = tpr #tpr para el calculo en el NR
#         lnPV_i = math.log(pres_vapor_sat(tpr_i))

#         #Derivada de la funcion, analiticamente
#         d_lnPV = dLnPws(tpr_i)

#         #Nueva estimación
#         tpr = tpr_i - (lnPV_i - lnPV) / d_lnPV
#         tpr = max(tpr, LIM[0])
#         tpr = min(tpr, LIM[1])

#         if((math.fabs(tpr - tpr_i) <= TOLERANCIA)):
#             break
#         if(i > MAX_ITER):
#             raise ValueError("No hay convergencia para tpr. Proceso detenido")

#         i += 1

#     tpr = min(tpr, tbs)
#     return tpr

#Temperatura del punto de rocio, en función de la temperatura en °C y la presion en Pa
def TempPuntoRocio(T: float, Pv: float) -> float:
    if T > -60 and T <= 0:
        Pv *= 1000
        Tpr = -60.450 + 7.0322*math.log(Pv) + 0.3700*(math.log(Pv))**2
        return Tpr
    
    elif T > 0 and T < 70:
        Pv *= 1000
        Tpr = -35.957 - 1.8726*math.log(Pv) + 1.1689*(math.log(Pv))**2
        return Tpr


#Entalpía
def Entalpia(T: float, W: float) -> float:
    h = 1.006*T + W*(2501+1.805*T)
    return h

def TempBulboHumedo(t: float, RH: float) -> float:
    RH *= 100
    tbh = t*math.atan(0.151977*(RH + 8.313659)**0.5) + math.atan(t + RH) \
           - math.atan(RH - 1.676331) + 0.00391838*RH**(1.5) * math.atan(0.023101*RH) - 4.686035
    return tbh
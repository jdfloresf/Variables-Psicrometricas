#variables_psicrometricas (version 2.0)
""" variables_psicrometricas.py

Contiene funciones para calcular propiedades termodinámicas de mezclas de 
gas y vapor de forma escalar. Librería desarrollada para la materia de automatización 
de biosistemas de la carrera de Ingeniería Mecatrónica Agrícola, adecuada para 
aplicaciones de ingeniería, física y meteorología.     

Las funciones de esta librería se encuentran en el capítulo 6 del ASHRAE Fundamentals Handbook (2001).  
Todas las funciones están implementadas para el sistema internacional de unidades (SI).

En esta nueva versión la temperatura de punto de roció y la temperatura de bulbo humedo se 
obtienen a partir del método numérico Newton-Raphson, al ser un proceso iterativo las temperaturas
obtenidas en ambos casos son más exactas.

Example
    >>> # Calcular TempBulboHum  con TempBulboSeco de 20 °C, humedad relativa del 50%, presión de 101.325 kPa
    >>> import variables_psicrometricas as vp
    >>> tbh = vp.temp_bulbo_humedo(20, 0.5, 101.325)
    >>> print(tbh)
    13.78336966431862

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
    -Temperatura de bulbo humedo
"""

import math

#Variables Globales 
Ra = 287.055            #Constante de los gases ideales
TOLERANCIA = 0.001      #Tolerancia para NR
MIN_HUM_RATIO = 1E-7    #Valor mínimo que puede tener la razón de humedad
MAX_ITER = 100          #Máximo numero de iteraciones para NR

def pres_atm_temp(Z: float) -> float:
    """
    Retorna la presión atmosferica y la temperatura  teniendo como dato
    la altitid (Z) en el rango de -5000 a 11000 metros.

    Args:
        Z: Altitid en metros
    
    Returns:
        Presión atmosférica en kPa
        Temperatura en °C
    """
    Z = 101.325 * (1 - 2.25577e-05 * Z)**(5.2559)
    temp = 15-0.0065*Z
    
    return Z, temp

def pres_vapor_sat(tbs: float) -> float:
    """
    Retorna la presión de vapor a saturacion teniendo como dato
    la temperatura de bulbo seco.

    Args:
        tbs: temperatura de bulbo seco en °C
    
    Returns:
        Presión de vapor a saturación en Pa
    """
    if tbs >= -100 and tbs <= 0:
        A1 = -5.6745359e03 
        A2 = 6.3925247
        A3 = -9.677843e-03
        A4 = 6.2215701e-07
        A5 = 2.0747825e-09
        A6 = -9.484024e-13
        A7 = 4.1635019

        tbs += 273.15

        PresVapSat = math.exp((A1/tbs) + A2+ A3*tbs + A4*tbs**2 + A5*tbs**3 + A6*tbs**4 + A7*math.log(tbs))
        return PresVapSat

    elif tbs > 0 and tbs <= 200:
        A1 = -5.8002206e03 
        A2 = 1.3914993
        A3 = -4.8640239e-02
        A4 = 4.1764768e-05
        A5 = -1.4452093e-08
        A6 = 0.0
        A7 = 6.5459673

        tbs += 273.15

        PresVapSat = (math.exp((A1/tbs) + A2 + A3*tbs + A4*tbs**2 + A5*tbs**3 + A6*tbs**4 + A7*math.log(tbs)))/1000
        return PresVapSat

def presion_vapor(RH: float, tbs: float) -> float:
    """
    Retorna la presión parcial de vapor dea agua en función de 
    temperatura de bulbo seco y la humedad relativa.

    Args:
        tbs: temperatura de bulbo seco en °C
        RH: Humedad relativa en porcentaje
    
    Returns:
        Presión parcial de vapor de agua en kPa
    """
    if RH < 0 or RH > 1:
        raise ValueError("Humedad relativa esta fuera del rango [0, 1]")

    PresVap = RH * pres_vapor_sat(tbs)
    return PresVap

def razon_hum_saturacion(P_atm: float, tbs: float) -> float:
    """
    Retorna la razón de humedad del aire a saturacion teniendo la temperatura 
    de bulbo seco y la presión atmosférica.

    Args:
        P_atm: Presión atmosférica en kPa
        tbs: temperatura de bulbo seco °C
    
    Returns:
        Razón de humedad a saturación en kg_agua/kg_aire
    """
    pvs = pres_vapor_sat(tbs)
    Ws = 0.62198 * pvs / (P_atm - pvs)

    return Ws

def razon_humedad(tbs: float, RH: float, P_atm: float) -> float:
    """
    Retorna la razón de humedad del aire teniendo la temperatura de bulbo seco
    la humedad relativa y la presión atmosférica.

    Args:
        P_atm: Presión atmosférica en kPa
        tbs: temperatura de bulbo seco °C
        RH: Humedad relativa en porcentaje
    
    Returns:
        Razón de humedad en kg_agua/kg_aire
    """
    pv = presion_vapor(RH, tbs)
    W = 0.62198 * pv / (P_atm-pv)

    return W

def grado_saturacion(W: float, Ws: float) -> float:
    """
    Retorna el grado de saturación (razón de humedad del aire/razón de humedad del aire a saturación
    a la misma temperatura y presión).

    Args:
        Ws: Razón de humedad del aire a saturacion
        W: Razón de humedad del aire
    
    Returns:
        Grado de saturación en unidades arbitrarias
    """
    return W/Ws
    
def vol_esp_aire_humedo(T: float, W: float, P: float) -> float:
    """
    Retorna el volumen específico de aire humedo teniendo la temperatura de bulbo seco,
    la razón de humedad y la presión.

    Args:
        T: Temperatura de bulbo seco en °C
        W: Razón de humedad del aire
        P: Presión atmosférica en kPa
    
    Returns:
        Volumen específico de aire humedo en m³/kg_aire humedo
    """
    Veh = (Ra * (T+273.15) / (P*1000)) * ((1 + 1.6078*W)/(1+W))

    return Veh

def temp_punto_rocio(T: float, Pv: float) -> float:
    if T > -60 and T <= 0:
        Pv *= 1000
        Tpr = -60.450 + 7.0322*math.log(Pv) + 0.3700*(math.log(Pv))**2
        return Tpr
    
    elif T > 0 and T < 70:
        Pv *= 1000
        Tpr = -35.957 - 1.8726*math.log(Pv) + 1.1689*(math.log(Pv))**2
        return Tpr

def entalpia(T: float, RH: float, P_atm: float) -> float:
    """
    Retorna la entalpía teniendo la temperatura de bulbo seco

    Args:
        T: Temperatura de bulbo seco en °C
        W: Razón de humedad del aire
    
    Returns:
        Entalpía kJ/kg
    """
    W = razon_humedad(T,RH,P_atm)
    h = 1.006*T + W*(2501+1.805*T)

    return h

def temp_bulbo_humedo1(t: float, RH: float) -> float:
    RH *= 100
    tbh = t*math.atan(0.151977*(RH + 8.313659)**0.5) + math.atan(t + RH) \
           - math.atan(RH - 1.676331) + 0.00391838*RH**(1.5) * math.atan(0.023101*RH) - 4.686035
    return tbh

def temp_bulbo_humedo(tbs: float, RH: float, P_atm: float) -> float:
    """
    Retorna la temperatura de bulbo humedo teniendo la temperatura de bulbo seco, 
    la humedad relativa y la presión atmosférica.

    Args:
        tbs: Temperatura de bulbo seco en °C
        RH: Humedad relativa en porcentaje
        P_atm: Presión atmosférica en kPa
    
    Returns:
        Temperatura de bulbo humedo en °C
    """
    W = razon_humedad(tbs, RH, P_atm)
    if W < 0:
        raise ValueError("Razón de humedada no puede ser negativo")

    #Se comprueba que W sea mayor que MIN_HUM_RATIO 
    lim_W = max(W, MIN_HUM_RATIO)
    
    #Se obtiene la temperatura de punto de rocio a partir de la presión de vapor
    pv = presion_vapor(RH, tbs)
    tpr = temp_punto_rocio(tbs, pv)

    #Valores iniciales
    tbh_sup = tbs
    tbh_inf = tpr
    tbh = (tbh_inf + tbh_sup)/2

    i = 1

    while ((tbh_sup - tbh_inf) > TOLERANCIA):
        #Calcular Razón de humdedad a la temperatura TBH_i
        W_inicial = razon_humedad_TBH(tbs, tbh, P_atm)

        #Obtener nuevos limites
        if W_inicial > lim_W:
            tbh_sup = tbh
        else:
            tbh_inf = tbh

        #Nuevo valor de tbh
        tbh = (tbh_sup + tbh_inf)/2

        if(i >= MAX_ITER):
            raise ValueError("No se logro convergencia para thb. Proceso terminado.")
        i += 1
    return tbh
 
def razon_humedad_TBH(tbs: float, tbh: float, P_atm: float) -> float:
    """
    Retorna la razón de humedad a la temperatura de bulbo humedo teniendo la temperatura de bulbo seco,
    temperatura de bulbo humedo y la presión. 

    Args:
        tbs: Temperatura de bulbo seco en °C
        tbh: Temperatura de bulbo humedo en °C
        P_atm: Presión atmosférica en kPa
    
    Returns:
        Razón de humedad en kg_agua/kg_aire
    """
    if tbh > tbs:
        raise ValueError("TBH no puede ser mayor que TBS")

    Ws = razon_hum_saturacion(P_atm, tbh)

    if tbh >= 0:
        W = ((2501. - 2.326 * tbh) * Ws - 1.006 * (tbs - tbh)) / (2501. + 1.86 * tbs - 4.186 * tbh)
    else:
        W = ((2830. - 0.24 * tbh) * Ws - 1.006 * (tbs - tbh)) / (2830. + 1.86 * tbs - 2.1 * tbh)

    return max(W, MIN_HUM_RATIO)

def razon_hum_entalpia(T: float, h: float) -> float:
    """
    Retorna la razón de humedad teniendo la temperatura de bulbo seco y la entalpía

    Args:
        T: Temperatura de bulbo seco en °C
        h: Entalpía en kJ/kg
    
    Returns:
        Razón de humedad
    """
    W = (h - 1.006*T) / (2501 + 1.805*T)

    return W

def dLnPws(tbs: float) -> float:
    """
    Función auxiliar que retorna la derivada del logaritmo natural de la presión de vapor a saturación
    en función de la temperaturade bulbo seco.

    Args:
        tbs: Temperatura de bulbo seco en °C
    
    Returns:
        Derivada del logaritmo natural de la presión de vapor a saturación en Pa
    """
    T = tbs + 273.15
    if tbs <= 0.01:
        _dLnPws = 5.6745359E+03 / T**2 - 9.677843E-03 + 2 * 6.2215701E-07 * T + 3 * 2.0747825E-09 * T**2 - 4 * 9.484024E-13 * T**3 + 4.1635019 / T
    else:
        _dLnPws = 5.8002206E+03 / T**2 - 4.8640239E-02 + 2 * 4.1764768E-05 * T - 3 * 1.4452093E-08 * T**2 + 6.5459673 / T

    return _dLnPws
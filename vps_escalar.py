import variables_psicrometricas as vp
from tkinter import *

#Variables globales
tbs = 19.7
RH = 0.15
Z = 2250

P_atm, T_aire = vp.pres_atm_temp(Z)
Pvs = vp.pres_vapor_sat(tbs)
Pv = vp.presion_vapor(RH, tbs)
Ws = vp.razon_hum_saturacion(P_atm, tbs) 
W = vp.razon_humedad(tbs, RH, P_atm)
Mu = vp.grado_saturacion(W, Ws)
Veh = vp.vol_esp_aire_humedo(tbs, W, P_atm)
tpr = vp.temp_punto_rocio(tbs,Pv)
h = vp.entalpia(tbs, RH, P_atm)
tbh = vp.temp_bulbo_humedo1(tbs,RH)

root = Tk()
root.title("Variables psicrométricas")
root.config(bd=20)

Label(root, text="Presión Atmósferica (kPa)").pack()
Label(root, text=P_atm).pack()
Label(root, text="Temperatura de bulbo seco (°C)").pack()
Label(root, text=tbs).pack()
Label(root, text="Humedad relativa (%)").pack()
Label(root, text=RH*100).pack()
Label(root, text="Presión de vapor a saturación (Pa)").pack()
Label(root, text=Pvs).pack()
Label(root, text="Presión de vapor (kPa)").pack()
Label(root, text=Pv).pack()
Label(root, text="Razón de humedad a saturación (kg_agua/kg_aire)").pack()
Label(root, text=Ws).pack()
Label(root, text="Razón de humedad (kg_agua/kg_aire)").pack()
Label(root, text=W).pack()
Label(root, text="Volumen especifico del aire humedo (m^3/kg_aire_humedo)").pack()
Label(root, text=Veh).pack()
Label(root, text="Grado de saturación").pack()
Label(root, text=Mu).pack()
Label(root, text="Temperatura de punto de rocio (°C)").pack()
Label(root, text=tpr).pack()
Label(root, text="Entalpía (kJ/kg)").pack()
Label(root, text=h).pack()
Label(root, text="Temperatura de bulbo humedo (°C)").pack()
Label(root, text=tbh).pack()

root.mainloop()



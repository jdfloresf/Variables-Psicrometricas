import matplotlib.pyplot as plt
import numpy as np
from psychrochart import PsychroChart

# Pass a dict with the changes wanted:
custom_style = {
    "figure": {
        # "title": "Psychrometric Chart (sea level)",
        "x_label": "DRY-BULB TEMPERATURE, $°C$",
        "y_label": "HUMIDITY RATIO $w, g_w / kg_{da}$",
        "x_axis": {"color": [1.0, 1.0, 1.0], "linewidth": 1.5, "linestyle": "-"},
        "x_axis_labels": {"color": [1.0, 1.0, 1.0], "fontsize": 8},
        "x_axis_ticks": {"direction": "out", "color": [1.0, 1.0, 1.0]},
        "y_axis": {"color": [1.0, 1.0, 1.0], "linewidth": 1.5, "linestyle": "-"},
        "y_axis_labels": {"color": [1.0, 1.0, 1.0], "fontsize": 8},
        "y_axis_ticks": {"direction": "out", "color": [1.0, 1.0, 1.0]},
        "partial_axis": False,
        "position": [0.025, 0.075, 0.925, 0.875]
        },
    "limits": {
        "range_temp_c": [0, 40],
        "range_humidity_g_kg": [0, 30],
        "altitude_m": 0,
        "step_temp": 1.0
        },
    "saturation": {"color": [1.0, 1.0, 1.0], "linewidth": 2, "linestyle": "-"},
    "constant_rh": {"color": [0.8, 0.0, 0.0], "linewidth": 1, "linestyle": "-"},
    "constant_v": {"color": [0.0, 0.4, 0.4], "linewidth": 0.5, "linestyle": "-"},
    "constant_h": {"color": [1, 0.4, 0.0], "linewidth": 0.75, "linestyle": "-"},
    "constant_wet_temp": {"color": [0.2, 0.8, 0.2], "linewidth": 1, "linestyle": "--"},
    "constant_dry_temp": {"color": [1.0, 1.0, 1.0], "linewidth": 0.25, "linestyle": "-"},
    "constant_humidity": {"color": [1.0, 1.0, 1.0], "linewidth": 0.25, "linestyle": "-"},
    "chart_params": {
        "with_constant_rh": True,
        "constant_rh_curves": [20, 30, 40, 50, 60, 70, 80, 90],
        "constant_rh_labels": [20, 40, 60, 80],
        "with_constant_v": False,
        "constant_v_step": 0.01,
        "range_vol_m3_kg": [0.78, 0.96],
        "with_constant_h": True,
        "constant_h_step": 10,
        "constant_h_labels": [0],
        "range_h": [10, 130],
        "with_constant_wet_temp": True,
        "constant_wet_temp_step": 1,
        "range_wet_temp": [-10, 35],
        "constant_wet_temp_labels": [0, 5, 10, 15, 20, 25, 30],
        "with_constant_dry_temp": True,
        "constant_temp_step": 5,

        "with_constant_humidity": True,
        "constant_humid_step": 2,

        "with_zones": False
        }
    }

fig, ax = plt.subplots(figsize=(7, 3))
chart = PsychroChart(custom_style)
chart.plot(ax)
plt.show()
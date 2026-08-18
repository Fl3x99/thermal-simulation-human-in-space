from src.human import Human
from src.environment import Environment
from src.radiation import calculate_IR_emitted_power,calculate_cmb_absorbed_power, calculate_I_sun_distance, calculate_abs_sun_power, calculate_IR_earth_distance, calculate_abs_IR_earth_power, calculate_abs_albedo_power
from src.simulation import calculate_net_power, calculate_temperature_change, euler_step, run_simulation

astronaut = Human(
    mass = 90,
    temperature = 310.15,
    specific_heat_capacity = 3500,
    metabolic_power = 100,
    emissivity_ir = 0.98,
    absorptivity_sun = 0.7,
    absorptivity_ir = 0.98,
    head_radius = 0.12,
    torso_height = 0.65,
    torso_width = 0.42,
    torso_depth = 0.24,
    arm_length = 0.63,
    arm_radius = 0.05,
    leg_length = 0.93,
    leg_radius = 0.075,
    )

environment = Environment(
    sun_distance = 1, #in AE
    earth_distance =  42164, # in km
    cmb_temperature = 2.7, # in K
    rotation_period = 60, # in Sekunden für eine volle Umdrehung
)
emitted_power = calculate_IR_emitted_power(astronaut)
cmb_power = calculate_cmb_absorbed_power(astronaut, environment)

print(f"IR-Leistung: {emitted_power:.2f} W")
print(f"CMB-Leistung: {cmb_power:.12f} W")

#P_net = calculate_net_power(astronaut, environment)
#print(f"Nettoleistung: {P_net:.2f} W")
#change_rate = calculate_temperature_change(astronaut, environment)
#print(f"Temperaturaenderung: {change_rate:.12f} K/s")

#new_Tem = euler_step(astronaut, environment, 1)
#print(f"Neue Temperatur: {new_Tem:.5f} K")

#times, temperatures = run_simulation(astronaut, environment, 1, 60)
#print(f"Neue Temperatur Astronaut: {temperatures[-1]:.5f} K")

I_r = calculate_I_sun_distance(environment)
print(f"Sonnenintensität: {I_r:.5f} W/m^2 bei einem Abstand von {environment.sun_distance:.1f} AE")

P_sun = calculate_abs_sun_power(environment, astronaut)
print(f"Sonnenleistung ist: {P_sun:.5f} W")

IR_earth = calculate_IR_earth_distance(environment)
print(f"Erd IR Strahlung ist: {IR_earth:.5f} W/m^2 bei einem Abstand von {environment.earth_distance:.1f}")

P_IR_earth = calculate_abs_IR_earth_power(environment, astronaut)
print(f"IR-Erdstrahlung ist: {P_IR_earth:.5f} W")

P_albedo = calculate_abs_albedo_power(environment, astronaut)
print(f"Albedostrahlung: {P_albedo:.5f} W bei einem Abstand von {environment.earth_distance:.1f} km")
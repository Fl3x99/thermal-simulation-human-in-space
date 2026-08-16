from src.human import Human

stefan_boltzmann_konstante = 5.670374419e-8

def calculate_IR_emitted_power(human):

    IR_emitted_power = human.emissivity_ir*stefan_boltzmann_konstante*human.total_surface_area*human.temperature**4
    return IR_emitted_power

def calculate_cmb_absorbed_power(human,environment):

    cmb_absorbed_power = human.absorptivity_ir*stefan_boltzmann_konstante*human.total_surface_area*environment.cmb_temperature**4
    return cmb_absorbed_power


def calculate_I_sun_distance(environment):

    I_0 = 1361 # W/m^2, Sonnenstrahlungsleistung, auf höhe der Erde
    r_0 = 1 # AE, Abstand Sonne Erde
    r_1 = environment.sun_distance#in AE, gewünschter Abstand bei Simulation

    I=I_0*(r_0/r_1)**2
    return I


def calculate_abs_sun_power(environment, human):

    I_sun = calculate_I_sun_distance(environment)
    A_pro = human.front_projizierte_surface_area

    P_sun = I_sun*A_pro*human.absorptivity_sun
    return P_sun

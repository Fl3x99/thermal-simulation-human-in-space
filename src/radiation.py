
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

def calculate_IR_earth_distance(environment):

    I_earth_0 = 241 # W/m^2, Erd_IR Abstarhlungsiehe parameters
    r_0 = 6371 # km Erdradius
    r_1 = environment.earth_distance

    I_earth = I_earth_0 * (r_0/r_1)**2
    return I_earth

def calculate_abs_IR_earth_power(environment, human):
    IR_earth = calculate_IR_earth_distance(environment)
    A_pro = human.front_projizierte_surface_area

    P_earth = IR_earth * A_pro * human.absorptivity_ir
    return P_earth

def calculate_abs_albedo_power(environment, human):

    A_pro = human.front_projizierte_surface_area
    r_0 = 6371 # km wird als Referenzpunkt gewählt. tatsächliche Höhe der Rückstrahlung nicht genau bestimmbar
    r_1 = environment.earth_distance
    I_albedo_0 = 0.3 * calculate_I_sun_distance(environment)
    I_albedo_1 = I_albedo_0 * (r_0/r_1)**2

    P_albedo = A_pro * human.absorptivity_sun * I_albedo_1
    return P_albedo

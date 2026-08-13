stefan_boltzmann_konstante = 5.670374419e-8

def calculate_IR_emitted_power(human):

    IR_emitted_power = human.emissivity_ir*stefan_boltzmann_konstante*human.total_surface_area*human.temperature**4
    return IR_emitted_power

def calculate_cmb_absorbed_power(human,environment):

    cmb_absorbed_power = human.absorptivity_ir*stefan_boltzmann_konstante*human.total_surface_area*environment.cmb_temperature**4
    return cmb_absorbed_power
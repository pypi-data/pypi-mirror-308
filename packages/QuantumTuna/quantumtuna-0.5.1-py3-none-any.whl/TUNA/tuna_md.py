import tuna_optfreq as optfreq
import tuna_energy as energ
import numpy as np
from tuna_util import *


def calculate_accelerations(forces, inv_masses): 

    """

    Requires forces (array) and inverse masses (array).
    
    Returns accelerations (array).

    """

    return np.einsum("ij,i->ij", forces, inv_masses, optimize=True)



def calculate_kinetic_energy(masses, velocities): 
    
    """

    Requires masses (array) and velocities (array).
    
    Returns kinetic energy (float).

    """
    
    return 0.5 * np.einsum("i,ij->", masses, velocities ** 2, optimize=True)


def calculate_temperature(masses, velocities, degrees_of_freedom):

    """
    
    Requires masses (array), velocities (array) and degree of freedom (int).

    Calculates and returns temperature, using the equation from statistical mechanics by calculating kinetic energy,
    using a set number of degrees of freedom (6 for diatomics)
    """

    temperature = 2 * calculate_kinetic_energy(masses, velocities) / (degrees_of_freedom * constants.k)

    return temperature



def calculate_initial_velocities(masses, temperature, degrees_of_freedom):

    """

    Requires masses (array), temperature (float) and degrees of freedom (int).
    
    Creates velocities array in line with Maxwell-Boltzmann distribution and if a finite temperature has been specified, 
    removes linear component of momentum to avoid floating ice cube, recalculates temperature to rescale the velocities
    to be in line with the Maxwell-Boltzmann distrbution again.
    
    Returns velocities (array).
    
    """

    velocities = np.einsum("i,ij->ij", np.sqrt(constants.k * temperature / masses), np.random.normal(0,1,(2,3)))

    if temperature > 0:

        #Removes net linear momentum
        momenta = np.einsum("i,ij->j", masses, velocities)
        velocities -= momenta / np.sum(masses)

        #Calculates new temperature from kinetic energies after linear momentum has been removed
        temp = calculate_temperature(masses, velocities, degrees_of_freedom)

        #Rescales velocities
        velocities *= np.sqrt(temperature / temp)

    return velocities



def calculate_forces(coordinates, calculation, atoms, rotation_matrix):

    """

    Requires coordinates (array), calculation (Calculation object), atoms (list) and rotation matrix (array).
    
    Calculates the magnitude of the force and creates a 1D array, applying the force along the z axis. This is then rotated using the
    rotation matrix back to a 3D array to allow molecular rotations. The equal and opposite forces are applied to the other atom, in
    a forces array.
        
    Returns the 3D forces (array).
    
    """

    force = optfreq.calculate_gradient(coordinates, calculation, atoms, silent=True)

    force_array_1d = [0.0, 0.0, force]

    #Uses previsously determined rotation matrix to bring forces back to original coordinate system
    force_array_3d = np.dot(rotation_matrix.T, force_array_1d)

    #Applies equal and opposite to other atom
    forces = np.array([force_array_3d, -force_array_3d])


    return forces



def print_md_status(step, time, bond_length, temperature, potential_energy, kinetic_energy, total_energy, drift, calculation):

    """

    Requires step (int), time (float), bond length (float), temperature (float), potential energy (float), kinetic energy (float), total energy (float), 
    energy drift (float) and calculation (Calculation).
    
    Prints the MD data given in the input, using dynamic spaces to align the decimal point.
    
    """

    step_space = " " * (4 - len(str(step + 1)))
    time_space = " " * (6 - len(f"{time:.2f}"))
    post_time_space = " " 
    temp_space = " " * (8 - len(f"{temperature:.2f}"))
    drift_space = " " if drift >= 0 else ""

    #Keeps decimal points aligned
    log(f"   {step + 1}{step_space}{time_space} {time:.2f}{post_time_space}   {bond_length:.4f}      {temp_space}{temperature:.2f}       {potential_energy:.6f}      {kinetic_energy:.6f}      {total_energy:.6f}      {drift_space}{drift:.6f}", calculation, 1)



def calculate_md_components(molecule, masses, velocities, starting_energy, degrees_of_freedom, energy):

    """

    Requires molecule (Molecule), masses (array), velocities (array), starting energy (float), degrees of freedom (int) and energy (float).
    
    Calculates and returns potential energy (float), kinetic energy (float), their sum (float), temperature (float, via kinetic energies), 
    bond length (float) and the energy drift (float) from the start of the simulation.
    
    """

    #Potential energy of the nuclei is the total electronic energy, kinetic energy is calculated classically
    potential_energy = energy
    kinetic_energy = calculate_kinetic_energy(masses, velocities)

    total_energy = kinetic_energy + potential_energy

    temperature = calculate_temperature(masses, velocities, degrees_of_freedom)
    bond_length = bohr_to_angstrom(molecule.bond_length)

    #Unphysical change in total energy over course of simulation (lower for lower timestep)
    drift = total_energy - starting_energy 

    return potential_energy, kinetic_energy, total_energy, temperature, bond_length, drift



def run_md(calculation, atoms, coordinates):

    """
    
    Requires calculation (Calculation), atoms (array) and coordinates (array).
    
    Calculates and prints data from an ab initio molecular dynamics trajectory. In the main loop, energy is calculated, then forces, then accelerations. These
    are integrated by the Velocity Verlet algorithm into new velocities and positions, before energy is recalculated and the loop continues. The number of MD
    steps and the finite timestep are extracted from the calculation objects. A trajectory is printed by default to tuna-trajectory.xyz, and orbtials are read
    from the previous step. Temperature can be set to produce initial velocities.
    
    """

    time = 0

    #Linear molecules lose one rotational degree of freedom
    degrees_of_freedom = 5

    #Unpacks useful quantities from calculation object
    n_steps = calculation.md_number_of_steps
    timestep = calculation.timestep
    initial_temperature = calculation.temperature

    #Convert to atomic units from femtoseconds for integration
    timestep_au = timestep / constants.atomic_time_in_femtoseconds


    log(f"\nBeginning TUNA molecular dynamics calculation with {n_steps} steps in the NVE ensemble...\n", calculation, 1)
    log(f"Using timestep of {timestep:.3f} femtoseconds and initial temperature of {initial_temperature:.2f} K.", calculation, 1)

    #Prints trajectory to XYZ file by default, unless NOTRAJ keyword used
    if calculation.trajectory: 

        log("Printing trajectory data to \"tuna-trajectory.xyz\".", calculation, 1)

        #Clears and recreates output file
        open("tuna-trajectory.xyz", "w").close()


    log("\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", calculation, 1)
    log("  Step    Time    Distance    Temperature    Pot. Energy   Kin. Energy      Energy         Drift", calculation, 1)
    log(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", calculation, 1)

    #Remains silent to prevent too much printing, just prints to table
    scf_output, molecule, energy, _ = energ.calculate_energy(calculation, atoms, coordinates, silent=True)

    #Calculates inverse mass array for acceleration calculation
    masses = molecule.masses
    inv_masses = 1 / masses

    #Calculates forces without rotation, so uses identity matrix as rotation matrix
    forces = calculate_forces(coordinates, calculation, atoms, np.eye(3))
    accelerations = calculate_accelerations(forces, inv_masses) 
    velocities = calculate_initial_velocities(masses, initial_temperature, degrees_of_freedom)

    #Total energy of molecule is nuclear potential energy (electronic total energy) and classically calculated kinetic energy
    initial_energy = energy + calculate_kinetic_energy(masses, velocities)

    #Calculates various energy components and MD quantities, then prints these
    potential_energy, kinetic_energy, total_energy, temperature, bond_length, drift = calculate_md_components(molecule, masses, velocities, initial_energy, degrees_of_freedom, energy)
    print_md_status(0, time, bond_length, temperature, potential_energy, kinetic_energy, total_energy, drift, calculation)

    #Iterates over MD steps, up to the number of steps specified, in MD simulation
    for i in range(1, n_steps):

        #Velocity Verlet algorithm with finite timestep, accelerations are recalculated halfway through to allow simultaneous calculation of velocities
        coordinates += velocities * timestep_au + 0.5 * accelerations * timestep_au ** 2

        #Optional (default) reading in of orbitals from previous MD step
        if calculation.moread: 
            
            P_guess = scf_output.P; 
            P_guess_alpha = scf_output.P_alpha
            P_guess_beta = scf_output.P_beta
            E_guess = scf_output.energy

        else: 
            
            P_guess = None
            P_guess_alpha = None
            P_guess_beta = None
            E_guess = None


        #Defines a 3D vector of the differences between atomic positions to rotate to the z axis
        difference_vector = np.array([coordinates[0][0] - coordinates[1][0], coordinates[0][1] - coordinates[1][1], coordinates[0][2] - coordinates[1][2]])

        #Rotate the difference vector so it lies along the z axis only
        difference_vector_rotated, rotation_matrix = rotate_coordinates_to_z_axis(difference_vector)
        aligned_coordinates = np.array([[0.0, 0.0, 0.0], -1 * difference_vector_rotated])

        #Additional print makes a big mess - prints all energy calculations to console
        scf_output, molecule, energy, _ = energ.calculate_energy(calculation, atoms, aligned_coordinates, P_guess=P_guess, E_guess=E_guess, P_guess_alpha=P_guess_alpha, P_guess_beta=P_guess_beta, silent=not(calculation.additional_print))  

        forces = calculate_forces(aligned_coordinates, calculation, atoms, rotation_matrix)

        accelerations_new = calculate_accelerations(forces, inv_masses) 
        velocities += 0.5 * timestep_au * (accelerations + accelerations_new) 

        #Updates accelerations and increments timestep
        accelerations = accelerations_new
        time += timestep

        #Cycle begins again as new energy components are printed
        potential_energy, kinetic_energy, total_energy, temperature, bond_length, drift = calculate_md_components(molecule, masses, velocities, initial_energy, degrees_of_freedom, energy)
        print_md_status(i, time, bond_length, temperature, potential_energy, kinetic_energy, total_energy, drift, calculation)

        #By default prints trajectory to file, can be viewed with Jmol
        if calculation.trajectory: optfreq.print_trajectory(molecule, potential_energy, coordinates)
        


    log(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", calculation, 1)


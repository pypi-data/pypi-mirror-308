# Changelog

## TUNA 0.5.1  —  14/11/2024

### Added

- Keyword for the default Hessian used in geometry optimisations, `DEFAULTHESS`
- Keyword for the maximum step size for geometry optimisations, `MAXSTEP`
- Optional parameter can be used with the `LEVELSHIFT` keyword to adjust the degree of level shift

### Changed

- Improved logging to console for a more consistent user experience
- Molecular dynamics simulations now read in the density matrix from the previous step by default
- Refactored and optimised all the code, ready for future updates and added comments and docstrings
- Separated two- and three-dimensional plotting functions into new tuna_plot module
- Keyword for the angle with which to rotate orbitals for initial guess, `THETA` has been removed and replaced by `ROTATE [ANGLE]`
- Reading in orbitals from previous coordinate scan step now turned off by default for UHF calculations

### Fixed

- Point group and molecular structure are now detected correctly for ghost atom calculations
- Nuclear repulsion energy is now not calculated for ghost atoms
- Individual energy components now work correctly for UHF energies
- Removed Koopmans' theorem parameter calculations for UHF references
- Molecular orbital eigenvalues and coefficients are now printed correctly for UHF, split into alpha and beta orbitals
- Stopped reading in orbitals for one-electron systems in coordinate scans, as there is no SCF cycle
- Orbitals are now rotated correctly by the requested angle for UHF initial guesses
- DIIS for UHF now works as intended when the equations can't be solved

<br>

## TUNA 0.5.0  —  21/09/2024

### Added

- *Ab initio* molecular dynamics
- Unrestricted Hartree--Fock energy and density
- Unrestricted MP2 energies
- Restricted and unrestricted MP3 energies
- Spin-component-scaled MP3 energies
- Keyword to decontract basis functions, `DECONTRACT`
- New basis sets: 4-31G, 6-31+G, 6-31++G, and 6-311+G
- Mayer bond order, free and total valences
- Spin contamination for UHF calculations
- Orbital rotation and `ROTATE` and `NOROTATE` keywords for UHF guess density
- Optimisations and molecular dynamics simulations optionally print to XYZ file with `TRAJ` and `NOTRAJ` keywords
- Option to optimize to a maximum with `OPTMAX` keyword
- Terminal output now has colour for warning and errors
- Increased speed of all TUNA calculations by 50–95% through making full use of permutational symmetry in the two-electron integrals
- Much better error handling and clear errors and warnings
- New changelog, manual, GitHub and PyPI pages 
- TUNA can now be installed simply by `pip install QuantumTUNA`

### Changed

- Rewrote all the code to make things object-oriented, improve efficiency and reduce redundancy
- Slimmed down the fish logo :(
- Optimised and simplified integral engine
- Reduced default SCF and optimisation convergence criteria by fixing associated bug
- Better handling of print levels; optimizations now only calculate properties at the end by default
- Now use more energy evaluations for gradients and Hessians, making them more robust but slower 
- Generally refined the output, making information more precise and clear

### Fixed

- When its equations can't be solved, DIIS now resets instead of crashing the program
- Fixed frequency calculations being far too sensitive to SCF convergence when guess density was read in
- SCF convergence was checking that DeltaE was less than the criteria, rather than its magnitude leading to too early convergence
- Fixed the thermochemistry module mixing up the temperature and pressure variables
- Formatting issues with population analysis
- Fixed handling of ghost atoms, accessible by `XH` or `XHe`

<br>

## TUNA 0.4.0 

### Added

- Fock matrix extrapolation for SCF convergence (DIIS)
- Electronic and total dipole moment
- Unrelaxed MP2 density and natural orbitals
- Thermochemistry after frequency calculations, `TEMPERATURE` and `PRESSURE` keywords
- New 3-21G basis set

### Changed

- Density matrix is now read by default from previous step in coordinate scans and optimisations

### Fixed

- Unbroke level shift, added keywords

<br>

## TUNA 0.3.0

### Added

- Geometry optimisations
- Harmonic frequencies, optionally linked with prior optimisation with `OPTFREQ` calculation type
- Rotational constants
- Nuclear dipole moment
- Optional exact or approximate (default) Hessian for optimisation
- Keywords for geometry convergence tolerance and maximum iterations
- High static damping option for difficult SCF convergence cases, `SLOWCONV`

<br>

## TUNA 0.2.0

### Added

- Conventional and spin-component-scaled MP2
- Mulliken and Löwdin population analysis
- Keywords for additional print, `P`, and SCF damping, `DAMP`
- Identification of point group

### Changes

- Updated to Python 3.12
- Significantly increased integral efficiency using vectorised operations

<br>

## TUNA 0.1.0

### Added

- Restricted Hartree–Fock
- Single point energy and coordinate scans
- New basis sets: STO-3G, STO-6G, 6-31G, 6-311G, 6-311++G
- Dynamic damping and level shift
- Ghost atoms
- Molecular orbitals and energies, Koopman's theorem parameters
- Electron density 3D plots
- Dispersion correction with semi-empirical D2 scheme
- Convergence criteria keywords for SCF
- Interface with matplotlib for coordinate scan via `SCANPLOT` keyword

import math

# --- Physics Constants & Scaling ---
l0 = 2.0 * math.pi      # Laser Wavelength
t0 = 2.0 * math.pi      # Laser Period
back_vacuum = 10.0 * l0 
plasma_length = 30.0 * l0
total_cells = 1536

# --- Main Simulation Box ---
Main(
    geometry = "1Dcartesian",
    interpolation_order = 2,
    cell_length = [l0 / 30.0], 
    grid_length = [total_cells * (l0 / 30.0)],
    timestep = 0.95 * (l0 / 30.0), 
    simulation_time = 60.0 * t0,
    
    number_of_patches = [16], 
    EM_boundary_conditions = [["silver-muller", "silver-muller"]],
)

# --- THE GEOMETRY-SPECIFIC ENVELOPE (Everything in one block) ---
LaserEnvelopePlanar1D(
    # Solver & Boundary Parameters
    envelope_solver = "explicit",
    Envelope_boundary_conditions = [["reflective", "reflective"]], 
    
    # Pulse Profile Parameters
    a0 = 1.0,
    omega = 1.0,
    polarization_phi = 0.0,
    time_envelope = tgaussian(fwhm=4.0*t0, center=5.0*l0)
)

# --- Plasma Electrons ---
Species(
    name = "electron",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = 20,
    mass = 1.0,
    charge = -1.0,
    number_density = trapezoidal(0.01, xvacuum=back_vacuum, xplateau=plasma_length),
    boundary_conditions = [["remove", "remove"]],
    pusher = "ponderomotive_boris", 
)

# --- Plasma Ions ---
Species(
    name = "ion",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = 20,
    mass = 1836.0, 
    charge = 1.0,           
    number_density = trapezoidal(0.01, xvacuum=back_vacuum, xplateau=plasma_length),
    boundary_conditions = [["remove", "remove"]],
    pusher = "ponderomotive_boris",
)

# --- Field Diagnostics ---
DiagFields(
    every = 2 * t0,
    fields = ["Ex", "Env_E_abs", "Rho_electron"] 
)

# Python Finite-Difference Hopf Index Calculation

This package provides Python implementations of the calculation of the Hopf index of the magnetisation texture for finite-difference micromagnetic simulations. The four methods implemented are `twopointstencil`, `fivepointstencil`, `solidangle`, and `solidanglefourier`. The package assumes NumPy arrays of the shape `(Nx, Ny, Nz, 3)`, where $N_i$ are the number of cells in each direction, and the final dimension is for the three components. It is assumed that the vector field is normalised.

Example usage to calculate the Hopf index, Hopf density $\boldsymbol{F} \cdot \boldsymbol{A}$, and emergent magnetic field of a vector field stored in a file `Magnetisation.npy` using the solid angle method is shown in the following.

```python
from pyhopf.hopfindex import HopfIndexCalculator

m = np.load('Magnetisation.npy')

hopf_index_calculator = HopfIndexCalculator(m, 'solidangle')
hopf_index            = hopf_index_calculator.hopf_index()
hopf_density          = hopf_index_calculator.hopf_density()
emergent_field        = hopf_index_calculator.emergent_field()
```

import numpy as np
import warnings


class HopfIndexCalculator:

    """
    Class to calculate the Hopf index of a vector field using various methods.
    
    Parameters:
        m (np.ndarray): Vector field array of shape (Nx, Ny, Nz, 3).
        method_name (str): Method to use for the calculation. Options are:
                           'twopointstencil', 'fivepointstencil', 'solidangle', 'solidanglefourier'.
        Delta_x (float, optional): Grid spacing in the x-direction. Default is 1.0.
        Delta_y (float, optional): Grid spacing in the y-direction. Default is 1.0.
        Delta_z (float, optional): Grid spacing in the z-direction. Default is 1.0.
    
    Raises:
        ValueError: If the method_name is not a valid option or if `m` is not a 4D array with a shape of (Nx, Ny, Nz, 3).
    """

    def __init__(self, m, method_name, Delta_x=1.0, Delta_y=1.0, Delta_z=1.0):
        self.m      = m
        self.method_name = method_name
        self.Delta_x = Delta_x
        self.Delta_y = Delta_y
        self.Delta_z = Delta_z

        if method_name not in ['twopointstencil', 'fivepointstencil', 'solidangle', 'solidanglefourier']:
            raise ValueError('Method must be one of twopointstencil, fivepointstencil, solidangle, or solidanglefourier')

        if len(m.shape) != 4 or m.shape[3] != 3:
            raise ValueError('Vector field must be array of shape (Nx x Ny x Nz x 3)')


    def hopf_index(self):
        """
        Calculate the Hopf index based on the selected method.

        Returns:
            float: Hopf index value.
        """
        if self.method_name == 'solidanglefourier':
            return self._hopf_index_solid_angle_fourier()

        else:
            return -self.Delta_x * self.Delta_y * self.Delta_z * np.sum(self.hopf_density())


    def hopf_density(self):
        """
        Calculate the Hopf density for real-space methods.

        Returns:
            np.ndarray: Array representing Hopf density.

        Raises:
            ValueError: If the calculation is attempted with 'solidanglefourier' method.
        """
        if self.method_name == 'solidanglefourier':
            raise ValueError('Hopf density calculation only available for real-space methods.')

        else:
            F = self.emergent_field()
            A = self._vector_potential(F)
            return np.einsum('ijkl,ijkl->ijk', F, A)


    def emergent_field(self):
        """
        Compute the emergent field using the specified method.

        Returns:
            np.ndarray: Array representing the emergent field.

        Raises:
            ValueError: If method 'solidanglefourier' is used but emergent_field calculation is attempted.
        """
        if self.method_name == 'solidanglefourier':
            raise ValueError('Emergent field calculation only available for real-space methods.')

        else:

            # Mapping method names to their corresponding functions
            emergent_field_methods = {
                'twopointstencil'   : self._emergent_field_two_point_stencil,
                'fivepointstencil'  : self._emergent_field_five_point_stencil,
                'solidangle'        : self._emergent_field_solid_angle,
            }

            return emergent_field_methods[self.method_name]()


    def _vector_potential(self, F):

        A = np.zeros_like(self.m, dtype=float)
        A[:, :, :, 0] = -np.cumsum(F[:, :, :, 2], axis=1) * self.Delta_y  # Approximate integral as cumulative sum along y-axis
        A[:, :, :, 2] =  np.cumsum(F[:, :, :, 0], axis=1) * self.Delta_y
        return A


    def _emergent_field_two_point_stencil(self):

        # Define m at position i+1, j+1 and so on, where i, j, k are indices along x, y, and z-axes
        m_ip1 = np.roll(self.m, -1, axis=0)
        m_im1 = np.roll(self.m, 1, axis=0)
        m_jp1 = np.roll(self.m, -1, axis=1)
        m_jm1 = np.roll(self.m, 1, axis=1)
        m_kp1 = np.roll(self.m, -1, axis=2)
        m_km1 = np.roll(self.m, 1, axis=2)

        # Central difference derivatives
        dm_dx = 0.5 * (m_ip1 - m_im1)
        dm_dy = 0.5 * (m_jp1 - m_jm1)
        dm_dz = 0.5 * (m_kp1 - m_km1)

        # At boundaries, do forward and backward difference
        dm_dx[ 0, :, :, :] = m_ip1[0, :, :, :] - self.m[0, :, :, :]
        dm_dx[-1, :, :, :] = self.m[-1, :, :, :] - m_im1[-1, :, :, :]
        dm_dy[:,  0, :, :] = m_jp1[:, 0, :, :] - self.m[:, 0, :, :]
        dm_dy[:, -1, :, :] = self.m[:, -1, :, :] - m_jm1[:, -1, :, :]
        dm_dz[:, :,  0, :] = m_kp1[:, :, 0, :] - self.m[:, :, 0, :]
        dm_dz[:, :, -1, :] = self.m[:, -1, :, :] - m_km1[:, :, -1, :]

        F = np.zeros_like(self.m, dtype=float)
        F[:, :, :, 0] = 2 * np.einsum('ijkl,ijkl->ijk', self.m, np.cross(dm_dy, dm_dz, axis=-1)) / (8*np.pi * self.Delta_y * self.Delta_z)
        F[:, :, :, 1] = 2 * np.einsum('ijkl,ijkl->ijk', self.m, np.cross(dm_dz, dm_dx, axis=-1)) / (8*np.pi * self.Delta_z * self.Delta_x)
        F[:, :, :, 2] = 2 * np.einsum('ijkl,ijkl->ijk', self.m, np.cross(dm_dx, dm_dy, axis=-1)) / (8*np.pi * self.Delta_x * self.Delta_y)

        return F


    def _emergent_field_five_point_stencil(self):

        Nx, Ny, Nz, _ = self.m.shape

        # Throw an exception if there are fewer than five cells.
        # This is because it would require extra handling of the calculation of the
        # derivatives in the five-point stencil, but given that a hopfion is a bulk
        # texture anyway, it probably doesn't make so much sense to handle this case.
        # For the handling in the case of fewer than five cells, see my MuMax implemenation.
        if Nx < 5 or Ny < 5 or Nz < 5:
            raise ValueError('Must have at least five cells in each direction.')

        # Define m at position i+1, i+2, j+1 and so on, where i, j, k are indices along x, y, and z-axes
        m_ip1 = np.roll(self.m, -1, axis=0)
        m_im1 = np.roll(self.m,  1, axis=0)
        m_jp1 = np.roll(self.m, -1, axis=1)
        m_jm1 = np.roll(self.m,  1, axis=1)
        m_kp1 = np.roll(self.m, -1, axis=2)
        m_km1 = np.roll(self.m,  1, axis=2)
        m_ip2 = np.roll(self.m, -2, axis=0)
        m_im2 = np.roll(self.m,  2, axis=0)
        m_jp2 = np.roll(self.m, -2, axis=1)
        m_jm2 = np.roll(self.m,  2, axis=1)
        m_kp2 = np.roll(self.m, -2, axis=2)
        m_km2 = np.roll(self.m,  2, axis=2)

        # Central difference derivatives
        dm_dx = (2. / 3.) * (m_ip1 - m_im1) + (1. / 12.) * (m_im2 - m_ip2)
        dm_dy = (2. / 3.) * (m_jp1 - m_jm1) + (1. / 12.) * (m_jm2 - m_jp2)
        dm_dz = (2. / 3.) * (m_kp1 - m_km1) + (1. / 12.) * (m_km2 - m_kp2)

        # Forward/backward differences for points at very edge
        dm_dx[ 0, :, :, :] = -0.5 * m_ip2[ 0, :, :, :] + 2.0 * m_ip2[ 0, :, :, :] - 1.5 * self.m[ 0, :, :, :]
        dm_dx[-1, :, :, :] =  0.5 * m_im2[-1, :, :, :] - 2.0 * m_im1[-1, :, :, :] + 1.5 * self.m[-1, :, :, :]
        dm_dy[:,  0, :, :] = -0.5 * m_jp2[:,  0, :, :] + 2.0 * m_jp2[:,  0, :, :] - 1.5 * self.m[:,  0, :, :]
        dm_dy[:, -1, :, :] =  0.5 * m_jm2[:, -1, :, :] - 2.0 * m_jm1[:, -1, :, :] + 1.5 * self.m[:, -1, :, :]
        dm_dz[:, :,  0, :] = -0.5 * m_kp2[:, :,  0, :] + 2.0 * m_kp2[:, :,  0, :] - 1.5 * self.m[:, :,  0, :]
        dm_dz[:, :, -1, :] =  0.5 * m_km2[:, :, -1, :] - 2.0 * m_km1[:, :, -1, :] + 1.5 * self.m[:, :, -1, :]

        # Central differences for points once cell away from the edge
        dm_dx[ 1, :, :, :] = 0.5 * (m_ip1[ 1, :, :, :] - m_im1[ 1, :, :, :])
        dm_dx[-2, :, :, :] = 0.5 * (m_ip1[-2, :, :, :] - m_im1[-2, :, :, :])
        dm_dy[:,  1, :, :] = 0.5 * (m_jp1[:,  1, :, :] - m_jm1[:,  1, :, :])
        dm_dy[:, -2, :, :] = 0.5 * (m_jp1[:, -2, :, :] - m_jm1[:, -2, :, :])
        dm_dz[:, :,  1, :] = 0.5 * (m_kp1[:, :,  1, :] - m_km1[:, :,  1, :])
        dm_dz[:, :, -2, :] = 0.5 * (m_kp1[:, :, -2, :] - m_km1[:, :, -2, :])

        F = np.zeros_like(self.m, dtype=float)
        F[:, :, :, 0] = 2 * np.einsum('ijkl,ijkl->ijk', self.m, np.cross(dm_dy, dm_dz, axis=-1)) / (8*np.pi * self.Delta_y * self.Delta_z)
        F[:, :, :, 1] = 2 * np.einsum('ijkl,ijkl->ijk', self.m, np.cross(dm_dz, dm_dx, axis=-1)) / (8*np.pi * self.Delta_z * self.Delta_x)
        F[:, :, :, 2] = 2 * np.einsum('ijkl,ijkl->ijk', self.m, np.cross(dm_dx, dm_dy, axis=-1)) / (8*np.pi * self.Delta_x * self.Delta_y)

        return F

    
    def _triangle_charge(self, mi, mj, mk):

        numerator = np.einsum('ijkl,ijkl->ijk', mi, np.cross(mj, mk, axis=-1))
        denominator = 1.0 + np.einsum('ijkl,ijkl->ijk', mi, mj) + np.einsum('ijkl,ijkl->ijk', mi, mk) + np.einsum('ijkl,ijkl->ijk', mj, mk)
        return 2.0 * np.arctan2(numerator, denominator)


    def _emergent_field_solid_angle(self):

        # MuMax deals with non-cuboidal geometries by still defining a cuboidal grid, but setting |m| = 0 outside of the geometry
        if np.any(np.isclose(np.linalg.norm(self.m, axis=3), 0.)):
            warnings.warn('It looks like you are using a non-cuboidal geometry. This package does not fully handle the weights for missing next-nearest neighbours as described in Joo-Von Kim and Jeroen Mulkers 2020 IOPSciNotes 1 025211; please ensure that your hopfion texture is far from the boundaries.')

        # Define neighbours, e.g. m_ip1 is one to the right (in x), m_km1 is one below (in z)
        m_ip1 = np.roll(self.m, -1, axis=0)
        m_im1 = np.roll(self.m,  1, axis=0)
        m_jp1 = np.roll(self.m, -1, axis=1)
        m_jm1 = np.roll(self.m,  1, axis=1)
        m_kp1 = np.roll(self.m, -1, axis=2)
        m_km1 = np.roll(self.m,  1, axis=2)

        Fx  = 0.5 * self._triangle_charge(self.m, m_jp1, m_kp1)  # Upper-right triangle
        Fx += 0.5 * self._triangle_charge(self.m, m_kp1, m_jm1)  # Upper-left
        Fx += 0.5 * self._triangle_charge(self.m, m_jm1, m_km1)  # Lower-left
        Fx += 0.5 * self._triangle_charge(self.m, m_km1, m_jp1)  # Lower-right

        Fy  = 0.5 * self._triangle_charge(self.m, m_kp1, m_ip1)
        Fy += 0.5 * self._triangle_charge(self.m, m_ip1, m_km1)
        Fy += 0.5 * self._triangle_charge(self.m, m_km1, m_im1)
        Fy += 0.5 * self._triangle_charge(self.m, m_im1, m_kp1)

        Fz  = 0.5 * self._triangle_charge(self.m, m_ip1, m_jp1)
        Fz += 0.5 * self._triangle_charge(self.m, m_jp1, m_im1)
        Fz += 0.5 * self._triangle_charge(self.m, m_im1, m_jm1)
        Fz += 0.5 * self._triangle_charge(self.m, m_jm1, m_ip1)

        Fx *= 2 / (8*np.pi * self.Delta_y * self.Delta_z)
        Fy *= 2 / (8*np.pi * self.Delta_x * self.Delta_z)
        Fz *= 2 / (8*np.pi * self.Delta_x * self.Delta_y)

        F = np.zeros_like(self.m, dtype=float)
        F[:, :, :, 0] = Fx
        F[:, :, :, 1] = Fy
        F[:, :, :, 2] = Fz

        return F

    
    def _hopf_index_solid_angle_fourier(self):

        F = self._emergent_field_solid_angle()

        F[:, :, :, 0] *= self.Delta_y * self.Delta_z
        F[:, :, :, 1] *= self.Delta_x * self.Delta_z
        F[:, :, :, 2] *= self.Delta_x * self.Delta_y

        Nx, Ny, Nz, _ = F.shape

        kx = np.fft.fftfreq(Nx)
        ky = np.fft.fftfreq(Ny)
        kz = np.fft.fftfreq(Nz)

        KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
        K = np.zeros((Nx, Ny, Nz, 3))
        K[:, :, :, 0] = KX
        K[:, :, :, 1] = KY
        K[:, :, :, 2] = KZ

        Fx_k = np.fft.fftn(F[:, :, :, 0])
        Fy_k = np.fft.fftn(F[:, :, :, 1])
        Fz_k = np.fft.fftn(F[:, :, :, 2])

        F_k = np.zeros((Nx, Ny, Nz, 3), dtype=np.complex_)
        F_k[:, :, :, 0] = Fx_k
        F_k[:, :, :, 1] = Fy_k
        F_k[:, :, :, 2] = Fz_k

        F_mk = np.conj(F_k)

        # Elementwise dot product
        k2 = np.einsum('ijkl,ijkl->ijk', K, K)

        summand = np.einsum('ijkl,ijkl->ijk', F_mk, np.cross(K, F_k, axis=-1)) / k2
        summand[np.where(np.isclose(k2, 0.0))] = 0

        return np.imag(np.sum(summand)) / (2*np.pi * Nx*Ny*Nz)

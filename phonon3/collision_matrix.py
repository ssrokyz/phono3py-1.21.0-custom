# Copyright (C) 2020 Atsushi Togo
# All rights reserved.
#
# This file is part of phono3py.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name of the phonopy project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import numpy as np
from phonopy.units import THzToEv, Kb
from phonopy.harmonic.force_constants import similarity_transformation
from phono3py.phonon3.imag_self_energy import ImagSelfEnergy


class CollisionMatrix(ImagSelfEnergy):
    """
    Main diagonal part (imag-self-energy) and
    the other part are separately stored.
    """
    def __init__(self,
                 interaction,
                 point_operations=None,
                 ir_grid_points=None,
                 rot_grid_points=None,
                 temperature=None,
                 sigma=None,
                 is_reducible_collision_matrix=False,
                 log_level=0,
                 lang='C'):
        self._pp = None
        self._sigma = None
        self._frequency_points = None
        self._temperature = None
        self._grid_point = None
        self._lang = None
        self._imag_self_energy = None
        self._collision_matrix = None
        self._pp_strength = None
        self._frequencies = None
        self._triplets_at_q = None
        self._triplets_map_at_q = None
        self._weights_at_q = None
        self._band_indices = None
        self._unit_conversion = None
        self._cutoff_frequency = None
        self._g = None
        self._mesh = None
        self._is_collision_matrix = None
        self._unit_conversion = None
        self._log_level = log_level

        ImagSelfEnergy.__init__(self,
                                interaction,
                                temperature=temperature,
                                sigma=sigma,
                                lang=lang)

        self._is_reducible_collision_matrix = is_reducible_collision_matrix
        self._is_collision_matrix = True

        if not self._is_reducible_collision_matrix:
            self._ir_grid_points = ir_grid_points
            self._rot_grid_points = rot_grid_points
            self._point_operations = point_operations
            self._primitive = self._pp.primitive
            rec_lat = np.linalg.inv(self._primitive.cell)
            self._rotations_cartesian = np.array(
                [similarity_transformation(rec_lat, r)
                 for r in self._point_operations], dtype='double', order='C')

    def run(self):
        if self._pp_strength is None:
            self.run_interaction()

        num_band0 = self._pp_strength.shape[1]
        num_band = self._pp_strength.shape[2]
        self._imag_self_energy = np.zeros(num_band0, dtype='double')

        if self._is_reducible_collision_matrix:
            num_mesh_points = np.prod(self._mesh)
            self._collision_matrix = np.zeros(
                (num_band0, num_mesh_points, num_band), dtype='double')
        else:
            self._collision_matrix = np.zeros(
                (num_band0, 3, len(self._ir_grid_points), num_band, 3),
                dtype='double')
        self._run_with_band_indices()
        self._run_collision_matrix()

    def get_collision_matrix(self):
        return self._collision_matrix

    def set_grid_point(self, grid_point=None):
        if grid_point is None:
            self._grid_point = None
        else:
            self._pp.set_grid_point(grid_point, stores_triplets_map=True)
            self._pp_strength = None
            (self._triplets_at_q,
             self._weights_at_q,
             self._triplets_map_at_q,
             self._ir_map_at_q) = self._pp.get_triplets_at_q()
            self._grid_address = self._pp.grid_address
            self._grid_point = grid_point
            self._bz_map = self._pp.bz_map
            self._frequencies, self._eigenvectors, _ = self._pp.get_phonons()

    def _run_collision_matrix(self):
        self._run_with_band_indices()
        if self._temperature > 0:
            if self._lang == 'C':
                if self._is_reducible_collision_matrix:
                    self._run_c_reducible_collision_matrix()
                else:
                    self._run_c_collision_matrix()
            else:
                if self._is_reducible_collision_matrix:
                    self._run_py_reducible_collision_matrix()
                else:
                    self._run_py_collision_matrix()

    def _run_c_collision_matrix(self):
        import phono3py._phono3py as phono3c
        phono3c.collision_matrix(self._collision_matrix,
                                 self._pp_strength,
                                 self._frequencies,
                                 self._g,
                                 self._triplets_at_q,
                                 self._triplets_map_at_q,
                                 self._ir_map_at_q,
                                 self._rot_grid_points,
                                 self._rotations_cartesian,
                                 self._temperature,
                                 self._unit_conversion,
                                 self._cutoff_frequency)

    def _run_c_reducible_collision_matrix(self):
        import phono3py._phono3py as phono3c
        phono3c.reducible_collision_matrix(self._collision_matrix,
                                           self._pp_strength,
                                           self._frequencies,
                                           self._g,
                                           self._triplets_at_q,
                                           self._triplets_map_at_q,
                                           self._ir_map_at_q,
                                           self._temperature,
                                           self._unit_conversion,
                                           self._cutoff_frequency)

    def _run_py_collision_matrix(self):
        num_band0 = self._pp_strength.shape[1]
        num_band = self._pp_strength.shape[2]
        gp2tp_map = self._get_gp2tp_map()

        for i, ir_gp in enumerate(self._ir_grid_points):
            r_gps = self._rot_grid_points[i]
            for r, r_gp in zip(self._rotations_cartesian, r_gps):
                ti = gp2tp_map[self._triplets_map_at_q[r_gp]]
                inv_sinh = self._get_inv_sinh(r_gp, gp2tp_map)

                for j in range(num_band0):
                    for k in range(num_band):
                        collision = (self._pp_strength[ti, j, k]
                                     * inv_sinh
                                     * self._g[2, ti, j, k]).sum()
                        collision *= self._unit_conversion
                        self._collision_matrix[j, :, i, k, :] += collision * r

    def _run_py_reducible_collision_matrix(self):
        num_mesh_points = np.prod(self._mesh)
        num_band0 = self._pp_strength.shape[1]
        num_band = self._pp_strength.shape[2]
        gp2tp_map = self._get_gp2tp_map()

        for i in range(num_mesh_points):
            ti = gp2tp_map[self._triplets_map_at_q[i]]
            inv_sinh = self._get_inv_sinh(i, gp2tp_map)
            for j, k in list(np.ndindex((num_band0, num_band))):
                collision = (self._pp_strength[ti, j, k]
                             * inv_sinh
                             * self._g[2, ti, j, k]).sum()
                collision *= self._unit_conversion
                self._collision_matrix[j, i, k] += collision

    def _get_gp2tp_map(self):
        gp2tp_map = {}
        count = 0
        for i, j in enumerate(self._triplets_map_at_q):
            if i == j:
                gp2tp_map[i] = count
                count += 1

        return gp2tp_map

    def _get_inv_sinh(self, gp, gp2tp_map):
        ti = gp2tp_map[self._triplets_map_at_q[gp]]
        tp = self._triplets_at_q[ti]
        if self._triplets_map_at_q[gp] == self._ir_map_at_q[gp]:
            gp2 = tp[2]
        else:
            gp2 = tp[1]
        freqs = self._frequencies[gp2]
        sinh = np.where(
            freqs > self._cutoff_frequency,
            np.sinh(freqs * THzToEv / (2 * Kb * self._temperature)),
            -1.0)
        inv_sinh = np.where(sinh > 0, 1.0 / sinh, 0)

        return inv_sinh

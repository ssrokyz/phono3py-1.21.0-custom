# Copyright (C) 2015 Atsushi Togo
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
from phonopy.cui.settings import Settings, ConfParser, fracval


class Phono3pySettings(Settings):
    _default = {
        # In micrometre. The default value is just set to avoid divergence.
        'boundary_mfp': 1.0e6,
        'coarse_mesh_shifts': None,
        'constant_averaged_pp_interaction': None,
        'create_forces_fc2': None,
        'create_forces_fc3': None,
        'create_forces_fc3_file': None,
        'cutoff_fc3_distance': None,
        'cutoff_pair_distance': None,
        'gamma_conversion_factor': None,
        'grid_addresses': None,
        'grid_points': None,
        'ion_clamped': False,
        'is_bterta': False,
        'is_compact_fc': False,
        'is_full_pp': False,
        'is_gruneisen': False,
        'is_imag_self_energy': False,
        'is_isotope': False,
        'is_joint_dos': False,
        'is_kappa_star': True,
        'is_lbte': False,
        'is_N_U': False,
        'is_real_self_energy': False,
        'is_reducible_collision_matrix': False,
        'is_spectral_function': False,
        'is_symmetrize_fc2': False,
        'is_symmetrize_fc3_q': False,
        'is_symmetrize_fc3_r': False,
        'lapack_zheev_uplo': 'L',
        'mass_variances': None,
        'max_freepath': None,
        'mesh_divisors': None,
        'num_points_in_batch': None,
        'read_collision': None,
        'read_fc2': False,
        'read_fc3': False,
        'read_gamma': False,
        'read_phonon': False,
        'read_pp': False,
        'phonon_supercell_matrix': None,
        'pinv_cutoff': 1.0e-8,
        'pinv_solver': 0,
        'pp_conversion_factor': None,
        'scattering_event_class': None,  # scattering event class 1 or 2
        'sigma_cutoff_width': None,
        'solve_collective_phonon': False,
        'subtract_forces': None,
        'use_ave_pp': False,
        'write_collision': False,
        'write_gamma_detail': False,
        'write_gamma': False,
        'write_phonon': False,
        'write_pp': False,
        'write_LBTE_solution': False
    }

    def __init__(self, default=None):
        Settings.__init__(self)
        self._v.update(Phono3pySettings._default.copy())
        if default is not None:
            self._v.update(default)

    def set_boundary_mfp(self, val):
        self._v['boundary_mfp'] = val

    def set_coarse_mesh_shifts(self, val):
        self._v['coarse_mesh_shifts'] = val

    def set_constant_averaged_pp_interaction(self, val):
        self._v['constant_averaged_pp_interaction'] = val

    def set_create_forces_fc2(self, val):
        self._v['create_forces_fc2'] = val

    def set_create_forces_fc3(self, val):
        self._v['create_forces_fc3'] = val

    def set_create_forces_fc3_file(self, val):
        self._v['create_forces_fc3_file'] = val

    def set_cutoff_fc3_distance(self, val):
        self._v['cutoff_fc3_distance'] = val

    def set_cutoff_pair_distance(self, val):
        self._v['cutoff_pair_distance'] = val

    def set_gamma_conversion_factor(self, val):
        self._v['gamma_conversion_factor'] = val

    def set_grid_addresses(self, val):
        self._v['grid_addresses'] = val

    def set_grid_points(self, val):
        self._v['grid_points'] = val

    def set_ion_clamped(self, val):
        self._v['ion_clamped'] = val

    def set_is_bterta(self, val):
        self._v['is_bterta'] = val

    def set_is_compact_fc(self, val):
        self._v['is_compact_fc'] = val

    def set_is_full_pp(self, val):
        self._v['is_full_pp'] = val

    def set_is_gruneisen(self, val):
        self._v['is_gruneisen'] = val

    def set_is_imag_self_energy(self, val):
        self._v['is_imag_self_energy'] = val

    def set_is_isotope(self, val):
        self._v['is_isotope'] = val

    def set_is_joint_dos(self, val):
        self._v['is_joint_dos'] = val

    def set_is_kappa_star(self, val):
        self._v['is_kappa_star'] = val

    def set_is_lbte(self, val):
        self._v['is_lbte'] = val

    def set_is_N_U(self, val):
        self._v['is_N_U'] = val

    def set_is_real_self_energy(self, val):
        self._v['is_real_self_energy'] = val

    def set_is_reducible_collision_matrix(self, val):
        self._v['is_reducible_collision_matrix'] = val

    def set_is_spectral_function(self, val):
        self._v['is_spectral_function'] = val

    def set_is_symmetrize_fc2(self, val):
        self._v['is_symmetrize_fc2'] = val

    def set_is_symmetrize_fc3_q(self, val):
        self._v['is_symmetrize_fc3_q'] = val

    def set_is_symmetrize_fc3_r(self, val):
        self._v['is_symmetrize_fc3_r'] = val

    def set_lapack_zheev_uplo(self, val):
        self._v['lapack_zheev_uplo'] = val

    def set_mass_variances(self, val):
        self._v['mass_variances'] = val

    def set_max_freepath(self, val):
        self._v['max_freepath'] = val

    def set_mesh_divisors(self, val):
        self._v['mesh_divisors'] = val

    def set_num_points_in_batch(self, val):
        self._v['num_points_in_batch'] = val

    def set_phonon_supercell_matrix(self, val):
        self._v['phonon_supercell_matrix'] = val

    def set_pinv_cutoff(self, val):
        self._v['pinv_cutoff'] = val

    def set_pinv_solver(self, val):
        self._v['pinv_solver'] = val

    def set_pp_conversion_factor(self, val):
        self._v['pp_conversion_factor'] = val

    def set_read_collision(self, val):
        self._v['read_collision'] = val

    def set_read_fc2(self, val):
        self._v['read_fc2'] = val

    def set_read_fc3(self, val):
        self._v['read_fc3'] = val

    def set_read_gamma(self, val):
        self._v['read_gamma'] = val

    def set_read_phonon(self, val):
        self._v['read_phonon'] = val

    def set_read_pp(self, val):
        self._v['read_pp'] = val

    def set_scattering_event_class(self, val):
        self._v['scattering_event_class'] = val

    def set_sigma_cutoff_width(self, val):
        self._v['sigma_cutoff_width'] = val

    def set_solve_collective_phonon(self, val):
        self._v['solve_collective_phonon'] = val

    def set_subtract_forces(self, val):
        self._v['subtract_forces'] = val

    def set_use_ave_pp(self, val):
        self._v['use_ave_pp'] = val

    def set_write_collision(self, val):
        self._v['write_collision'] = val

    def set_write_gamma_detail(self, val):
        self._v['write_gamma_detail'] = val

    def set_write_gamma(self, val):
        self._v['write_gamma'] = val

    def set_write_phonon(self, val):
        self._v['write_phonon'] = val

    def set_write_pp(self, val):
        self._v['write_pp'] = val

    def set_write_LBTE_solution(self, val):
        self._v['write_LBTE_solution'] = val


class Phono3pyConfParser(ConfParser):
    def __init__(self, filename=None, args=None, default_settings=None):
        self._settings = Phono3pySettings(default=default_settings)
        confs = {}
        if filename is not None:
            ConfParser.__init__(self, filename=filename)
            self.read_file()  # store .conf file setting in self._confs
            self._parse_conf()
            self._set_settings()
            confs.update(self._confs)
        if args is not None:
            ConfParser.__init__(self, args=args)
            self._read_options()
            self._parse_conf()
            self._set_settings()
            confs.update(self._confs)
        self._confs = confs

    def _read_options(self):
        ConfParser.read_options(self)  # store data in self._confs
        if 'phonon_supercell_dimension' in self._args:
            dim_fc2 = self._args.phonon_supercell_dimension
            if dim_fc2 is not None:
                self._confs['dim_fc2'] = " ".join(dim_fc2)

        if 'boundary_mfp' in self._args:
            if self._args.boundary_mfp is not None:
                self._confs['boundary_mfp'] = self._args.boundary_mfp

        if 'const_ave_pp' in self._args:
            const_ave_pp = self._args.const_ave_pp
            if const_ave_pp is not None:
                self._confs['const_ave_pp'] = const_ave_pp

        if 'create_forces_fc2' in self._args:
            if self._args.create_forces_fc2:
                self._confs['create_forces_fc2'] = self._args.create_forces_fc2

        if 'create_forces_fc3' in self._args:
            if self._args.create_forces_fc3:
                self._confs['create_forces_fc3'] = self._args.create_forces_fc3

        if 'create_forces_fc3_file' in self._args:
            if self._args.create_forces_fc3_file:
                cfc3_file = self._args.create_forces_fc3_file
                self._confs['create_forces_fc3_file'] = cfc3_file

        if 'cutoff_fc3_distance' in self._args:
            cutoff_fc3 = self._args.cutoff_fc3_distance
            if cutoff_fc3 is not None:
                self._confs['cutoff_fc3_distance'] = cutoff_fc3

        if 'cutoff_pair_distance' in self._args:
            cutoff_pair = self._args.cutoff_pair_distance
            if cutoff_pair is not None:
                self._confs['cutoff_pair_distance'] = cutoff_pair

        if 'gamma_conversion_factor' in self._args:
            g_conv_factor = self._args.gamma_conversion_factor
            if g_conv_factor is not None:
                self._confs['gamma_conversion_factor'] = g_conv_factor

        if 'grid_addresses' in self._args:
            grid_adrs = self._args.grid_addresses
            if grid_adrs is not None:
                self._confs['grid_addresses'] = " ".join(grid_adrs)

        if 'grid_points' in self._args:
            if self._args.grid_points is not None:
                self._confs['grid_points'] = " ".join(self._args.grid_points)

        if 'ion_clamped' in self._args:
            if self._args.ion_clamped:
                self._confs['ion_clamped'] = '.true.'

        if 'is_bterta' in self._args:
            if self._args.is_bterta:
                self._confs['bterta'] = '.true.'

        if 'is_compact_fc' in self._args:
            if self._args.is_compact_fc:
                self._confs['compact_fc'] = '.true.'

        if 'is_gruneisen' in self._args:
            if self._args.is_gruneisen:
                self._confs['gruneisen'] = '.true.'

        if 'is_full_pp' in self._args:
            if self._args.is_full_pp:
                self._confs['full_pp'] = '.true.'

        if 'is_imag_self_energy' in self._args:
            if self._args.is_imag_self_energy:
                self._confs['imag_self_energy'] = '.true.'

        if 'is_isotope' in self._args:
            if self._args.is_isotope:
                self._confs['isotope'] = '.true.'

        if 'is_joint_dos' in self._args:
            if self._args.is_joint_dos:
                self._confs['joint_dos'] = '.true.'

        if 'no_kappa_stars' in self._args:
            if self._args.no_kappa_stars:
                self._confs['kappa_star'] = '.false.'

        if 'is_lbte' in self._args:
            if self._args.is_lbte:
                self._confs['lbte'] = '.true.'

        if 'is_N_U' in self._args:
            if self._args.is_N_U:
                self._confs['N_U'] = '.true.'

        if 'is_real_self_energy' in self._args:
            if self._args.is_real_self_energy:
                self._confs['real_self_energy'] = '.true.'

        if 'is_reducible_collision_matrix' in self._args:
            if self._args.is_reducible_collision_matrix:
                self._confs['reducible_collision_matrix'] = '.true.'

        if 'is_spectral_function' in self._args:
            if self._args.is_spectral_function:
                self._confs['spectral_function'] = '.true.'

        if 'is_symmetrize_fc2' in self._args:
            if self._args.is_symmetrize_fc2:
                self._confs['symmetrize_fc2'] = '.true.'

        if 'is_symmetrize_fc3_q' in self._args:
            if self._args.is_symmetrize_fc3_q:
                self._confs['symmetrize_fc3_q'] = '.true.'

        if 'is_symmetrize_fc3_r' in self._args:
            if self._args.is_symmetrize_fc3_r:
                self._confs['symmetrize_fc3_r'] = '.true.'

        if 'lapack_zheev_uplo' in self._args:
            if self._args.lapack_zheev_uplo is not None:
                self._confs['lapack_zheev_uplo'] = self._args.lapack_zheev_uplo

        if 'mass_variances' in self._args:
            mass_variances = self._args.mass_variances
            if mass_variances is not None:
                self._confs['mass_variances'] = " ".join(mass_variances)

        if 'max_freepath' in self._args:
            if self._args.max_freepath is not None:
                self._confs['max_freepath'] = self._args.max_freepath

        if 'mesh_divisors' in self._args:
            mesh_divisors = self._args.mesh_divisors
            if mesh_divisors is not None:
                self._confs['mesh_divisors'] = " ".join(mesh_divisors)

        if 'num_points_in_batch' in self._args:
            num_points_in_batch = self._args.num_points_in_batch
            if num_points_in_batch is not None:
                self._confs['num_points_in_batch'] = num_points_in_batch

        if 'pinv_cutoff' in self._args:
            if self._args.pinv_cutoff is not None:
                self._confs['pinv_cutoff'] = self._args.pinv_cutoff

        if 'pinv_solver' in self._args:
            if self._args.pinv_solver is not None:
                self._confs['pinv_solver'] = self._args.pinv_solver

        if 'pp_conversion_factor' in self._args:
            pp_conv_factor = self._args.pp_conversion_factor
            if pp_conv_factor is not None:
                self._confs['pp_conversion_factor'] = pp_conv_factor

        if 'read_fc2' in self._args:
            if self._args.read_fc2:
                self._confs['read_fc2'] = '.true.'

        if 'read_fc3' in self._args:
            if self._args.read_fc3:
                self._confs['read_fc3'] = '.true.'

        if 'read_gamma' in self._args:
            if self._args.read_gamma:
                self._confs['read_gamma'] = '.true.'

        if 'read_phonon' in self._args:
            if self._args.read_phonon:
                self._confs['read_phonon'] = '.true.'

        if 'read_pp' in self._args:
            if self._args.read_pp:
                self._confs['read_pp'] = '.true.'

        if 'read_collision' in self._args:
            if self._args.read_collision is not None:
                self._confs['read_collision'] = self._args.read_collision

        if 'scattering_event_class' in self._args:
            scatt_class = self._args.scattering_event_class
            if scatt_class is not None:
                self._confs['scattering_event_class'] = scatt_class

        if 'sigma_cutoff_width' in self._args:
            sigma_cutoff = self._args.sigma_cutoff_width
            if sigma_cutoff is not None:
                self._confs['sigma_cutoff_width'] = sigma_cutoff

        if 'solve_collective_phonon' in self._args:
            if self._args.solve_collective_phonon:
                self._confs['collective_phonon'] = '.true.'

        if 'subtract_forces' in self._args:
            if self._args.subtract_forces:
                self._confs['subtract_forces'] = self._args.subtract_forces

        if 'use_ave_pp' in self._args:
            if self._args.use_ave_pp:
                self._confs['use_ave_pp'] = '.true.'

        if 'write_gamma_detail' in self._args:
            if self._args.write_gamma_detail:
                self._confs['write_gamma_detail'] = '.true.'

        if 'write_gamma' in self._args:
            if self._args.write_gamma:
                self._confs['write_gamma'] = '.true.'

        if 'write_collision' in self._args:
            if self._args.write_collision:
                self._confs['write_collision'] = '.true.'

        if 'write_phonon' in self._args:
            if self._args.write_phonon:
                self._confs['write_phonon'] = '.true.'

        if 'write_pp' in self._args:
            if self._args.write_pp:
                self._confs['write_pp'] = '.true.'

        if 'write_LBTE_solution' in self._args:
            if self._args.write_LBTE_solution:
                self._confs['write_LBTE_solution'] = '.true.'

    def _parse_conf(self):
        ConfParser.parse_conf(self)
        confs = self._confs

        for conf_key in confs.keys():
            # Boolean
            if conf_key in (
                    'read_fc2', 'read_fc3', 'read_gamma', 'read_phonon',
                    'read_pp', 'use_ave_pp', 'collective_phonon',
                    'write_gamma_detail', 'write_gamma',
                    'write_collision', 'write_phonon', 'write_pp',
                    'write_LBTE_solution', 'full_pp', 'ion_clamped',
                    'bterta', 'compact_fc', 'real_self_energy',
                    'gruneisen', 'imag_self_energy', 'isotope',
                    'joint_dos', 'lbte', 'N_U', 'spectral_function',
                    'reducible_collision_matrix', 'symmetrize_fc2',
                    'symmetrize_fc3_q', 'symmetrize_fc3_r', 'kappa_star'):
                if confs[conf_key].lower() == '.true.':
                    self.set_parameter(conf_key, True)
                elif confs[conf_key].lower() == '.false.':
                    self.set_parameter(conf_key, False)

            # float
            if conf_key in (
                    'boundary_mfp', 'cutoff_fc3_distance',
                    'cutoff_pair_distance', 'gamma_conversion_factor',
                    'max_freepath', 'pinv_cutoff', 'pp_conversion_factor',
                    'sigma_cutoff_width'):
                self.set_parameter(conf_key, float(confs[conf_key]))

            # int
            if conf_key in ('pinv_solver', 'num_points_in_batch'):
                self.set_parameter(conf_key, int(confs[conf_key]))

            # specials
            if conf_key in ('create_forces_fc2', 'create_forces_fc3'):
                if type(confs[conf_key]) is str:
                    fnames = confs[conf_key].split()
                else:
                    fnames = confs[conf_key]
                self.set_parameter(conf_key, fnames)

            if conf_key == 'dim_fc2':
                matrix = [ int(x) for x in confs['dim_fc2'].split() ]
                if len(matrix) == 9:
                    matrix = np.array(matrix).reshape(3, 3)
                elif len(matrix) == 3:
                    matrix = np.diag(matrix)
                else:
                    self.setting_error(
                        "Number of elements of dim2 has to be 3 or 9.")

                if matrix.shape == (3, 3):
                    if np.linalg.det(matrix) < 1:
                        self.setting_error(
                            "Determinant of supercell matrix has " +
                            "to be positive.")
                    else:
                        self.set_parameter('dim_fc2', matrix)

            if conf_key in ('constant_averaged_pp_interaction'
                            'const_ave_pp'):
                self.set_parameter('const_ave_pp', float(confs['const_ave_pp']))

            if conf_key == 'grid_addresses':
                vals = [int(x) for x in
                        confs['grid_addresses'].replace(',', ' ').split()]
                if len(vals) % 3 == 0 and len(vals) > 0:
                    self.set_parameter('grid_addresses',
                                       np.reshape(vals, (-1, 3)))
                else:
                    self.setting_error("Grid addresses are incorrectly set.")

            if conf_key == 'grid_points':
                vals = [int(x) for x in
                        confs['grid_points'].replace(',', ' ').split()]
                self.set_parameter('grid_points', vals)

            if conf_key == 'lapack_zheev_uplo':
                self.set_parameter('lapack_zheev_uplo',
                                   confs['lapack_zheev_uplo'].upper())

            if conf_key == 'mass_variances':
                vals = [fracval(x) for x in confs['mass_variances'].split()]
                if len(vals) < 1:
                    self.setting_error("Mass variance parameters are incorrectly set.")
                else:
                    self.set_parameter('mass_variances', vals)

            if conf_key == 'mesh_divisors':
                vals = [x for x in confs['mesh_divisors'].split()]
                if len(vals) == 3:
                    self.set_parameter('mesh_divisors', [int(x) for x in vals])
                elif len(vals) == 6:
                    divs = [int(x) for x in vals[:3]]
                    is_shift = [x.lower() == 't' for x in vals[3:]]
                    for i in range(3):
                        if is_shift[i] and (divs[i] % 2 != 0):
                            is_shift[i] = False
                            self.setting_error("Coarse grid shift along the " +
                                               ["first", "second", "third"][i] +
                                               " axis is not allowed.")
                    self.set_parameter('mesh_divisors', divs + is_shift)
                else:
                    self.setting_error("Mesh divisors are incorrectly set.")

            if conf_key == 'read_collision':
                if confs['read_collision'] == 'all':
                    self.set_parameter('read_collision', 'all')
                else:
                    vals = [int(x) for x in confs['read_collision'].split()]
                    self.set_parameter('read_collision', vals)

            if conf_key == 'scattering_event_class':
                self.set_parameter('scattering_event_class',
                                   int(confs['scattering_event_class']))

    def _set_settings(self):
        self.set_settings()
        params = self._parameters

        # Supercell dimension for fc2
        if 'dim_fc2' in params:
            self._settings.set_phonon_supercell_matrix(params['dim_fc2'])

        # Boundary mean free path for thermal conductivity calculation
        if 'boundary_mfp' in params:
            self._settings.set_boundary_mfp(params['boundary_mfp'])

        # Calculate thermal conductivity in BTE-RTA
        if 'bterta' in params:
            self._settings.set_is_bterta(params['bterta'])

        # Solve collective phonons
        if 'collective_phonon' in params:
            self._settings.set_solve_collective_phonon(
                params['collective_phonon'])

        # Compact force constants or full force constants
        if 'compact_fc' in params:
            self._settings.set_is_compact_fc(params['compact_fc'])

        # Peierls type approximation for squared ph-ph interaction strength
        if 'const_ave_pp' in params:
            self._settings.set_constant_averaged_pp_interaction(
                params['const_ave_pp'])

        # Trigger to create FORCES_FC2 and FORCES_FC3
        if 'create_forces_fc2' in params:
            self._settings.set_create_forces_fc3(params['create_forces_fc2'])

        if 'create_forces_fc3' in params:
            self._settings.set_create_forces_fc3(params['create_forces_fc3'])

        if 'create_forces_fc3_file' in params:
            self._settings.set_create_forces_fc3_file(
                params['create_forces_fc3_file'])

        # Cutoff distance of third-order force constants. Elements where any
        # pair of atoms has larger distance than cut-off distance are set zero.
        if 'cutoff_fc3_distance' in params:
            self._settings.set_cutoff_fc3_distance(
                params['cutoff_fc3_distance'])

        # Cutoff distance between pairs of displaced atoms used for supercell
        # creation with displacements and making third-order force constants
        if 'cutoff_pair_distance' in params:
            self._settings.set_cutoff_pair_distance(
                params['cutoff_pair_distance'])

        # Gamma unit conversion factor
        if 'gamma_conversion_factor' in params:
            self._settings.set_gamma_conversion_factor(
                params['gamma_conversion_factor'])

        # Grid addresses (sets of three integer values)
        if 'grid_addresses' in params:
            self._settings.set_grid_addresses(params['grid_addresses'])

        # Grid points
        if 'grid_points' in params:
            self._settings.set_grid_points(params['grid_points'])

        # Atoms are clamped under applied strain in Gruneisen parameter calculation
        if 'ion_clamped' in params:
            self._settings.set_ion_clamped(params['ion_clamped'])

        # Calculate full ph-ph interaction strength for RTA conductivity
        if 'full_pp' in params:
            self._settings.set_is_full_pp(params['full_pp'])

        # Calculate phonon-Gruneisen parameters
        if 'gruneisen' in params:
            self._settings.set_is_gruneisen(params['gruneisen'])

        # Calculate imaginary part of self energy
        if 'imag_self_energy' in params:
            self._settings.set_is_imag_self_energy(params['imag_self_energy'])

        # Calculate lifetime due to isotope scattering
        if 'isotope' in params:
            self._settings.set_is_isotope(params['isotope'])

        # Calculate joint-DOS
        if 'joint_dos' in params:
            self._settings.set_is_joint_dos(params['joint_dos'])

        # Sum partial kappa at q-stars
        if 'kappa_star' in params:
            self._settings.set_is_kappa_star(params['kappa_star'])

        if 'lapack_zheev_uplo' in params:
            self._settings.set_lapack_zheev_uplo(params['lapack_zheev_uplo'])

        # Calculate thermal conductivity in LBTE with Chaput's method
        if 'lbte' in params:
            self._settings.set_is_lbte(params['lbte'])

        # Number of frequency points in a batch.
        if 'num_points_in_batch' in params:
            self._settings.set_num_points_in_batch(
                params['num_points_in_batch'])

        # Calculate Normal and Umklapp processes
        if 'N_U' in params:
            self._settings.set_is_N_U(params['N_U'])

        # Solve reducible collision matrix but not reduced matrix
        if 'reducible_collision_matrix' in params:
            self._settings.set_is_reducible_collision_matrix(
                params['reducible_collision_matrix'])

        # Symmetrize fc2 by index exchange
        if 'symmetrize_fc2' in params:
            self._settings.set_is_symmetrize_fc2(params['symmetrize_fc2'])

        # Symmetrize phonon fc3 by index exchange
        if 'symmetrize_fc3_q' in params:
            self._settings.set_is_symmetrize_fc3_q(params['symmetrize_fc3_q'])

        # Symmetrize fc3 by index exchange
        if 'symmetrize_fc3_r' in params:
            self._settings.set_is_symmetrize_fc3_r(params['symmetrize_fc3_r'])

        # Mass variance parameters
        if 'mass_variances' in params:
            self._settings.set_mass_variances(params['mass_variances'])

        # Maximum mean free path
        if 'max_freepath' in params:
            self._settings.set_max_freepath(params['max_freepath'])

        # Divisors for mesh numbers
        if 'mesh_divisors' in params:
            self._settings.set_mesh_divisors(params['mesh_divisors'][:3])
            if len(params['mesh_divisors']) > 3:
                self._settings.set_coarse_mesh_shifts(
                    params['mesh_divisors'][3:])

        # Cutoff frequency for pseudo inversion of collision matrix
        if 'pinv_cutoff' in params:
            self._settings.set_pinv_cutoff(params['pinv_cutoff'])

        # Switch for pseudo-inverse solver
        if 'pinv_solver' in params:
            self._settings.set_pinv_solver(params['pinv_solver'])

        # Ph-ph interaction unit conversion factor
        if 'pp_conversion_factor' in params:
            self._settings.set_pp_conversion_factor(
                params['pp_conversion_factor'])

        # Calculate real_self_energys
        if 'real_self_energy' in params:
            self._settings.set_is_real_self_energy(params['real_self_energy'])

        # Read phonon-phonon interaction amplitudes from hdf5
        if 'read_amplitude' in params:
            self._settings.set_read_amplitude(params['read_amplitude'])

        # Read collision matrix and gammas from hdf5
        if 'read_collision' in params:
            self._settings.set_read_collision(params['read_collision'])

        # Read fc2 from hdf5
        if 'read_fc2' in params:
            self._settings.set_read_fc2(params['read_fc2'])

        # Read fc3 from hdf5
        if 'read_fc3' in params:
            self._settings.set_read_fc3(params['read_fc3'])

        # Read gammas from hdf5
        if 'read_gamma' in params:
            self._settings.set_read_gamma(params['read_gamma'])

        # Read phonons from hdf5
        if 'read_phonon' in params:
            self._settings.set_read_phonon(params['read_phonon'])

        # Read ph-ph interaction strength from hdf5
        if 'read_pp' in params:
            self._settings.set_read_pp(params['read_pp'])

        # Scattering event class 1 or 2
        if 'scattering_event_class' in params:
            self._settings.set_scattering_event_class(
                params['scattering_event_class'])

        # Cutoff width of smearing function (ratio to sigma value)
        if 'sigma_cutoff_width' in params:
            self._settings.set_sigma_cutoff_width(params['sigma_cutoff_width'])

        # Calculate spectral_functions
        if 'spectral_function' in params:
            self._settings.set_is_spectral_function(params['spectral_function'])

        # Subtract residual forces to create FORCES_FC2 and FORCES_FC3
        if 'subtract_forces' in params:
            self._settings.set_subtract_forces(params['subtract_forces'])

        # Use averaged ph-ph interaction
        if 'use_ave_pp' in params:
            self._settings.set_use_ave_pp(params['use_ave_pp'])

        # Write detailed imag-part of self energy to hdf5
        if 'write_gamma_detail' in params:
            self._settings.set_write_gamma_detail(
                params['write_gamma_detail'])

        # Write imag-part of self energy to hdf5
        if 'write_gamma' in params:
            self._settings.set_write_gamma(params['write_gamma'])

        # Write collision matrix and gammas to hdf5
        if 'write_collision' in params:
            self._settings.set_write_collision(params['write_collision'])

        # Write all phonons on grid points to hdf5
        if 'write_phonon' in params:
            self._settings.set_write_phonon(params['write_phonon'])

        # Write phonon-phonon interaction amplitudes to hdf5
        if 'write_pp' in params:
            self._settings.set_write_pp(params['write_pp'])

        # Write direct solution of LBTE to hdf5 files
        if 'write_LBTE_solution' in params:
            self._settings.set_write_LBTE_solution(
                params['write_LBTE_solution'])

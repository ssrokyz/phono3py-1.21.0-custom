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

import os
import sys
import numpy as np
from phonopy.harmonic.force_constants import (
    show_drift_force_constants,
    symmetrize_force_constants,
    symmetrize_compact_force_constants)
from phonopy.file_IO import get_dataset_type2, parse_FORCE_SETS
from phonopy.cui.phonopy_script import print_error, file_exists
from phonopy.interface.calculator import get_default_physical_units
from phono3py.phonon3.fc3 import show_drift_fc3
from phono3py.file_IO import (
    parse_disp_fc3_yaml, parse_disp_fc2_yaml, parse_FORCES_FC2,
    parse_FORCES_FC3, read_fc3_from_hdf5, read_fc2_from_hdf5,
    write_fc3_to_hdf5, write_fc2_to_hdf5, get_length_of_first_line)
from phono3py.cui.show_log import show_phono3py_force_constants_settings
from phono3py.phonon3.fc3 import (
    set_permutation_symmetry_fc3, set_translational_invariance_fc3)
from phono3py.interface.phono3py_yaml import Phono3pyYaml


def create_phono3py_force_constants(phono3py,
                                    settings,
                                    ph3py_yaml=None,
                                    input_filename=None,
                                    output_filename=None,
                                    phono3py_yaml_filename=None,
                                    log_level=1):
    if settings.fc_calculator is None:
        symmetrize_fc3r = (settings.is_symmetrize_fc3_r or
                           settings.fc_symmetry)
        symmetrize_fc2 = (settings.is_symmetrize_fc2 or
                          settings.fc_symmetry)
    else:  # Rely on fc calculator the symmetrization of fc.
        symmetrize_fc2 = False
        symmetrize_fc3r = False

    if log_level:
        show_phono3py_force_constants_settings(settings)

    #######
    # fc3 #
    #######
    if (settings.is_joint_dos or
        (settings.is_isotope and
         not (settings.is_bterta or settings.is_lbte)) or
        settings.read_gamma or
        settings.read_pp or
        (not settings.is_bterta and settings.write_phonon) or
        settings.constant_averaged_pp_interaction is not None):
        pass
    else:
        if settings.read_fc3:
            _read_phono3py_fc3(phono3py,
                               symmetrize_fc3r,
                               input_filename,
                               log_level)
        else:  # fc3 from FORCES_FC3 or ph3py_yaml
            _create_phono3py_fc3(phono3py,
                                 ph3py_yaml,
                                 symmetrize_fc3r,
                                 symmetrize_fc2,
                                 input_filename,
                                 output_filename,
                                 settings.is_compact_fc,
                                 settings.cutoff_pair_distance,
                                 settings.fc_calculator,
                                 settings.fc_calculator_options,
                                 log_level)
            if output_filename is None:
                filename = 'fc3.hdf5'
            else:
                filename = 'fc3.' + output_filename + '.hdf5'
            if log_level:
                print("Writing fc3 to \"%s\"." % filename)
            write_fc3_to_hdf5(phono3py.fc3,
                              filename=filename,
                              p2s_map=phono3py.primitive.p2s_map,
                              compression=settings.hdf5_compression)

        cutoff_distance = settings.cutoff_fc3_distance
        if cutoff_distance is not None and cutoff_distance > 0:
            if log_level:
                print("Cutting-off fc3 by zero (cut-off distance: %f)" %
                      cutoff_distance)
            phono3py.cutoff_fc3_by_zero(cutoff_distance)

        if log_level:
            show_drift_fc3(phono3py.fc3, primitive=phono3py.primitive)

    #######
    # fc2 #
    #######
    phonon_primitive = phono3py.phonon_primitive
    p2s_map = phonon_primitive.p2s_map
    if settings.read_fc2:
        _read_phono3py_fc2(phono3py,
                           symmetrize_fc2,
                           input_filename,
                           log_level)
    else:
        if phono3py.phonon_supercell_matrix is None:
            if (settings.fc_calculator == 'alm' and phono3py.fc2 is not None):
                if log_level:
                    print("fc2 that was fit simultaneously with fc3 "
                          "by ALM is used.")
            else:
                _create_phono3py_fc2(phono3py,
                                     ph3py_yaml,
                                     symmetrize_fc2,
                                     input_filename,
                                     settings.is_compact_fc,
                                     settings.fc_calculator,
                                     settings.fc_calculator_options,
                                     log_level)
        else:
            _create_phono3py_phonon_fc2(phono3py,
                                        ph3py_yaml,
                                        symmetrize_fc2,
                                        input_filename,
                                        settings.is_compact_fc,
                                        settings.fc_calculator,
                                        settings.fc_calculator_options,
                                        log_level)
        if output_filename is None:
            filename = 'fc2.hdf5'
        else:
            filename = 'fc2.' + output_filename + '.hdf5'
        if log_level:
            print("Writing fc2 to \"%s\"." % filename)
        write_fc2_to_hdf5(phono3py.fc2,
                          filename=filename,
                          p2s_map=p2s_map,
                          physical_unit='eV/angstrom^2',
                          compression=settings.hdf5_compression)

    if log_level:
        show_drift_force_constants(phono3py.fc2,
                                   primitive=phonon_primitive,
                                   name='fc2')


def parse_forces(phono3py,
                 ph3py_yaml=None,
                 cutoff_pair_distance=None,
                 force_filename="FORCES_FC3",
                 disp_filename=None,
                 fc_type=None,
                 log_level=0):
    filename_read_from = None

    if fc_type == 'phonon_fc2':
        natom = len(phono3py.phonon_supercell)
    else:
        natom = len(phono3py.supercell)

    # Get dataset from ph3py_yaml. dataset can be None.
    dataset = _extract_datast_from_ph3py_yaml(ph3py_yaml, fc_type)
    if dataset:
        filename_read_from = ph3py_yaml.yaml_filename

    # Try to read FORCES_FC* if type-2 and return dataset.
    # None is returned unless type-2.
    # can emit FileNotFoundError.
    if (dataset is None or
        dataset is not None and not forces_in_dataset(dataset)):
        _dataset = _get_type2_dataset(natom,
                                      phono3py.calculator,
                                      filename=force_filename,
                                      log_level=log_level)
        # Do not overwrite dataset when _dataset is None.
        if _dataset:
            filename_read_from = force_filename
            dataset = _dataset

    if dataset is None:
        # Displacement dataset is obtained from disp_filename.
        # can emit FileNotFoundError.
        dataset = _read_disp_fc_yaml(disp_filename, fc_type)
        filename_read_from = disp_filename

    if 'natom' in dataset and dataset['natom'] != natom:
        msg = ("Number of atoms in supercell is not consistent with "
               "\"%s\"." % filename_read_from)
        raise RuntimeError(msg)

    if log_level and filename_read_from is not None:
        print("Displacement dataset for %s was read from \"%s\"."
              % (fc_type, filename_read_from))

    if cutoff_pair_distance:
        if ('cutoff_distance' not in dataset or
            ('cutoff_distance' in dataset and
             cutoff_pair_distance < dataset['cutoff_distance'])):
            dataset['cutoff_distance'] = cutoff_pair_distance
            if log_level:
                print("Cutoff-pair-distance: %f" % cutoff_pair_distance)

    # Type-1 FORCES_FC*.
    # dataset comes either from disp_fc*.yaml or phono3py*.yaml.
    if not forces_in_dataset(dataset):
        if fc_type == 'phonon_fc2':
            parse_FORCES_FC2(dataset, filename=force_filename)
        else:
            parse_FORCES_FC3(dataset, filename=force_filename)

        if log_level:
            print("Sets of supercell forces were read from \"%s\"."
                  % force_filename)
            sys.stdout.flush()

    _convert_unit_in_dataset(dataset, phono3py.calculator)

    return dataset


def forces_in_dataset(dataset):
    return ('forces' in dataset or
            ('first_atoms' in dataset and
             'forces' in dataset['first_atoms'][0]))


def _read_disp_fc_yaml(disp_filename, fc_type):
    if fc_type == 'phonon_fc2':
        dataset = parse_disp_fc2_yaml(filename=disp_filename)
    else:
        dataset = parse_disp_fc3_yaml(filename=disp_filename)

    return dataset


def _read_phono3py_fc3(phono3py,
                       symmetrize_fc3r,
                       input_filename,
                       log_level):
    if input_filename is None:
        filename = 'fc3.hdf5'
    else:
        filename = 'fc3.' + input_filename + '.hdf5'
    file_exists(filename, log_level)
    if log_level:
        print("Reading fc3 from \"%s\"." % filename)

    p2s_map = phono3py.primitive.p2s_map
    try:
        fc3 = read_fc3_from_hdf5(filename=filename, p2s_map=p2s_map)
    except RuntimeError:
        import traceback
        traceback.print_exc()
        if log_level:
            print_error()
        sys.exit(1)
    num_atom = phono3py.supercell.get_number_of_atoms()
    if fc3.shape[1] != num_atom:
        print("Matrix shape of fc3 doesn't agree with supercell size.")
        if log_level:
            print_error()
        sys.exit(1)

    if symmetrize_fc3r:
        set_translational_invariance_fc3(fc3)
        set_permutation_symmetry_fc3(fc3)

    phono3py.fc3 = fc3


def _read_phono3py_fc2(phono3py,
                       symmetrize_fc2,
                       input_filename,
                       log_level):
    if input_filename is None:
        filename = 'fc2.hdf5'
    else:
        filename = 'fc2.' + input_filename + '.hdf5'
    file_exists(filename, log_level)
    if log_level:
        print("Reading fc2 from \"%s\"." % filename)

    num_atom = phono3py.phonon_supercell.get_number_of_atoms()
    p2s_map = phono3py.phonon_primitive.p2s_map
    try:
        phonon_fc2 = read_fc2_from_hdf5(filename=filename, p2s_map=p2s_map)
    except RuntimeError:
        import traceback
        traceback.print_exc()
        if log_level:
            print_error()
        sys.exit(1)

    if phonon_fc2.shape[1] != num_atom:
        print("Matrix shape of fc2 doesn't agree with supercell size.")
        if log_level:
            print_error()
        sys.exit(1)

    if symmetrize_fc2:
        if phonon_fc2.shape[0] == phonon_fc2.shape[1]:
            symmetrize_force_constants(phonon_fc2)
        else:
            symmetrize_compact_force_constants(phonon_fc2,
                                               phono3py.phonon_primitive)

    phono3py.fc2 = phonon_fc2


def _get_type2_dataset(natom, calculator, filename="FORCES_FC3", log_level=0):
    if not os.path.isfile(filename):
        return None

    with open(filename, 'r') as f:
        len_first_line = get_length_of_first_line(f)
        if len_first_line == 6:
            dataset = get_dataset_type2(f, natom)
            if log_level:
                print("%d snapshots were found in %s."
                      % (len(dataset['displacements']), "FORCES_FC3"))
        else:
            dataset = None
    return dataset


def _create_phono3py_fc3(phono3py,
                         ph3py_yaml,
                         symmetrize_fc3r,
                         symmetrize_fc2,
                         input_filename,
                         output_filename,
                         is_compact_fc,
                         cutoff_pair_distance,
                         fc_calculator,
                         fc_calculator_options,
                         log_level):
    """

    Note
    ----
    cutoff_pair_distance is the parameter to determine each displaced
    supercell is included to the computation of fc3. It is assumed that
    cutoff_pair_distance is stored in the step to create sets of
    displacements and the value is stored n the displacement dataset and
    also as the parameter 'included': True or False for each displacement.
    The parameter cutoff_pair_distance here can be used in the step to
    create fc3 by overwriting original cutoff_pair_distance value only
    when the former value is smaller than the later.

    """
    if input_filename is None:
        disp_filename = 'disp_fc3.yaml'
    else:
        disp_filename = 'disp_fc3.' + input_filename + '.yaml'

    _ph3py_yaml = _get_ph3py_yaml(disp_filename, ph3py_yaml)

    try:
        dataset = parse_forces(phono3py,
                               ph3py_yaml=_ph3py_yaml,
                               cutoff_pair_distance=cutoff_pair_distance,
                               force_filename="FORCES_FC3",
                               disp_filename=disp_filename,
                               fc_type='fc3',
                               log_level=log_level)
    except RuntimeError as e:
        # from _parse_forces_type1
        if log_level:
            print(str(e))
            print_error()
        sys.exit(1)
    except FileNotFoundError as e:
        # from _get_type2_dataset
        file_exists(e.filename, log_level)

    phono3py.dataset = dataset
    phono3py.produce_fc3(symmetrize_fc3r=symmetrize_fc3r,
                         is_compact_fc=is_compact_fc,
                         fc_calculator=fc_calculator,
                         fc_calculator_options=fc_calculator_options)


def _create_phono3py_fc2(phono3py,
                         ph3py_yaml,
                         symmetrize_fc2,
                         input_filename,
                         is_compact_fc,
                         fc_calculator,
                         fc_calculator_options,
                         log_level):
    if input_filename is None:
        disp_filename = 'disp_fc3.yaml'
    else:
        disp_filename = 'disp_fc3.' + input_filename + '.yaml'

    _ph3py_yaml = _get_ph3py_yaml(disp_filename, ph3py_yaml)

    try:
        dataset = parse_forces(phono3py,
                               ph3py_yaml=_ph3py_yaml,
                               force_filename="FORCES_FC3",
                               disp_filename=disp_filename,
                               fc_type='fc2',
                               log_level=log_level)
    except RuntimeError as e:
        if log_level:
            print(str(e))
            print_error()
        sys.exit(1)
    except FileNotFoundError as e:
        file_exists(e.filename, log_level)

    phono3py.phonon_dataset = dataset
    phono3py.produce_fc2(
        symmetrize_fc2=symmetrize_fc2,
        is_compact_fc=is_compact_fc,
        fc_calculator=fc_calculator,
        fc_calculator_options=fc_calculator_options)


def _get_ph3py_yaml(disp_filename, ph3py_yaml):
    _ph3py_yaml = ph3py_yaml
    # Try to use phono3py.phonon_dataset when the disp file not found
    if not os.path.isfile(disp_filename):
        disp_filename = None
        if _ph3py_yaml is None and os.path.isfile('phono3py_disp.yaml'):
            _ph3py_yaml = Phono3pyYaml()
            _ph3py_yaml.read('phono3py_disp.yaml')
    return _ph3py_yaml


def _create_phono3py_phonon_fc2(phono3py,
                                ph3py_yaml,
                                symmetrize_fc2,
                                input_filename,
                                is_compact_fc,
                                fc_calculator,
                                fc_calculator_options,
                                log_level):
    if input_filename is None:
        disp_filename = 'disp_fc2.yaml'
    else:
        disp_filename = 'disp_fc2.' + input_filename + '.yaml'

    _ph3py_yaml = _get_ph3py_yaml(disp_filename, ph3py_yaml)

    try:
        dataset = parse_forces(phono3py,
                               ph3py_yaml=_ph3py_yaml,
                               force_filename="FORCES_FC2",
                               disp_filename=disp_filename,
                               fc_type='phonon_fc2',
                               log_level=log_level)
    except RuntimeError as e:
        if log_level:
            print(str(e))
            print_error()
        sys.exit(1)
    except FileNotFoundError as e:
        file_exists(e.filename, log_level)

    phono3py.phonon_dataset = dataset
    phono3py.produce_fc2(
        symmetrize_fc2=symmetrize_fc2,
        is_compact_fc=is_compact_fc,
        fc_calculator=fc_calculator,
        fc_calculator_options=fc_calculator_options)


def _convert_unit_in_dataset(dataset, calculator):
    physical_units = get_default_physical_units(calculator)
    force_to_eVperA = physical_units['force_to_eVperA']
    distance_to_A = physical_units['distance_to_A']

    if 'first_atoms' in dataset:
        for d1 in dataset['first_atoms']:
            if distance_to_A is not None:
                disp = _to_ndarray(d1['displacement'])
                d1['displacement'] = disp * distance_to_A
            if force_to_eVperA is not None and 'forces' in d1:
                forces = _to_ndarray(d1['forces'])
                d1['forces'] = forces * force_to_eVperA
            if 'second_atoms' in d1:
                for d2 in d1['second_atoms']:
                    if distance_to_A is not None:
                        disp = _to_ndarray(d2['displacement'])
                        d2['displacement'] = disp * distance_to_A
                    if force_to_eVperA is not None and 'forces' in d2:
                        forces = _to_ndarray(d2['forces'])
                        d2['forces'] = forces * force_to_eVperA
    else:
        if distance_to_A is not None and 'displacements' in dataset:
            disp = _to_ndarray(dataset['displacements'])
            dataset['displacements'] = disp * distance_to_A
        if force_to_eVperA is not None and 'forces' in dataset:
            forces = _to_ndarray(dataset['forces'])
            dataset['forces'] = forces * force_to_eVperA


def _to_ndarray(array, dtype='double'):
    if type(array) is not np.ndarray:
        return np.array(array, dtype=dtype, order='C')
    else:
        return array


def _extract_datast_from_ph3py_yaml(ph3py_yaml, fc_type):
    dataset = None
    if fc_type == 'phonon_fc2':
        if ph3py_yaml and ph3py_yaml.phonon_dataset is not None:
            # copy dataset
            # otherwise unit conversion can be applied multiple times.
            _ph3py_yaml = Phono3pyYaml()
            _ph3py_yaml.yaml_data = ph3py_yaml.yaml_data
            _ph3py_yaml.parse()
            dataset = _ph3py_yaml.phonon_dataset
    else:
        if ph3py_yaml and ph3py_yaml.dataset is not None:
            # copy dataset
            # otherwise unit conversion can be applied multiple times.
            _ph3py_yaml = Phono3pyYaml()
            _ph3py_yaml.yaml_data = ph3py_yaml.yaml_data
            _ph3py_yaml.parse()
            dataset = _ph3py_yaml.dataset
    return dataset

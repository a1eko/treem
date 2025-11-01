"""Implementation of CLI check command."""

import os
import json
import warnings

import numpy as np

from treem.io import SWC, TreemEncoder


def _validate_file_path(args, err):
    """Checks for file existence and accessibility."""
    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        err['no_file'] = [args.file]
        return False
    return True

def _check_file_extension(args, err):
    """Checks for SWC extension."""
    if not args.file.lower().endswith('swc'):
        err['not_swc_ext'] = [args.file.split('.')[-1]]

def _load_data_array(args, err):
    """Loads data, checking for array format and size."""
    data = None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            data = np.loadtxt(args.file)
    except ValueError:
        err['not_array'] = [True]
        return None
    if data.shape[0] == 0:
        err['no_data'] = [True]
        return None
    if len(data.shape) == 1:
        err['single_point'] = [data[SWC.I].astype(int)]
        return None
    if data.shape[1] != len(SWC.COLS):
        err['not_swc_cols'] = [data.shape[1]]
        return None
    return data

def _check_first_node(data, err):
    """Checks the first node (soma) properties."""
    first = data[0]
    if first[SWC.I] != 1:
        err['node1_not_id1'] = [first[SWC.I].astype(int)]
    if first[SWC.P] != -1:
        err['node1_has_parent'] = [first[SWC.P].astype(int)]
    if first[SWC.T] != SWC.SOMA:
        err['node1_not_soma'] = [first[SWC.T].astype(int)]

def _check_soma_nodes(data, err):
    """Checks for sequential soma."""
    soma_nodes = data[data[:, SWC.T] == SWC.SOMA]
    soma_ids = soma_nodes[:, SWC.I].astype(int)
    if len(soma_ids > 1):
        inc = soma_ids[1:] - soma_ids[:-1]
        if not (inc == 1).all():
            err['non_sequential_soma_ids'] = soma_ids[np.nonzero(inc != 1)[0] + 1]

def _check_valid_types(data, err):
    """Checks for valid node types."""
    types = set(data[:, SWC.T].astype(int))
    if not types.issubset(SWC.TYPES):
        err['not_valid_types'] = [
            data[x][SWC.I].astype(int)
            for t in types.difference(SWC.TYPES)
            for x in np.nonzero(data[:, SWC.T] == t)[0]
        ]

def _check_ids(data, err):
    """Checks for valid and unique IDs."""
    ids = data[:, SWC.I].astype(int)
    if not (ids > 0).all():
        err['not_valid_ids'] = ids[ids <= 0]
        #return ids, None # critical error, must break validation
    ids_set = set(ids)
    if len(ids_set) != len(ids):
        seen = set()
        err['non_unique_ids'] = {x for x in ids if x in seen or seen.add(x)}
        #return None # critical error, must break validation
    return ids, ids_set

def _check_parent_ids(data, ids_set, err):
    """Checks for valid parent IDs and defined parents."""
    ids = data[:, SWC.I].astype(int)
    idp = data[1:, SWC.P].astype(int)
    if not (idp > 0).all():
        err['not_valid_parent_ids'] = ids[1:][idp <= 0]
        return False # critical error, must break validation
    idp_set = set(idp)
    if not idp_set.issubset(ids_set):
        err['undef_parent_ids'] = [
            data[x][SWC.I].astype(int)
            for p in idp_set.difference(ids_set)
            for x in np.nonzero(data[:, SWC.P] == p)[0]
        ]
        return False # critical error, must break validation
    return idp

def _check_id_sequence_and_descent(data, ids, idp, err):
    """Checks ID order and parent/child relationship."""
    inc = ids[1:] - ids[:-1]
    if not (inc > 0).all():
        err['non_increasing_ids'] = ids[np.nonzero(inc <= 0)[0] + 1]
        return False # critical error, must break validation
    if not (inc == 1).all():
        err['non_sequential_ids'] = ids[np.nonzero(inc != 1)[0] + 1]
        return False # critical error, must break validation
    if not (ids[1:] > idp).all():
        err['non_descendant'] = ids[np.nonzero(ids[1:] <= idp)[0] + 1]
        return False # critical error, must break validation
    return True

def _check_non_stem_neurite(data, err):
    """Checks if neurites are properly stemmed from the soma."""
    types = set(data[:, SWC.T].astype(int))
    non_stem_list = [
        data[x][SWC.I].astype(int)
        for t in types.difference([SWC.SOMA]) # SWC.SOMA is 1
        for x in np.nonzero(data[:, SWC.T] == t)[0][:1]
        if data[x][SWC.P] != 1
    ]
    if non_stem_list:
        err['non_stem_neurite'] = non_stem_list

def _dump_results(err, quiet=False, out=False):
    """Print out and save check results."""
    if not quiet:
        for k in err:
            print(f'{k}:', end=' ')
            print(*err[k])
    if out:
        with open(out, 'w', encoding='utf-8') as file:
            json.dump(err, file, cls=TreemEncoder)


def check(args):
    """Checks morphology reconstruction for structural consistency."""
    err = {}

    # basic file checks
    if not _validate_file_path(args, err):
        _dump_results(err, args.quiet, args.out)
        return len(err)

    _check_file_extension(args, err)

    # data loading checks
    data = _load_data_array(args, err)
    if data is None or len(err) > 0:
        _dump_results(err, args.quiet, args.out)
        return len(err)

    # structural node checks
    _check_first_node(data, err)
    _check_soma_nodes(data, err)
    _check_valid_types(data, err)
    _check_non_stem_neurite(data, err)

    # id consistency checks
    ids, ids_set = _check_ids(data, err)
    #if ids is None or len(err) > 0:
    #    _dump_results(err, args.quiet, args.out)
    #    return len(err)

    idp = _check_parent_ids(data, ids_set, err)
    #if idp is False or len(err) > 0:
    #    _dump_results(err, args.quiet, args.out)
    #    return len(err)

    # id sequence and descent checks
    if not _check_id_sequence_and_descent(data, ids, idp, err):
        _dump_results(err, args.quiet, args.out)
        return len(err)

    _dump_results(err, args.quiet, args.out)
    return len(err)

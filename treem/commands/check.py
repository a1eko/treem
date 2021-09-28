"""Implementation of CLI check command."""

import os
import json
import warnings

import numpy as np

from treem.io import SWC, TreemEncoder


def check(args):
    """Checks morphology reconstruction for structural consistency."""
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    data = None
    err = dict()
    while True:
        if not os.path.exists(args.file) or not os.path.isfile(args.file):
            err['no_file'] = [args.file]
            break
        if not args.file.lower().endswith('swc'):
            err['not_swc_ext'] = [args.file.split('.')[-1]]
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                data = np.loadtxt(args.file)
        except ValueError:
            err['not_array'] = [True]
            break
        if data.shape[0] == 0:
            err['no_data'] = [True]
            break
        if len(data.shape) == 1:
            err['single_point'] = [data[SWC.I].astype(int)]
            break
        if data.shape[1] != len(SWC.COLS):
            err['not_swc_cols'] = [data.shape[1]]
            break
        first = data[0]
        if first[SWC.I] != 1:
            err['node1_not_id1'] = [first[SWC.I].astype(int)]
        if first[SWC.P] != -1:
            err['node1_has_parent'] = [first[SWC.P].astype(int)]
        if first[SWC.T] != SWC.SOMA:
            err['node1_not_soma'] = [first[SWC.T].astype(int)]
        soma_nodes = data[data[:, SWC.T] == SWC.SOMA]
        soma_ids = soma_nodes[:, SWC.I].astype(int)
        if len(soma_ids > 1):
            inc = soma_ids[1:] - soma_ids[:-1]
            if not (inc == 1).all():
                err['non_sequential_soma_ids'] = soma_ids[np.where(inc != 1)[0] + 1]
        types = set(data[:, SWC.T].astype(int))
        if not types.issubset(SWC.TYPES):
            err['not_valid_types'] =\
                [data[x][SWC.I].astype(int)
                 for t in types.difference(SWC.TYPES)
                 for x in np.where(data[:, SWC.T] == t)[0]]
        ids = data[:, SWC.I].astype(int)
        if not (ids > 0).all():
            err['not_valid_ids'] = ids[ids <= 0]
            break
        idp = data[1:, SWC.P].astype(int)
        if not (idp > 0).all():
            err['not_valid_parent_ids'] = ids[1:][idp <= 0]
            break
        ids_set = set(ids)
        idp_set = set(idp)
        if len(ids_set) != len(ids):
            seen = set()
            err['non_unique_ids'] =\
                {x for x in ids if x in seen or seen.add(x)}
            break
        if not idp_set.issubset(ids_set):
            err['undef_parent_ids'] =\
                [data[x][SWC.I].astype(int)
                 for p in idp_set.difference(ids_set)
                 for x in np.where(data[:, SWC.P] == p)[0]]
            break
        inc = ids[1:] - ids[:-1]
        if not (inc > 0).all():
            err['non_increasing_ids'] = ids[np.where(inc <= 0)[0] + 1]
            break
        if not (inc == 1).all():
            err['non_sequential_ids'] = ids[np.where(inc != 1)[0] + 1]
            break
        if not (ids[1:] > idp).all():
            err['non_descendant'] = ids[np.where(ids[1:] <= idp)[0] + 1]
            break
        if [data[x][SWC.I].astype(int) for t in types.difference([1])
                for x in np.where(data[:, SWC.T] == t)[0][:1]
                if data[x][SWC.P] != 1]:
            err['non_stem_neurite'] =\
                [data[x][SWC.I].astype(int)
                 for t in types.difference([1])
                 for x in np.where(data[:, SWC.T] == t)[0][:1]
                 if data[x][SWC.P] != 1]
        break

    if not args.quiet:
        for k in err:
            print(f'{k}:', end=' ')
            print(*err[k])

    if args.out:
        with open(args.out, 'w') as f:  # pylint: disable=invalid-name
            json.dump(err, f, cls=TreemEncoder)

    return len(err)

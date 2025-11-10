"""Implementation of CLI check command."""

import os
import json
import warnings

import numpy as np

from treem.io import SWC, TreemEncoder


def _load_data(path, err):
    """Tries to load data from SWC file."""
    data = None
    if not os.path.exists(path) or not os.path.isfile(path):
        err["no_file"] = [path]
    elif not path.lower().endswith("swc"):
        err["not_swc_ext"] = [path.split(".")[-1]]
    else:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                data = np.loadtxt(path)
                if data.shape[0] == 0:
                    err["no_data"] = [True]
                    data = None
                elif len(data.shape) == 1:
                    err["single_point"] = [data[SWC.I].astype(int)]
                    data = None
                elif data.shape[1] != len(SWC.COLS):
                    err["not_swc_cols"] = [data.shape[1]]
                    data = None
        except ValueError:
            err["not_array"] = [True]
            data = None
    return data


def _node1_not_id1(data, err):
    first = data[0]
    if first[SWC.I] != 1:
        err["node1_not_id1"] = [first[SWC.I].astype(int)]


def _node1_has_parent(data, err):
    first = data[0]
    if first[SWC.P] != -1:
        err["node1_has_parent"] = [first[SWC.P].astype(int)]


def _node1_not_soma(data, err):
    first = data[0]
    if first[SWC.T] != SWC.SOMA:
        err["node1_not_soma"] = [first[SWC.T].astype(int)]


def _non_sequential_soma_ids(data, err):
    soma_nodes = data[data[:, SWC.T] == SWC.SOMA]
    soma_ids = soma_nodes[:, SWC.I].astype(int)
    if len(soma_ids > 1):
        inc = soma_ids[1:] - soma_ids[:-1]
        if not (inc == 1).all():
            err["non_sequential_soma_ids"] = soma_ids[np.nonzero(inc != 1)[0] + 1]


def _not_valid_types(data, err):
    types = set(data[:, SWC.T].astype(int))
    if not types.issubset(SWC.TYPES):
        err["not_valid_types"] = [
            data[x][SWC.I].astype(int)
            for t in types.difference(SWC.TYPES)
            for x in np.nonzero(data[:, SWC.T] == t)[0]
        ]


def _not_valid_ids(data, err):
    ids = data[:, SWC.I].astype(int)
    if not (ids > 0).all():
        err["not_valid_ids"] = ids[ids <= 0]
        return False
    return True


def _not_valid_parent_ids(data, err):
    ids = data[:, SWC.I].astype(int)
    idp = data[1:, SWC.P].astype(int)
    if not (idp > 0).all():
        err["not_valid_parent_ids"] = ids[1:][idp <= 0]
        return False
    return True


def _non_unique_ids(data, err):
    ids = data[:, SWC.I].astype(int)
    ids_set = set(ids)
    if len(ids_set) != len(ids):
        seen = set()
        err["non_unique_ids"] = {x for x in ids if x in seen or seen.add(x)}
        return False
    return True


def _undef_parent_ids(data, err):
    ids = data[:, SWC.I].astype(int)
    idp = data[1:, SWC.P].astype(int)
    ids_set = set(ids)
    idp_set = set(idp)
    if not idp_set.issubset(ids_set):
        err["undef_parent_ids"] = [
            data[x][SWC.I].astype(int)
            for p in idp_set.difference(ids_set)
            for x in np.nonzero(data[:, SWC.P] == p)[0]
        ]
        return False
    return True


def _non_increasing_ids(data, err):
    ids = data[:, SWC.I].astype(int)
    inc = ids[1:] - ids[:-1]
    if not (inc > 0).all():
        err["non_increasing_ids"] = ids[np.nonzero(inc <= 0)[0] + 1]
        return False
    return True


def _non_sequential_ids(data, err):
    ids = data[:, SWC.I].astype(int)
    inc = ids[1:] - ids[:-1]
    if not (inc == 1).all():
        err["non_sequential_ids"] = ids[np.nonzero(inc != 1)[0] + 1]
        return False
    return True


def _non_descendant(data, err):
    ids = data[:, SWC.I].astype(int)
    idp = data[1:, SWC.P].astype(int)
    if not (ids[1:] > idp).all():
        err["non_descendant"] = ids[np.nonzero(ids[1:] <= idp)[0] + 1]
        return False
    return True


def _non_stem_neurite(data, err):
    types = set(data[:, SWC.T].astype(int))
    if [
        data[x][SWC.I].astype(int)
        for t in types.difference([1])
        for x in np.nonzero(data[:, SWC.T] == t)[0][:1]
        if data[x][SWC.P] != 1
    ]:
        err["non_stem_neurite"] = [
            data[x][SWC.I].astype(int)
            for t in types.difference([1])
            for x in np.nonzero(data[:, SWC.T] == t)[0][:1]
            if data[x][SWC.P] != 1
        ]
        return False
    return True


basic_checks = [
    _node1_not_id1,
    _node1_has_parent,
    _node1_not_soma,
    _non_sequential_soma_ids,
    _not_valid_types,
]
while_checks = [
    _not_valid_ids,
    _not_valid_parent_ids,
    _non_unique_ids,
    _undef_parent_ids,
    _non_increasing_ids,
    _non_sequential_ids,
    _non_descendant,
    _non_stem_neurite,
]


def _check_swc(data, err):
    """Checks SWC data for consistency."""
    for _check in basic_checks:
        _check(data, err)
    for _check in while_checks:
        if not _check(data, err):
            break


def check(args):
    """Checks morphology reconstruction for structural consistency."""
    err = {}
    data = _load_data(args.file, err)
    if data is not None:
        _check_swc(data, err)

    if not args.quiet:
        for condition in err:
            print(f"{condition}:", end=" ")
            print(*err[condition])

    if args.out:
        with open(args.out, "w", encoding="utf-8") as file:
            json.dump(err, file, cls=TreemEncoder)

    return len(err)

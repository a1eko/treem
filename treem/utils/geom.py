"""Utilities for manipulating geometry of morphology reconstructions."""

import math
import numpy as np

from treem.io import SWC

# pylint: disable=invalid-name
# pylint: disable=too-many-locals


def rotation_matrix(axis, angle):
    """Computes rotation matrix for 3D manipulations.

    Args:
        axis (float[3]): rotation axis.
        angle (float): rotation angle in radians.

    Returns:
        rotation matrix (NumPy ndarray).
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(angle / 2.0)
    b, c, d = -axis * math.sin(angle / 2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa + bb - cc - dd, 2*(bc + ad), 2*(bd - ac)],
                     [2*(bc - ad), aa + cc - bb - dd, 2*(cd + ab)],
                     [2*(bd + ac), 2*(cd - ab), aa + dd - bb - cc]])


def norm(vec):
    """Returns magnitude of a 3D vector."""
    x, y, z = vec
    return math.sqrt(x*x + y*y + z*z)


def angle_between(u, v):
    """Returns angle in radians between two 3D vectors (float[3])."""
    un, vn, = norm(u), norm(v)
    angle = math.acos(np.dot(u, v) / (un*vn)) if un > 1e-6 and vn > 1e-6 else 0
    return angle


def rotation(u, v):
    """Computes rotation axis and angle for two 3D vectors (float[3]).

    Returns:
        axis (NumPy ndarray[3]), angle (float)

        rotation axis, rotation angle in radians.
    """
    angle = angle_between(u, v)
    if math.isclose(math.sin(angle), 0, abs_tol=1e-6):
        dv = np.ones(3)*1e-6
        u, v = u + dv, v - dv
    axis = np.cross(u, v)
    axis = axis / norm(axis)
    return axis, angle


def repair_branch(cmorph, cut, rmorph, rep, force=False, keep_radii=False):
    """Attempts to extend cut neurite using intact branch.

    Args:
        cmorph (treem.Morph): cut morphology.
        cut (treem.Node): cut node, from cmorph.
        rmorph (treem.Morph): repair morphology.
        rep (treem.Node): undamaged branch start node, from rmorph.
        force (bool): force repair if branch is too short.
        keep_radii (bool): do not scale radii of repaired branch.

    Returns:
        True if repaired.
    """
    # pylint: disable=too-many-arguments
    done = 0
    cutsec = list(reversed(list(cut.section(reverse=True))))
    repsec = list(rep.section())
    cutlen = cmorph.length(cutsec)
    replen = rmorph.length(repsec)
    target = cut
    if replen > cutlen:
        for node in repsec[-1::-1]:
            if rmorph.length(node.section()) > replen - cutlen:
                break
        source = node  # pylint: disable=undefined-loop-variable
    elif rep.breadth() > 1 or force:
        source = rep
    else:
        source = None
    if source:
        tree = rmorph.copy(source)
        scale_z = -1
        if keep_radii:
            scale_r = 1
        else:
            # possibly unsafe use of memory block in radii() may cause errors in swc-repair
            #rcut = cmorph.radii(cutsec).mean()
            #rrep = rmorph.radii(repsec).mean()
            rcut = np.mean([node.radius() for node in cutsec])
            rrep = np.mean([node.radius() for node in repsec])
            scale_r = rcut / rrep
        tree.data[:, SWC.XYZR] *= np.array([1, 1, scale_z, scale_r])
        u = np.mean(tree.data[:, SWC.XYZ], axis=0) - tree.root.coord()
        v = target.coord() - cmorph.root.coord()
        axis, angle = rotation(u, v)
        tree.rotate(axis, angle)
        shift = (target.coord() - tree.root.coord() +
                 target.coord() - target.parent.coord())
        tree.translate(shift)
        cmorph.graft(tree, target)
        done = 1
    return done


def sample(points, num):
    """Samples points with fixed resolution using linear interpolation.

    Args:
        points (NumPy ndarray[4]): array of 4D data points (x,y,z,r).
        num (int): sample size.

    Returns:
        array of 4D points (NumPy ndarray[4]).
    """
    num = num if num > 1 else 2
    links = [norm(p[0:3] - q[0:3]) for p, q in zip(points[:-1], points[1:])]
    tp = [sum(links[0:i]) for i in range(len(links)+1)]
    xp, yp, zp, rp = points.T
    t = np.linspace(tp[0], tp[-1], num, endpoint=True)
    return np.array([np.interp(t, tp, xp),
                     np.interp(t, tp, yp),
                     np.interp(t, tp, zp),
                     np.interp(t, tp, rp)]).T


def fibonacci_sphere(npoints=100):
    """Samples equally spaced points on a unit sphere.

    Args:
        npoints (int): sample size [100].

    Returns:
        array of 3D points (NumPy ndarray[3]).
    """
    indices = np.arange(0, npoints, dtype=float) + 0.5
    phi = np.arccos(1 - 2 * indices / npoints)
    theta = np.pi * (1 + 5**0.5) * indices
    x = np.cos(theta) * np.sin(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(phi)
    points = np.array([x, y, z]).T
    return points

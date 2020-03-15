"""
NiBabel <-> ITK orientation and affine conversion utilities.
The conventions of nibabel and itk are different and this module supplies functions which convert between
these conventions.

Orientation
-----------
In nibabel each axis code indicates the ending direction - RAS+: L -> R, P -> A, I -> S
In itk it corresponds to the converse of nibabel - RAS: R -> L, A -> P, S -> I

Affine
------
In itk, the direction matrix (3x3 upper left affine with unit spacings) of RAS orientation image is:
[[1, 0, 0],
 [0, 1, 0],
 [0, 0, -1]]

In nibabel it is LPI+:
[[-1, 0, 0],
 [0, -1, 0],
 [0, 0, -1]]

The matrix convert_aff_mat accounts for this difference (for all possible orientations, not only RAS).

Usage
=====
Works both ways: itk -> nib and nib -> itk, the usage is the same:
>>> new_affine, new_axcodes = convert(affine, axcodes)
"""

import numpy as np
from utils.two_way_dict import TwoWayDict
from img_io.affine import Affine


# store compactly axis directions codes
axes_inv = TwoWayDict()
axes_inv['R'] = 'L'
axes_inv['A'] = 'P'
axes_inv['S'] = 'I'


def inv_axcodes(axcodes):
    """Inverse axes codes chars, for example: SPL -> IAR"""
    if axcodes is None:
        return None
    new_axcodes = ''
    for code in axcodes:
        new_axcodes += axes_inv[code]
    return new_axcodes


def convert_affine(affine):
    # conversion matrix of the affine from itk to nibabel and vice versa
    convert_aff_mat = np.diag([-1, -1, 1, 1])
    new_affine = convert_aff_mat @ affine
    if isinstance(affine, Affine):
        new_affine = Affine(new_affine)
    return new_affine


def convert(affine, axcodes):
    """Convert affine and meta data dictionary (original orientation) from nibabel to itk and vice versa"""
    new_affine = convert_affine(affine)
    new_axcodes = inv_axcodes(axcodes)

    return new_affine, new_axcodes
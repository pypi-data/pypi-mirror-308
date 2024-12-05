"""Functions for slicing circuit files to place specific cells only."""

import logging

import numpy as np
import pandas as pd
from region_grower.atlas_helper import AtlasHelper
from voxcell.exceptions import VoxcellError
from voxcell.nexus.voxelbrain import Atlas

from neurocollage.exceptions import NeurocollageException
from neurocollage.planes_utils.planes import _smoothing
from neurocollage.planes_utils.planes import create_centerline
from neurocollage.planes_utils.planes import create_planes as _create_planes

L = logging.getLogger(__name__)
LEFT = "left"
RIGHT = "right"


def halve_atlas(annotated_volume, axis=2, side=LEFT):
    """Return the half of the annotated volume along the x-axis.

    The identifiers of the voxels located on the left half or the right half
    of the annotated volume are zeroed depending on which `side` is chosen.

    Args:
        annotated_volume: integer array of shape (W, L, D) holding the annotation
            of a brain region.
        axis: (Optional) axis along which to halve. Either 0, 1 or 2.
            Defaults to 2.
        side: (Optional) Either 'left' or 'right', depending on which half is requested.
            Defaults to LEFT.

    Returns:
        Halves `annotated_volume` where where voxels on the opposite `side` have been
        zeroed (black).
    """
    assert axis in range(3)
    assert side in [LEFT, RIGHT]

    middle = annotated_volume.shape[axis] // 2
    slices_ = [slice(0), slice(0), slice(0)]
    for coord in range(3):
        if axis == coord:
            slices_[coord] = (
                slice(0, middle) if side == RIGHT else slice(middle, annotated_volume.shape[axis])
            )
        else:
            slices_[coord] = slice(0, annotated_volume.shape[coord])
    annotated_volume[slices_[0], slices_[1], slices_[2]] = 0
    return annotated_volume


def slice_per_mtype(cells, mtypes):
    """Selects cells of given mtype."""
    return cells[cells["mtype"].isin(mtypes)]


def slice_n_cells(cells, n_cells, random_state=0):
    """Selects n_cells random cells per mtypes."""
    if n_cells <= 0:
        return cells

    sampled_cells = []
    for mtype in cells.mtype.unique():
        samples = cells[cells.mtype == mtype].sample(
            n=min(n_cells, len(cells[cells.mtype == mtype])), random_state=random_state
        )
        sampled_cells.append(samples)

    if len(sampled_cells) > 0:
        return pd.concat(sampled_cells)
    return pd.DataFrame()


def get_cells_between_planes(cells, plane_left, plane_right):
    """Gets cells gids between two planes in equation representation."""
    eq_left = plane_left.get_equation()
    eq_right = plane_right.get_equation()
    left = np.einsum("j,ij", eq_left[:3], cells[["x", "y", "z"]].values)
    right = np.einsum("j,ij", eq_right[:3], cells[["x", "y", "z"]].values)
    selected = (left > eq_left[3]) & (right < eq_right[3])
    return cells.loc[selected]


def _get_principal_direction(points):
    """Return the principal direction of a point cloud.

    It is the eigen vector of the covariance matrix with the highest eigen value.
    Taken from neuror.unravel.
    """
    X = np.copy(np.asarray(points))
    X -= np.mean(X, axis=0)
    C = np.dot(X.T, X)
    w, v = np.linalg.eig(C)
    return v[:, w.argmax()]


def get_centerline_bounds(layer):
    """Find centerline bounds using PCA of the voxell position of a given layer in the region."""
    _ls = np.unique(layer.raw[layer.raw > 0])
    central_layer = _ls[int(len(_ls) / 2)]

    # we select voxels which are on the boundary of the region, to prevent picking them in y dir
    layer_raw = np.array(layer.raw, dtype=float)
    layer_raw[layer_raw == 0] = -10000  # large number to be safe
    boundary_mask = sum(abs(g) for g in np.gradient(layer_raw)) > 1000
    ids = np.column_stack(np.where((layer.raw == central_layer) & boundary_mask))
    points = layer.indices_to_positions(ids)
    _align = points.dot(_get_principal_direction(points))
    return ids[_align.argmin()], ids[_align.argmax()]


def get_local_bbox(annotation):
    """Compute bbox where annotation file is strictly positive."""
    ids = np.where(annotation.raw > 0)
    dim = annotation.voxel_dimensions
    return annotation.offset + np.array(
        [np.min(ids, axis=1) * dim, (np.max(ids, axis=1) + 1) * dim]
    )


def create_planes(
    layer_annotation,
    plane_type="aligned",
    plane_count=10,
    slice_thickness=100,
    centerline_first_bound=None,
    centerline_last_bound=None,
    centerline_axis=0,
    seed=42,
):  # pylint:disable=too-many-branches,too-many-locals
    """Create planes in an atlas.

    We create 3 * plane_count such each triplet of planes define the left, center
    and right plane of each slice.

    Args:
        layer_annotation (VoxelData): annotations with layers
        plane_type (str): type of planes creation algorithm, two choices:

            * centerline_straight: centerline is straight between _first_bound and _last_bound
            * centerline_curved: centerline is curved with algorithm from atlas-analysis package
            * aligned: centerline is a straight line, along the centerline_axis

        plane_count (int): number of planes to create slices of atlas,
        slice_thickness (float): thickness of slices (in micrometer)
        centerline_first_bound (list): (for plane_type == centerline) location of first bound
            for centerline (in voxcell index)
        centerline_last_bound (list): (for plane_type == centerline) location of last bound
            for centerline (in voxcell index)
        centerline_axis (str): (for plane_type = aligned) axis along which to create planes
        seed (int): fix seed for centerline creation
    """
    if plane_type == "centerline_straight":
        if centerline_first_bound is None and centerline_last_bound is None:
            centerline_first_bound, centerline_last_bound = get_centerline_bounds(
                layer_annotation["annotation"]
            )
        if isinstance(centerline_first_bound[0], (int, np.integer)):
            centerline = np.array(
                [
                    layer_annotation["annotation"].indices_to_positions(centerline_first_bound),
                    layer_annotation["annotation"].indices_to_positions(centerline_last_bound),
                ]
            )
        else:
            centerline = np.array([centerline_first_bound, centerline_last_bound])

    elif plane_type == "centerline_curved":
        if centerline_first_bound is None and centerline_last_bound is None:
            centerline_first_bound, centerline_last_bound = get_centerline_bounds(
                layer_annotation["annotation"]
            )
        if not isinstance(centerline_first_bound[0], (int, np.integer)):
            bounds = [
                layer_annotation["annotation"].positions_to_indices(centerline_first_bound),
                layer_annotation["annotation"].positions_to_indices(centerline_last_bound),
            ]
        else:
            bounds = [centerline_first_bound, centerline_last_bound]

        np.random.seed(seed)
        centerline = create_centerline(layer_annotation["annotation"], bounds)
        centerline = _smoothing(centerline)

    elif plane_type == "aligned":
        centerline = np.zeros([2, 3])
        bbox = get_local_bbox(layer_annotation["annotation"])
        centerline[:, centerline_axis] = np.linspace(
            bbox[0, centerline_axis], bbox[1, centerline_axis], 2
        )
    else:
        raise NeurocollageException(
            f"Please set plane_type to 'aligned' or 'centerline', not {plane_type}."
        )

    # check centerline is in the atlas region
    for point in centerline:
        try:
            layer_annotation["annotation"].lookup(point)
        except VoxcellError as exc:
            raise NeurocollageException(
                "Centerline goes out of atlas region, we better stop here."
            ) from exc

    # create all planes to match slice_thickness between every two planes
    shift = slice_thickness / np.linalg.norm(np.diff(centerline, axis=0), axis=1).sum()
    _plane_count = plane_count
    if plane_count == 1:
        _plane_count = 3

    left_planes = _create_planes(
        centerline, steps=np.clip(np.linspace(0, 1 - 2 * shift, _plane_count), 0, 1)
    )
    center_planes = _create_planes(
        centerline, steps=np.clip(np.linspace(shift, 1 - shift, _plane_count), 0, 1)
    )
    right_planes = _create_planes(
        centerline, steps=np.clip(np.linspace(2 * shift, 1.0, _plane_count), 0, 1)
    )

    if plane_count == 1:
        left_planes = [left_planes[1]]
        right_planes = [right_planes[1]]
        center_planes = [center_planes[1]]

    planes = []
    for l_plane, c_plane, r_plane in zip(left_planes, center_planes, right_planes):
        planes.append({"left": l_plane, "center": c_plane, "right": r_plane})
    return planes, centerline


def get_atlas(atlas_path):
    """Get atlas helper."""
    return AtlasHelper(
        Atlas.open(atlas_path["atlas"]), region_structure_path=atlas_path["structure"]
    )


def get_layer_annotation(atlas_path, region, hemisphere=None):
    """Create a VoxelData with layer annotation."""
    atlas_helper = get_atlas(atlas_path)

    brain_regions = atlas_helper.brain_regions
    layers_data = np.zeros_like(brain_regions.raw, dtype="uint8")

    try:
        region_mask = atlas_helper.atlas.get_region_mask(region).raw
    except AttributeError:
        L.warning("%s does not exists in the atlas, so we do not filter", region)
        region_mask = None

    layer_mapping = {}
    if atlas_helper.layers[region]:
        for layer_id, layer in enumerate(atlas_helper.layers[region]):
            layer_mapping[layer_id] = atlas_helper.region_structure[region]["names"].get(
                layer, str(layer)
            )
            region_query = atlas_helper.region_structure[region]["region_queries"][layer]
            mask = atlas_helper.atlas.get_region_mask(region_query).raw
            if region_mask is not None:
                mask *= region_mask
            layers_data[mask] = layer_id + 1
            if not len(layers_data[mask]):
                L.warning("No voxel found for layer %s.", layer)

    else:
        layer_mapping = {1: region}
        mask = atlas_helper.atlas.get_region_mask(region).raw
        layers_data[mask] = 1
    if hemisphere is not None:
        layers_data = halve_atlas(layers_data, side=hemisphere)

    brain_regions.raw = layers_data
    return {"annotation": brain_regions, "mapping": layer_mapping}

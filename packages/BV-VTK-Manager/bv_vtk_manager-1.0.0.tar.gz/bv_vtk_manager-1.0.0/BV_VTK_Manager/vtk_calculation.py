import vtk
import numpy as np
from vtkmodules.util.numpy_support import vtk_to_numpy


def calcVolumStructuredPointVTK(structuredVTK):
    """
    Calculates the volume of a specific VTK object where points have a scalar value of 1.0 for those to be considered.

    Args:
        structuredVTK (vtkObj): VTK object.

    Returns:
        volume (float): Calculated volume.
    """

    # Get the dimensions of the data
    dims = structuredVTK.GetDimensions()

    # Get the spacing of the data
    spacing = structuredVTK.GetSpacing()

    # Get point scalars
    point_scalars_vtk = structuredVTK.GetPointData().GetScalars()

    if point_scalars_vtk is None:
        raise ValueError("No point scalars found.")

    # Convert point scalars to numpy array
    point_scalars_np = vtk_to_numpy(point_scalars_vtk)

    # Filter points with scalar value of 1.0
    filtered_points = point_scalars_np[point_scalars_np == 1.0]

    # Get the number of points with the scalar value of 1.0
    points_with_value = len(filtered_points)

    # Calculate the point volume
    point_vol = spacing[0] * spacing[1] * spacing[2]

    # Calculate the volume
    volume = point_vol * points_with_value

    print(f"Volume: {volume} m³")

    return volume


def calcVolumeStructuredGridVTK(structuredVTK):
    """
    Calculates the volume of a specific VTK structured grid object where points have a scalar value of 1.0.

    Args:
        structuredVTK (vtkStructuredGrid): VTK structured grid object.

    Returns:
        volume (float): Calculated volume.
    """

    # Get the dimensions of the grid
    dims = structuredVTK.GetDimensions()

    # Calculate the spacing
    extent = structuredVTK.GetExtent()
    spacing = np.array(
        [
            (extent[1] - extent[0]) / (dims[0] - 1),
            (extent[3] - extent[2]) / (dims[1] - 1),
            (extent[5] - extent[4]) / (dims[2] - 1),
        ]
    )

    # Get the point data
    pointData = structuredVTK.GetPointData()

    # Get point scalars
    point_scalars_vtk = pointData.GetScalars()

    if point_scalars_vtk is None:
        raise ValueError("No point scalars found.")

    # Convert point scalars to numpy array
    point_scalars_np = vtk_to_numpy(point_scalars_vtk)

    # Filter points with scalar value of 1.0
    filtered_points = point_scalars_np[point_scalars_np == 1.0]

    # Get the number of points with the scalar value of 1.0
    points_with_value = len(filtered_points)

    # Calculate the point volume
    point_vol = spacing[0] * spacing[1] * spacing[2]

    # Calculate the total volume
    volume = point_vol * points_with_value

    print(f"Volume: {volume} m³")

    return volume
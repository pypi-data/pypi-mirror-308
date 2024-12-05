import vtk
from vtkmodules.util.numpy_support import vtk_to_numpy

def visualizeVTK(VTK):
    """Visualiza um objeto VTK

    Args:
        **VTK (vtkObj):** Objeto VTK
    """

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(VTK)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)

    window = vtk.vtkRenderWindow()
    window.SetSize(800, 600)
    window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.Start()


def verifyPoint(VTKdata):
    """Verifica a quantidade de pontos de um objeto VTK

    Args:
        **VTKdata (objVTK):** Objeto VTK
    """

    # get the VTK data array object containing scalar values associated with the cells
    cell_scalars_vtk = VTKdata.GetCellData().GetScalars()
    cell_scalars_np = vtk_to_numpy(cell_scalars_vtk)

    # get the point coordinates as a numpy array
    points_vtk = VTKdata.GetPointData()

    dims = VTKdata.GetDimensions()
    print("Number of points: ", (dims[0]) * (dims[1]) * (dims[2]))

    print("Number of scalar values: ", len(cell_scalars_np))

    # loop through the cells and print their coordinates
    for i in range(VTKdata.GetNumberOfCells()):
        cell = VTKdata.GetCell(i)
        print(cell.GetPointIds().GetId(7))
        print(f"Cell {i}: {cell.GetPoints().GetData()}")

    points_np = vtk_to_numpy(points_vtk.GetData())

    # print (points_vtk)
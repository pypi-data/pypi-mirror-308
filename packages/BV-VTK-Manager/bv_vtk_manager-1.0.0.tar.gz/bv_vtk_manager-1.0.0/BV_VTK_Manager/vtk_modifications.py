import vtk
from vtkmodules.util.numpy_support import vtk_to_numpy

def applyThreshold(VTKdata, lower=0.0, upper=1.0):
    """Aplica o filtro threshold em um objeto VTK

    Args:
        **VTKdata (objVTK):** Objeto VTK\n
        **lower (float, optional):** Limite inferior para o filtro. Defaults to 0.0.\n
        **upper (float, optional):** Limite superior para o filtro. Defaults to 1.0.\n

    Returns:
        **threshold (objVTK):** Objeto VTK com o filtro threshold aplicado
    """

    # Create the threshold filter and set its parameters - MISS STRUCTURED GRID..
    threshold = vtk.vtkThreshold()
    threshold.SetInputData(VTKdata)
    threshold.SetUpperThreshold(lower)
    threshold.SetLowerThreshold(upper)
    threshold.Update()

    return threshold.GetOutput()


def convertVTKScalar_to_npData(VTKdata):
    """Converte um objeto VTK em uma nuvem de pontos no formato numpy

    Args:
        **VTKdata (objVTK):** Objeto VTK

    Returns:
        **npScalars (list-Numpy):** Nuvem de pontos
    """

    vtkScalars = VTKdata.GetCellData().GetScalars()
    npScalars = vtk_to_numpy(vtkScalars)

    return npScalars

def list_to_vtk(pontos, caminho):

    # Criar um objeto VTK para armazenar os pontos
    pontos_vtk = vtk.vtkPoints()

    # Adicionar os pontos à estrutura VTK
    for p in pontos:
        pontos_vtk.InsertNextPoint(p[0], p[1], p[2])

    # Criar um objeto VTK para armazenar as células (neste caso, pontos individuais)
    celulas = vtk.vtkCellArray()

    # Adicionar as células ao objeto VTK
    for i in range(len(pontos)):
        celulas.InsertNextCell(1)
        celulas.InsertCellPoint(i)

    # Criar uma estrutura VTK do tipo "PolyData" e associar os pontos e células
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(pontos_vtk)
    polydata.SetVerts(celulas)

    # Salvar o arquivo VTK
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(caminho)
    writer.SetInputData(polydata)
    writer.Write()

from vtk_own_structure import vtk_obj

import vtk
from vtkmodules.util.numpy_support import vtk_to_numpy
import pyvista as pv
import numpy as np


def genVTK_Faces(vtk_own_structure, outputPath):
    # Cria o objeto de poliedro do VTK
    vtk_polydata = vtk.vtkPolyData()

    # Cria o objeto de pontos do VTK
    vtk_points = vtk.vtkPoints()

    # Cria o objeto de polígonos do VTK
    vtk_polygons = vtk.vtkCellArray()

    # Adiciona os pontos, polígonos e dados escalares
    for point in vtk_own_structure.points:
        point_id = vtk_points.InsertNextPoint(point)

    # Define os Pontos do objeto VTK
    vtk_polydata.SetPoints(vtk_points)

    for cell in vtk_own_structure.cells:
        num_points = cell[0]
        polygon = [int(point) for point in cell[1:]]
        vtk_polygons.InsertNextCell(num_points, polygon)

    # Define as Faces do objeto VTK
    vtk_polydata.SetPolys(vtk_polygons)

    for scalarName, scalarValues in vtk_own_structure.scalarPoints.items():
        vtk_scalar = vtk.vtkDoubleArray()
        vtk_scalar.SetName(scalarName)
        vtk_scalar.SetNumberOfComponents(
            1
        )  # Define o número de componentes como 1 para um scalar

        for scalar in scalarValues:
            vtk_scalar.InsertNextValue(scalar)

        vtk_polydata.GetPointData().AddArray(vtk_scalar)

    # Cria o escritor VTK para gerar o arquivo .vtk
    vtk_writer = vtk.vtkPolyDataWriter()
    vtk_writer.SetFileName(f"{outputPath}")
    vtk_writer.SetInputData(vtk_polydata)
    vtk_writer.Write()

def genVTK_points(vtk_own_structure, outputPath):
    # Cria o objeto de pontos do VTK
    vtk_points = vtk.vtkPoints()

    # Cria o objeto de poliedro do VTK
    vtk_polydata = vtk.vtkPolyData()

    # Adiciona os pontos ao objeto de pontos do VTK
    for point in vtk_own_structure.points:
        vtk_points.InsertNextPoint(point)

    # Define os Pontos do objeto VTK
    vtk_polydata.SetPoints(vtk_points)

    # Cria o objeto de polígonos do VTK
    vtk_polygons = vtk.vtkCellArray()

    # Adiciona os polígonos ao objeto de polígonos do VTK
    for i in range(len(vtk_own_structure.points)):
        vtk_polygons.InsertNextCell(1)
        vtk_polygons.InsertCellPoint(i)

    # Define os Poligonos do objeto VTK
    vtk_polydata.SetVerts(vtk_polygons)

    # Cria o objeto de dados escalares do VTK
    for scalarName, scalarValues in vtk_own_structure.scalarPoints.items():
        vtk_scalar = vtk.vtkDoubleArray()
        vtk_scalar.SetName(scalarName)
        vtk_scalar.SetNumberOfComponents(
            1
        )  # Define o número de componentes como 1 para um scalar

        for scalar in scalarValues:
            vtk_scalar.InsertNextValue(scalar)

        # Define os dados escalares no objeto de poliedro do VTK
        vtk_polydata.GetPointData().AddArray(vtk_scalar)

    # Cria o escritor VTK para gerar o arquivo .vtk
    vtk_writer = vtk.vtkPolyDataWriter()
    vtk_writer.SetFileName(f"{outputPath}")
    vtk_writer.SetInputData(vtk_polydata)
    vtk_writer.Write()


def create_structured_grid_vtk_file(
    points: list,
    dimensions: list,
    valores_scalares: dict,
    caminho_saida: str,
    nome_arquivo: str,
    binario: bool = False,
):
    # Create a vtkStructuredGrid
    structuredGrid = vtk.vtkStructuredGrid()

    # Set the dimensions of the structured grid
    structuredGrid.SetDimensions(dimensions)

    # Create a vtkPoints object and assign the list of points to it
    pointsObj = vtk.vtkPoints()
    for point in points:
        pointsObj.InsertNextPoint(point)

    # Set the points for the structured grid
    structuredGrid.SetPoints(pointsObj)

    # Cria o objeto de dados escalares do VTK
    for scalarName, scalarValues in valores_scalares.items():
        vtk_scalar = vtk.vtkDoubleArray()
        vtk_scalar.SetName(scalarName)
        vtk_scalar.SetNumberOfComponents(
            1
        )  # Define o número de componentes como 1 para um scalar

        for scalar in scalarValues:
            vtk_scalar.InsertNextValue(scalar)

        structuredGrid.GetPointData().AddArray(vtk_scalar)

    # Create a vtkStructuredGridWriter to write the VTK file
    writer = vtk.vtkStructuredGridWriter()
    writer.SetFileName(f"{caminho_saida}\{nome_arquivo}.vtk")

    if binario:
        writer.SetFileTypeToBinary()

    writer.SetInputData(structuredGrid)

    # Write the VTK file
    writer.Write()

def create_structured_point_vtk_file(
    dimensions: list,
    origem: list,
    espacamento: list,
    valores_scalares: dict,
    caminho_saida: str,
    nome_arquivo: str,
    binario: bool = False,
):
    # Create a vtkStructuredPoints object
    structuredPoints = vtk.vtkStructuredPoints()

    # Set the dimensions, origin, and spacing of the structured points
    structuredPoints.SetDimensions(dimensions)
    structuredPoints.SetOrigin(origem)  # Defina a origem conforme necessário
    structuredPoints.SetSpacing(
        espacamento
    )  # Defina o espaçamento conforme necessário

    # Create a vtkFloatArray to store scalar values
    for scalarName, scalarValues in valores_scalares.items():
        vtk_scalar = vtk.vtkFloatArray()
        vtk_scalar.SetName(scalarName)
        vtk_scalar.SetNumberOfComponents(1)

        for scalar in scalarValues:
            vtk_scalar.InsertNextValue(scalar)

        structuredPoints.GetPointData().SetScalars(vtk_scalar)

    # Create a vtkStructuredPointsWriter to write the VTK file
    writer = vtk.vtkStructuredPointsWriter()
    writer.SetFileName(f"{caminho_saida}/{nome_arquivo}.vtk")

    if binario:
        writer.SetFileTypeToBinary()

    writer.SetInputData(structuredPoints)

    # Write the VTK file
    writer.Write()

def criar_vtk_tipo_pontos(
    lista_pontos: list, valores_scalares: dict, caminho_saida: str
) -> None:
    """_summary_

    Args:
        lista_pontos (list): _description_
        valores_scalares (dict): _description_
        caminho_saida (str): _description_
    """
    vtk_objeto = vtk_obj()

    vtk_objeto.setPoints(lista_pontos)

    for key, value in valores_scalares.items():
        vtk_objeto.setScalarPoints(key, value)

    vtk_objeto.genVTK_points(caminho_saida)

def criar_vtk_tipo_faces(
    lista_pontos: list,
    lista_faces: list,
    valores_scalares: dict,
    caminho_saida: str,
) -> None:
    """_summary_

    Args:
        lista_pontos (list): _description_
        lista_faces (list): _description_
        valores_scalares (dict): _description_
        caminho_saida (str): _description_
    """

    vtk_objeto = vtk_obj()

    vtk_objeto.setPoints(lista_pontos)

    vtk_objeto.setCells(lista_faces)

    if valores_scalares != None:
        for key, value in valores_scalares.items():
            vtk_objeto.setScalarPoints(key, value)

    vtk_objeto.genVTK_Faces(caminho_saida)

def mesh_with_cloud_points(lista_pontos: list, caminho_saida: str):
    np_lista_pontos = np.array(lista_pontos)
    cloud = pv.PolyData(np_lista_pontos)

    mesh = cloud.delaunay_3d(7)
    mesh.save(caminho_saida)

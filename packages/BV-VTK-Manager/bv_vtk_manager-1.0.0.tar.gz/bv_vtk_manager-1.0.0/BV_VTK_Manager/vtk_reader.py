import vtk

# from vtk.util import numpy_support
from vtkmodules.util.numpy_support import vtk_to_numpy
import pandas as pd


def verify_type_vtk(path_vtk):
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName(path_vtk)
    reader.Update()

    # Inicializando variáveis para armazenar o tipo e a saída do arquivo VTK
    vtk_type = None

    # Verificando cada tipo de arquivo VTK
    if reader.IsFileStructuredGrid():
        vtk_type = "StructuredGrid"
    elif reader.IsFilePolyData():
        vtk_type = "PolyData"
    elif reader.IsFileRectilinearGrid():
        vtk_type = "RectilinearGrid"
    elif reader.IsFileStructuredPoints():
        vtk_type = "StructuredPoints"
    elif reader.IsFileUnstructuredGrid():
        vtk_type = "UnstructuredGrid"
    else:
        print("O arquivo VTK não corresponde a nenhum tipo VTK conhecido.")
        return None

    # Retornando o tipo e o output correspondente
    return vtk_type

def read_vtk (path_vtk):

    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName(path_vtk)
    reader.Update()

    # Inicializando vtks
    vtk_obj = None

    # Verificacao do tipo 
    vtk_type = verify_type_vtk(path_vtk)

    # Verificando cada tipo de arquivo VTK
    if vtk_type == "StructuredGrid":
        vtk_obj = reader.GetStructuredGridOutput()

    elif vtk_type == "PolyData":
        vtk_obj = reader.GetPolyDataOutput()

    elif vtk_type == "RectilinearGrid":
        vtk_obj = reader.GetRectilinearGridOutput()

    elif vtk_type == "StructuredPoints":
        vtk_obj = reader.GetStructuredPointsOutput()

    elif vtk_type == "UnstructuredGrid":
        vtk_obj = reader.GetUnstructuredGridOutput()

    else:
        print("O arquivo VTK não corresponde a nenhum tipo VTK conhecido.")
        return None

    # Retornando o tipo e o output correspondente
    return vtk_obj, vtk_type

def get_scalar_names(vtk_obj):
    # Obtém os dados de pontos e de células do objeto VTK
    point_data = vtk_obj.GetPointData()
    cell_data = vtk_obj.GetCellData()

    # Listas para armazenar os nomes dos escalares
    scalar_names = {"point_scalars": [], "cell_scalars": []}

    # Adiciona os nomes dos escalares de pontos, se existirem
    if point_data:
        for i in range(point_data.GetNumberOfArrays()):
            array_name = point_data.GetArrayName(i)
            if array_name:
                scalar_names["point_scalars"].append(array_name)

    # Adiciona os nomes dos escalares de células, se existirem
    if cell_data:
        for i in range(cell_data.GetNumberOfArrays()):
            array_name = cell_data.GetArrayName(i)
            if array_name:
                scalar_names["cell_scalars"].append(array_name)

    return scalar_names

def read_scalar(vtk_obj, scalar_name):

    # Acessa os dados de pontos no objeto VTK (valores escalares associados aos pontos)
    point_data = vtk_obj.GetPointData()
    
    # Verifica se o dado escalar está presente
    scalars = point_data.GetScalars(scalar_name)
    if scalars is None:
        print(f"Nao foi encontrado o dado escalar com o nome '{scalar_name}' no arquivo.")
        return None

    # Converte os dados escalares para um array NumPy
    scalar_array = vtk_to_numpy(scalars)
    return scalar_array


def readStructuredGridVTKfile(pathVtk):
    """
    Reads a VTK file with structured grid data and filters based on scalar values.

    Args:
        pathVtk (str): Path to the VTK file.
        progressBar (obj-ProgressBar): Progress bar object.

    Returns:
        structuredVTK (vtkDataSet): VTK dataset object.
        point_locations (DataFrame): DataFrame with the location of each filtered point in the mesh.
    """
    # Read the VTK file
    reader = vtk.vtkStructuredGridReader()
    reader.SetFileName(pathVtk)
    reader.Update()

    structuredVTK = reader.GetOutput()

    # Verificando se houve error
    if reader.GetErrorCode() != 0:
        print(f"Erro ao ler o arquivo: {reader.GetErrorCode()}")
        return None, None

    # Point Locations DataFrame
    point_locations = []

    points = structuredVTK.GetPoints().GetData()
    scalars = structuredVTK.GetPointData().GetScalars()

    for i in range(structuredVTK.GetNumberOfPoints()):
        point = points.GetTuple(i)
        scalarValue = scalars.GetValue(i)

        if scalarValue == 1.0:
            # Extract point coordinates
            x = point[0]
            y = point[1]
            z = point[2]

            point_locations.append({"X": x, "Y": y, "Z": z})

    point_locations = pd.DataFrame(point_locations)

    return structuredVTK, point_locations


def readStructuredPointVTKfile(pathVtk):
    """
    Reads a VTK file with structured point data and filters based on scalar values.

    Args:
        pathVtk (str): Path to the VTK file.
        progressBar (obj-PorgressBar): Progress bar object.

    Returns:
        structuredVTK (vtkObj): VTK object.
        point_locations (DataFrame): DataFrame with the location of each filtered point in the mesh.
    """
    # Read the VTK file
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(pathVtk)
    reader.Update()

    structuredVTK = reader.GetOutput()

    # Convert structured points to unstructured grid
    geometryFilter = vtk.vtkGeometryFilter()
    geometryFilter.SetInputData(structuredVTK)
    geometryFilter.Update()
    unstructuredGrid = geometryFilter.GetOutput()

    # Point Locations DataFrame
    point_locations = []

    spacing = structuredVTK.GetSpacing()
    points = unstructuredGrid.GetPoints().GetData()
    scalars = unstructuredGrid.GetPointData().GetScalars()

    for i in range(unstructuredGrid.GetNumberOfPoints()):
        point = points.GetTuple(i)
        scalarValue = scalars.GetValue(i)

        if scalarValue == 1.0:
            # Extract point coordinates
            x = point[0]
            y = point[1]
            z = point[2]

            point_locations.append(
                {
                    "X": x,
                    "Y": y,
                    "Z": z,
                    "ext_X": spacing[0],
                    "ext_Y": spacing[1],
                    "ext_Z": spacing[2],
                }
            )

    point_locations = pd.DataFrame(point_locations)

    return structuredVTK, point_locations


def obter_pontos_e_valores_escalares_vtk(path_vtk, nome_coluna_scalar):
    # Carregar o arquivo VTK
    reader = vtk.vtkDataSetReader()
    reader.SetFileName(path_vtk)
    reader.Update()
    dataset = reader.GetOutput()

    point_locations = []

    # Verificar se o dataset é 'STRUCTURED_POINTS', 'UNSTRUCTURED_GRID' ou 'STRUCTURED_GRID'
    dataset_type = dataset.GetClassName()
    if dataset_type not in [
        "vtkStructuredPoints",
        "vtkUnstructuredGrid",
        "vtkStructuredGrid",
    ]:
        print("O arquivo VTK possui um tipo de dataset não suportado.")
        return None

    # Obter a lista de pontos e valores escalares
    pontos_e_valores = []
    if dataset_type == "vtkStructuredPoints":
        dimensions = dataset.GetDimensions()
        scalar_array = dataset.GetPointData().GetArray(nome_coluna_scalar)
        for z in range(dimensions[2]):
            for y in range(dimensions[1]):
                for x in range(dimensions[0]):
                    idx = x + y * dimensions[0] + z * dimensions[0] * dimensions[1]
                    point = dataset.GetPoint(idx)
                    scalar = scalar_array.GetValue(idx)
                    pontos_e_valores.append((point, scalar))

                    if scalar == 1.0:
                        # Extract point coordinates
                        xq = point[0]
                        yq = point[1]
                        zq = point[2]

                        point_locations.append({"X": xq, "Y": yq, "Z": zq})
    elif dataset_type == "vtkUnstructuredGrid":
        points = dataset.GetPoints()
        scalar_array = dataset.GetPointData().GetArray(nome_coluna_scalar)
        for i in range(points.GetNumberOfPoints()):
            point = points.GetPoint(i)
            scalar = scalar_array.GetValue(i)
            pontos_e_valores.append((point, scalar))

            if scalar == 1.0:
                # Extract point coordinates
                xq = point[0]
                yq = point[1]
                zq = point[2]

                point_locations.append({"X": xq, "Y": yq, "Z": zq})
    elif dataset_type == "vtkStructuredGrid":
        points = dataset.GetPoints()
        scalar_array = dataset.GetPointData().GetArray(nome_coluna_scalar)
        for i in range(points.GetNumberOfPoints()):
            point = points.GetPoint(i)
            scalar = scalar_array.GetValue(i)
            pontos_e_valores.append((point, scalar))

            if scalar == 1.0:
                # Extract point coordinates
                xq = point[0]
                yq = point[1]
                zq = point[2]

                point_locations.append({"X": xq, "Y": yq, "Z": zq})

    point_locations = pd.DataFrame(point_locations)

    return dataset, point_locations
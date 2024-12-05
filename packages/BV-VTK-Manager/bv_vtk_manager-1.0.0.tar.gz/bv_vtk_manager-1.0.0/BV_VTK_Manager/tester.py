import numpy as np
import vtk_writer
import vtk_reader
import vtk_visualize
import vtk_calculation
import vtk_modifications

# NAO ALTERAR A ESTRUTURA DOS TESTES ANTERIORES, POIS ELES SAO EXEMPLOS DE UTILIZACAO DO CODIGO EM OUTRAS FERRAMENTAS.

#01 : TESTANDO Criar um vtk a partir dos pontos
if (False):
    points = [
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 0),
        (0, 0, 1),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
    ]
    dimensions = (2, 2, 2)  # Replace with your desired dimensions

    valores_escalares_1 = np.random.rand(
        len(points)
    )  # Example: Generate random scalar values
    valores_escalares_2 = np.random.rand(
        len(points)
    )  # Example: Generate random scalar values

    dict_escalares = {"teste_1": valores_escalares_1, "teste_2": valores_escalares_2}

    # Call the function to create the structured grid VTK file
    vtk_writer.create_structured_grid_vtk_file(
        points,
        dimensions,
        dict_escalares,
        r"D:\PROJETOS_FERRAMENTAS\05-BV_FERRAMENTAS\RISS_LOC\.py\RISS_LOC",
        "teste",
    )

#02 : Testando ler um vtk e visualiza-lo

if (True): 

    vtk_obj, vtk_type = vtk_reader.read_vtk(r"TESTER_FOLDER\structured_grid.vtk")
    scalar_names = vtk_reader.get_scalar_names(vtk_obj)

    if (scalar_names == {'point_scalars': ['1_massfractionfuel_0.0', '2_massfractionfuelco2_0.0', '3_massfractionfuelco_0.0', '4_massfractionfuelh2s_0.0', '5_massfractionfuel_3242.0', '6_massfractionfuelco2_3242.0', '7_massfractionfuelco_3242.0', '8_massfractionfuelh2s_3242.0'], 'cell_scalars': []}):
        print ("OK \033[92m\u2714\033[0m - 02 : SCALAR NAMES")
    else:
        print ("ERROR \033[91m\u274C\033[0m - 02 : SCALAR NAMES")

    scalar_array = vtk_reader.read_scalar(vtk_obj, '5_massfractionfuel_3242.0')

    if (scalar_array.sum() == 768.3818):
        print ("OK \033[92m\u2714\033[0m - 02 : READ SCALAR")
    else:
        print ("ERROR \033[91m\u274C\033[0m - 02 : READ SCALAR")

    #thresholdVTK = vtk_modifications.applyThreshold(vtk_obj, 0.1, 1.0)
    #vtk_visualize.visualizeVTK(thresholdVTK)

if (False): #ERROR

    vtk_reader.verify_type_vtk("C:/Users/fpasquetti/Documents/FER/BV_APIs/BV_VTK_Manager/BV_VTK_Manager/TESTER_FOLDER/000011.vtk")
    
    #dataset, point_locations = vtk_reader.obter_pontos_e_valores_escalares_vtk("C:/Users/fpasquetti/Documents/FER/BV_APIs/BV_VTK_Manager/BV_VTK_Manager/TESTER_FOLDER/000011.vtk", "2_massfractionfuelco2_0.0")

    #print (point_locations)

#03 : Verificar o tipo de vtk

if (True): 

    vtk_type = vtk_reader.verify_type_vtk(r"TESTER_FOLDER\structured_grid.vtk")

    if vtk_type == "StructuredGrid":
        print ("OK \033[92m\u2714\033[0m - 03 : VTK STRUCTURED GRID")
    else:
        print ("ERROR \033[91m\u274C\033[0m - 03 : VTK STRUCTURED GRID")

    vtk_type = vtk_reader.verify_type_vtk(r"TESTER_FOLDER\polydata.vtk")

    if vtk_type == "PolyData":
        print ("OK \033[92m\u2714\033[0m - 03 : VTK POLYDATA")
    else:
        print ("ERROR \033[91m\u274C\033[0m - 03 : VTK POLYDATA")

    vtk_type = vtk_reader.verify_type_vtk(r"TESTER_FOLDER\structured_points.vtk")

    if vtk_type == "StructuredPoints":
        print ("OK \033[92m\u2714\033[0m - 03 : VTK STRUCTURED POINTS")
    else:
        print ("ERROR \033[91m\u274C\033[0m - 03 : VTK STRUCTURED POINTS")

    vtk_type = vtk_reader.verify_type_vtk(r"TESTER_FOLDER\unstructured_grid.vtk")

    if vtk_type == "UnstructuredGrid":
        print ("OK \033[92m\u2714\033[0m - 03 : VTK UNSTRUCTURED GRID")
    else:
        print ("ERROR \033[91m\u274C\033[0m - 03 : VTK UNSTRUCTURED GRID")

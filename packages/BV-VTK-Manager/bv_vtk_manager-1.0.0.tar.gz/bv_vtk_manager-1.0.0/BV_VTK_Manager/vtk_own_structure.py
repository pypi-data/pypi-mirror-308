import vtk

class vtk_obj:
    def __init__(self):
        self.lenPoints = 0
        self.lenCells = 0
        self.cellsItems = 0

        self.points = []
        self.cells = []
        self.scalarPoints = {}
        self.scalarCells = {}

    def setPoints(self, pointsList):
        self.point = []

        self.lenPoints = len(pointsList)
        self.points = pointsList

    def setCells(self, cell_corresp_points):
        self.cells = []

        self.lenCells = len(cell_corresp_points)

        for points in cell_corresp_points:
            cell = [len(points)] + points
            self.cellsItems += len(cell)
            self.cells.append(cell)

    def setScalarPoints(self, nameScalar, scalarPoints):
        if len(scalarPoints) != self.lenPoints:
            raise ValueError(
                "Tamanho da lista de valores escalares para os pontos diferente do tamanho da lista de pontos"
            )

        self.scalarPoints[nameScalar] = scalarPoints

    def setScalarCells(self, nameScalar, scalarCells):
        if len(scalarCells) != self.lenCells:
            raise ValueError(
                "Tamanho da lista de valores escalares para as celulas diferente do tamanho da lista de celulas"
            )

        self.scalarCells[nameScalar] = scalarCells

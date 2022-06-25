from PIL import Image


class Row:
    descriptor: list
    combinations: list
    size: int

    def __init__(self, descriptor: list):
        self.descriptor = descriptor
        self.generatePossibleCombinationsForRow()

    def generatePossibleCombinationsForRow(self):
        """Generate all possible combinations for a row. Size is size of
        the row meaning width of horizontal and height for vertical rows."""
        combinations = []
        pixelsInRow = sum(self.descriptor)
        for bitCombination in range(2 ** self.size):
            if bin(bitCombination).count("1") != pixelsInRow:
                continue
            if self.descriptor == generateDescriptor(list(map(lambda x: bool(int(x)),
                                                              list(f"{bitCombination:0{self.size}b}")))):
                combinations.append(list(map(lambda x: bool(int(x)), list(f"{bitCombination:0{self.size}b}"))))
        self.combinations = combinations

    def remove(self, row: list):
        """Row is 0 if low, 1 if high, -1 if unfilled"""
        assert len(row) == self.size
        for i, p in enumerate(row):
            if p == -1:
                continue
            for j in range(len(self.combinations) - 1, -1, -1):
                if self.combinations[j][i] != bool(p):
                    self.combinations.pop(j)

    def getCommons(self):
        """Generate a list of all common values"""
        commons = []
        for pi in range(self.size):
            state = self.combinations[0][pi]
            for c in self.combinations:
                if state != c[pi]:
                    commons.append(-1)
                    break
            if len(commons) < pi:
                commons.append(int(state))
        return commons


class Game:
    img: Image.Image
    pix = None
    descriptorsX: list
    descriptorsY: list
    rowsX: list
    rowsY: list
    width: int
    height: int

    def __init__(self, descriptorsX, descriptorsY, width, height):
        self.descriptorsX = descriptorsX
        self.descriptorsY = descriptorsY
        self.width = width
        self.height = height
        Row.size = width
        self.rowsX = []
        self.rowsY = []
        for x in descriptorsX:
            self.rowsX.append(Row(x))
        Row.size = height
        for y in descriptorsY:
            self.rowsY.append(Row(y))
        self.img = Image.new("L", (width, height), 128)
        self.pix = self.img.load()

    def solve(self):
        while True:
            for y, r in enumerate(self.rowsX):
                r.remove(self.getRow(y))
                if len(r.combinations) == 1:
                    self.plotRow(r.combinations[0], y)
                else:
                    self.plotRow(r.getCommons(), y)
            for x, c in enumerate(self.rowsY):
                c.remove(self.getColumn(x)) # remove removes to much: debug getColumn function and remove function
                if len(c.combinations) == 1:
                    self.plotColumn(c.combinations[0], x)
                else:
                    self.plotColumn(c.getCommons(), x)
            self.img.save("temp.png")

    def getRow(self, y):
        t = []
        for x in range(self.width):
            p = self.pix[x, y]
            t.append(-1 if p == 128 else int(p / 255))
        return t

    def getColumn(self, x):
        t = []
        for y in range(self.height):
            p = self.pix[x, y]
            t.append(-1 if p == 128 else int(p / 255))
        return t

    def plotRow(self, row, y):
        for x, v in enumerate(row):
            if v == 1:
                self.pix[x, y] = 255
            elif v == 0:
                self.pix[x, y] = 0

    def plotColumn(self, column, x):
        for y, v in enumerate(column):
            if v == 1:
                self.pix[x, y] = 255
            elif v == 0:
                self.pix[x, y] = 0


def generateDescriptor(row: list):
    """Generate a row descriptor from a list of pixels"""
    descriptor = []
    i = 0
    for p in row:
        if p:
            i += 1
        if not p and i > 0:
            descriptor.append(i)
            i = 0
    if i != 0:
        descriptor.append(i)
    if len(descriptor) == 0:
        return [0]
    return descriptor


if __name__ == '__main__':
    g = Game([[2], [2]], [[2], [2]], 2, 2)
    g.solve()

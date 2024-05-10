class MatrizDispersa:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def print_matrix(self):
        for row in self.data:
            print(row)

    def to_coo(self):
        coo_data = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.data[i][j] != 0:
                    coo_data.append((i, j, self.data[i][j]))
        return coo_data

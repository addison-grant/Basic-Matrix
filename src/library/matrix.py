from typing import Sequence, Union
from types import NoneType
import array
import math
import collections.abc
import itertools

class Matrix(collections.abc.Mapping):
    def __init__(self, nrow: int, ncol: int, data: Sequence=None):
        self.shape = (nrow, ncol)
        self.item_count = int(math.prod(self.shape))
        self.internal_data = array.array('d')

        iterator = iter(data if data else [])
        for i in range(self.item_count):
            try:
                self.internal_data.append(next(iterator))
            except:
                self.internal_data.append(0)

    def construct_range(self, dim: int, input_range: Union[tuple[Union[int | slice], Union[int | slice] | NoneType]]):
        if input_range == None:
            output_range = range(dim)
        elif isinstance(input_range, slice):
            output_range = range(input_range.start or 0, input_range.stop or dim, input_range.step or 1)
        elif isinstance(input_range, int):
            output_range = [input_range]
        else:
            raise KeyError("Matrix key must be of type int or slice")
        return output_range

    def __getitem__(self, key: Union[tuple[Union[int | slice], Union[int | slice] | NoneType]]):
        rows, cols = key

        nrows, ncols = self.shape
        row_range = self.construct_range(nrows, rows)
        col_range = self.construct_range(ncols, cols)
        
        cols_per_row = self.shape[1]
        data = []
        nrow, ncol = 0, 0
        for i in row_range:
            nrow += 1
            for j in col_range:
                data.append(self.internal_data[i * cols_per_row + j])
        if len(data) == 1:
            return next(iter(data))
        ncol = int(len(data) / nrow)
        return Matrix(nrow, ncol, data)

    def __iter__(self):
        pass

    def __len__(self):
        return self.item_count

    def __str__(self):
        item_str = "{: >9g}"
        nrow, ncol = self.shape
        format_lines = []
        for row in range(nrow):
            line = []
            for col in range(ncol):
                line.append(item_str.format(self.internal_data[row*ncol + col]))
            format_lines.append(" ".join(line))
        return "\n".join(format_lines)

    def __eq__(self, other):
        return self.shape == other.shape and self.internal_data == other.internal_data

    def dot(self, w):
        return sum(x*y for x,y in zip(self.internal_data, w.internal_data))

    def __mul__(self, M):
        nrow1, ncol1 = self.shape
        nrow2, ncol2 = M.shape
        if ncol1 != nrow2:
            raise ValueError("Matrix dimensions not compatible for multiplication")

        data = []
        for i in range(nrow1):
            row = self[i,:]
            for j in range(ncol2):
                col = M[:, j]
                data.append(row.dot(col))
        
        return Matrix(nrow1, ncol2, data)

    def transpose(self):
        nrow, ncol = self.shape
        tnrow, tncol = ncol, nrow
        
        transposed_indexes = itertools.product(range(tnrow), range(tncol))
        transposed = Matrix(tnrow, tncol)
        transposed.internal_data = []
        for i in transposed_indexes:
            transposed.internal_data.append(self[reversed(i)])
        return transposed

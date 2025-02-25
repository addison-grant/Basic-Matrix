
from src.library.matrix import Matrix

def run_test():
    A = Matrix(3, 3, range(3*3))
    print_A = """        0         1         2
        3         4         5
        6         7         8"""
    assert(str(A) == print_A)
    assert(A[0,0] == 0)
    assert(A[1,1] == 4)
    B = Matrix(2,3,[1,2,3,4,5,6])
    assert(B*B.transpose() == Matrix(2,2,[14, 32, 32, 77]))
    return True

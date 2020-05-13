'''Magic Square

https://en.wikipedia.org/wiki/Magic_square

A magic square is a n * n square grid filled with distinct positive integers in
the range 1, 2, ..., n^2 such that each cell contains a different integer and
the sum of the integers in each row, column, and diagonal is equal.

'''

from z3 import *

def solve_magic_square(n, r, c, val):
    solver = Solver()

    ### CREATE CONSTRAINTS AND LOAD STORE THEM IN THE SOLVER
    a = [ [ BitVec("%s%s" % (i, j),64) for j in range(n) ]for i in range(n) ]

    #condition for n>0
    nchk=[And(n>0)]
    #condition for 0<=r<n
    rchk=[And(0<=r,r<n)]
    #condition for 0<=c<n
    cchk=[And(0<=c,c<n)]
    #condition for 1<=val<=n*n
    valchk=[And(1<=val,val<=n*n)]
    #condition for a[r,c]=val
    valposchk=[And(a[r][c]==val)]
    #check for each element in matrix in betweem 1<=a[i][j]<=n*n
    cellchk  = [ And(1 <=a[i][j],a[i][j] <= (n*n))for i in range(n) for j in range(n) ]
    #condition for distinct elements in row
    rowschk   = [ Distinct(a[i]) for i in range(n) ]
    #condition for distinct elements im columns
    colschk  = [ Distinct([ a[i][j] for i in range(n) ])for j in range(n) ]
    #condition for each element in matrix is distinct
    distchk  = [ Distinct([ a[i][j] for j in range(n)  for i in range(n)]) ]
    #to check sum of rows and columns and diagonals are equal
    for i in range (n):
    	solver.add(Sum([a[j][i]for j in range(n)])==Sum(a[i]),Sum(a[i])==Sum([a[j][j]for j in range(n)]),Sum([a[j][i]for j in range(n)])==Sum([a[j][j]for j in range(n)]),Sum(a[i])==Sum([a[j][n-j-1]for j in range(n)]),Sum([a[j][i]for j in range(n)])==Sum([a[j][n-j-1]for j in range(n)]) )

    solver.add(nchk+rchk+cchk+valchk+valposchk+cellchk+rowschk+colschk+distchk)


    if solver.check() == sat:
        mod = solver.model()
        res = []
        res = [ [ mod.evaluate(a[i][j]) for j in range(n) ]for i in range(n) ]

        ### CREATE RESULT MAGIC SQUARE BASED ON THE MODEL FROM THE SOLVER

        return res
    else:
        return None


def print_square(square):
    '''
    Prints a magic square as a square on the console
    '''
    n = len(square)

    assert n > 0
    for i in range(n):
        assert len(square[i]) == n

    for i in range(n):
        line = []
        for j in range(n):
            line.append(str(square[i][j]))
        print('\t'.join(line))


def puzzle(n, r, c, val):
    res = solve_magic_square(n, r, c, val)
    f=None
    if res is None:
        print('No solution!')
    else:
        print('Solution:')
        print_square(res)
        f=res[:]
        for i in range(n):
        	for j in range(n):
        		f[i][j]=res[i][j].as_long()
    return f


if __name__ == '__main__':
    n = 3
    r = 1
    c = 1
    val = 5
    puzzle(n, r, c, val)

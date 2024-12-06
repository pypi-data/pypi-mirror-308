import sympy as sp
from sympy import I, nsimplify

def print_matrix(matrix):
    """Helper function to print the matrix at each step."""
    sp.pprint(matrix, use_unicode=True)
    print()

def matrix_to_rref_with_steps(matrix):
    # Convert to sympy Matrix
    mat = sp.Matrix(matrix)
    rows, cols = mat.shape

    print("Initial Matrix:")
    print_matrix(mat)

    # Track row operations step by step
    row = 0
    for col in range(cols):
        # Find the pivot row (the first row with a non-zero entry in this column)
        pivot_row = None
        for r in range(row, rows):
            if mat[r, col] != 0:
                pivot_row = r
                break

        if pivot_row is None:
            # If there's no pivot in this column, move to the next column
            continue

        # Swap the current row with the pivot row if they're not the same
        if pivot_row != row:
            mat.row_swap(row, pivot_row)
            mat = mat.applyfunc(nsimplify)
            print(f"R{row + 1} <-> R{pivot_row + 1}")
            print_matrix(mat)

        # Scale the pivot row to make the pivot element 1
        pivot_val = mat[row, col]
        if pivot_val != 1:
            mat.row_op(row, lambda x, _: x / pivot_val)
            mat = mat.applyfunc(nsimplify)

            print(f"R{row + 1} *= (1/({pivot_val})) ")
            print_matrix(mat)

        # Eliminate all other entries in this column
        for r in range(rows):
            if r != row and mat[r, col] != 0:
                factor = mat[r, col]
                mat.row_op(r, lambda x, j: x - factor * mat[row, j])
                
                mat = mat.applyfunc(nsimplify)
                # Show the row operation in the form "Rr -> Rr - factor * Rrow"
                operation = f"R{r + 1} += - ({factor}) * R{row + 1}"
                print(operation)
                print_matrix(mat)

        # Move to the next row for the next pivot
        row += 1
        if row == rows:
            break

    print("Final RREF Matrix:")
    print_matrix(mat)

    return mat



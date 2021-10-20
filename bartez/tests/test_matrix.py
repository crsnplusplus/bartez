def add_column_to_matrix(matrix, column):
    new_matrix = []
    
    for row in matrix:
        new_row = []
        for el1 in row:
            new_row.append(el1)
            for el2 in column: 
                new_row.append(el2)
        new_matrix.append(new_row)
    return new_matrix
            
list1 = [1, 2, 3, 4]
indices = add_column_to_matrix(list1, list1)
indices3 = add_column_to_matrix(indices, list1)
print(indices)

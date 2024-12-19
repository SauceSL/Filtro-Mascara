def pascal(row):
    if row == 0:
        return [[]]
    elif row == 1:
        return [[1]]
    else:
        last_row = pascal(row-1)[-1]
        new_row = [1]
        for i in range(len(last_row)-1):
            new_row.append(last_row[i] + last_row[i+1])
        new_row.append(1)
        return pascal(row-1) + [new_row]

print(pascal(10)) 
### solve the longest common subsequence problem

# get the matrix of LCS lengths at each sub-step of the recursive process
# (m+1 by n+1, where m=len(list1) & n=len(list2) ... it's one larger in each direction
# so we don't have to special-case the x-1 cases at the first elements of the iteration
def lcs_mat(list1, list2):
    m = len(list1)
    n = len(list2)

    mat = [[list() for column in range(n+1)] for row in range(m+1)]

    for row in range(1, m+1):
        for col in range(1, n+1):
            if list1[row - 1] == list2[col - 1]:
                # if it's the same element, it's one longer than the LCS of the truncated lists
                mat[row][col] = mat[row - 1][col - 1] + [list1[row - 1]]
            else:
                # they're not the same, so it's the the maximum of the lengths of the LCSs of the two options (different list truncated in each case)
                mat[row][col] = max(mat[row][col - 1], mat[row - 1][col], key=len)
    return mat


# return a set of the sets of longest common subsequences in list1 and list2
def longest_common_seq(list1, list2):
    matrix = lcs_mat(list1, list2)
    rows = [row for row in matrix]
    elements = []
    for row in rows:
        elements.extend(row)

    return max(elements, key=len)

### main ###

def main():
    l1 = [7,1,5,4,4,7,2,2,6,6]
    l2 = [6,6,7,2,2,7,7,1,5,4]
    longest = longest_common_seq(l1, l2)
    print(longest)

if __name__ == "__main__":
    main()
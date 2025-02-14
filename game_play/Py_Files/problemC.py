t = int(input())
row1 = 0
row2 = 0
for _ in range(t):
    inp = input()
    lst_num = inp.split()
    m = int(lst_num[0])
    a = int(lst_num[1])
    b = int(lst_num[2])
    c = int(lst_num[3])
    row1 = min(m, a)
    row2 = min(m, b)
    l_row1 = m - row1
    l_row2 = m - row2
    if c >= 1:
        row1 += min(l_row1, c)
        c -= min(l_row1, c)
    if c >=1:
        row2 += min(l_row2, c)
        c -= min(l_row1, c)
    print(row1 + row2)

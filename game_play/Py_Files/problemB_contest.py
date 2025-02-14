t = int(input())
for _ in range(t):
    x = input()
    lst = x.split()
    n = int(lst[0])
    k = int(lst[1])
    a = 1
    combos = ["0"] * n
    last = None
    new_lst = [i for i in range(1, n + 1)]
    for num in new_lst:
        if a * k - 1 > n - 1:
            break
        combos[a * k - 1] = str(num)
        a += 1
        last = int(combos[(a - 1) * k - 1])
    for i, x in enumerate(combos):
        if x == "0":
            combos[i] = str(last + 1)
            last += 1
 
    result = ' '.join(combos)
    print(result)
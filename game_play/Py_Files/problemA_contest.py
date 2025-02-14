def not_33(x):
    if "33" not in str(x):
         return x
    else:
        index = str(x).find("33")
        new_x = str(x)[:index] + str(x)[index + 2:]
        if len(new_x) > 0:
            s = int(new_x)
    return not_33(s)
def sub(x):
    if x == 0 or x < 33:
        return x
    elif x != 33:
        x = not_33(x)
    return sub(x - 33)

t = int(input())
for _ in range(t):
    x = int(input())
    x = sub(x)
    if x == 0:
        print("YES")
    else:
        print("NO")    

    
    
    

    
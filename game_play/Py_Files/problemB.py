t = int(input())
for _ in range(t):
    a = input()
    r_a = a[::-1]
    new_str = ""
    for letter in r_a:
        if letter == "p":
            new_str += "q"
        elif letter ==  "q":
            new_str += "p"
        else:
            new_str += letter
    print(new_str)
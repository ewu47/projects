#Factorial

def factorial(n : int) -> int:
    """
    returns the factorial of a given integer
    """

    if n == 0:
        return 1
    
    return n * factorial (n-1)


if __name__ == "__main__":
    print(factorial(5))


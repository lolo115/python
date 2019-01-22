def divide(x, y):
     try:
         result = x / y
     except ZeroDivisionError:
        print("division by zero!")
     else:
        print("result is", result)
     finally:
        print("Bye bye ...")

if __name__ == '__main__':
    print(2/0)

    divide(4,2)
    divide(4,0)


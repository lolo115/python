def addOne(v):
    return v+1

if __name__ == '__main__':
    l=[1,2,3,4,5]
    # List transformation

    # Crap
    for i in range(len(l)):
       l[i]=addOne(l[i])
    print(l)

    # Clean ... we map addOne function on each value of the array
    print(list(map(addOne, l)))

    # Better ... same with a lambda (anonymous function)
    print(list(map(lambda x:x+1,l)))
a = 0
b = 1

def run(data):
    global a
    global b

    a, b = b, a + b

    return a

import basic

while True:
    text = input('calc> ')
    if text == 'quit': break
    result,error = basic.run(text)

    if error: print(error)
    else: print(result)

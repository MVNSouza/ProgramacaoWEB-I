chance = 2
while True:
    email = input('Email:')
    try:
        password = int(input('Senha:'))
    except ValueError:
        password = 0

    if chance == 0: 
        print("Acesso Bloqueado")
        break

    if email == '' or password == '' :
        print('Preencha todos os campos!')
        continue
    elif email == 'admin' and int(password) == 1234:
        print('Login realizado com sucesso')
    else:
        print('Dados invalidos')
        chance -= 1
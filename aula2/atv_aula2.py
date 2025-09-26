for i in range(5):
    numero = int(input(f"Digite o {i + 1}º número: "))

    if numero == 3:
        print("Número 3 ignorado.")
        continue 

    if numero == -1:
        print("Número -1 detectado. Encerrando o programa.")
        break

    print(f"Você digitou: {numero}")
lista = [0]

def agregar():
    
    for x in range(3):
        valor = int(input("agregar valor: "))
        lista.append(valor)
        lista.remove(lista[0])

    print(lista)


agregar()
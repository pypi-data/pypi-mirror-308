"""
Created on Wendnesday 13/11/24

@author: Victor Mendoza
"""
# Función Shell
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    paso = 1

    while gap > 0:
        print(f"\nGap actual: {gap}")
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
            print(f"Paso {paso}: {arr}")
            paso += 1
        gap //= 2
    return arr
# Función Quick
def quicksort(arr, depth=0):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[-1]
        left = [x for x in arr[:-1] if x <= pivot]
        right = [x for x in arr[:-1] if x > pivot]
        
        print("\n  " * depth + f"División en profundidad {depth}: Pivote = {pivot}")
        print("  " * depth + f"Izquierda: {left}")
        print("  " * depth + f"Derecha: {right}")
        
        # Recursión y combinación
        sorted_left = quicksort(left, depth + 1)
        sorted_right = quicksort(right, depth + 1)
        
        result = sorted_left + [pivot] + sorted_right
        print("  " * depth + f"Combinación en profundidad {depth}: {result}")
        
        return result
# Función Heap
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        print(f"\nIntercambio: {arr}")
        heapify(arr, n, largest)

def heapsort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
        print(f"Heap construido en índice {i}: {arr}")
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        print(f"Intercambio de raíz con el elemento en índice {i}: {arr}")
        heapify(arr, i, 0)
        print(f"Heap después del heapify en índice {i}: {arr}")
    return arr
# Función Radix
def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    print(f"\n[Counting Sort] Ordenando por el dígito en la posición {exp}:")
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
    print("Frecuencia de cada dígito:", count)
    for i in range(1, 10):
        count[i] += count[i - 1]
    print("Posiciones finales en la lista de salida:", count)
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    print("Lista después de ordenar por el dígito actual:", output)
    for i in range(0, len(arr)):
        arr[i] = output[i]

def radix_sort(arr):
    max_num = max(arr)
    exp = 1
    print("Lista original:", arr)
    while max_num // exp > 0:
        print(f"\n[Radix Sort] Ordenando con exp = {exp}")
        counting_sort(arr, exp)
        print("Lista después de ordenar con exp =", exp, ":", arr)
        exp *= 10
    return arr

# Función Intercambio
def metodo_burbuja(ListaNum):
    for i in range(len(ListaNum) - 1):
    
        for j in range(len(ListaNum) - 1):
        
            print(ListaNum[j],">",ListaNum[j + 1]) # Se imprime la comparación
        
            if ListaNum[j] > (ListaNum[j + 1]): # Comparamos los números
                ListaNum[j], ListaNum[j + 1] = ListaNum[j + 1], ListaNum[j] # Si el primer número es mayor al segundo, intercambiamos
                print("Si hay cambio")
            else:
                print("No hay cambio")
    
        print(f"\nLa lista queda así después de la pasada {i + 1}:\n")
        print(ListaNum,"\n")
    return ListaNum
# Función Inserción
def metodo_baraja(ListaNum):
    # Empezamos desde el segundo elemento
    for i in range(1, len(ListaNum)):
        valor_actual = ListaNum[i] # Guardamos el valor actual que queremos insertar en su posición correcta
        j = i - 1

        # Desplazamos los elementos mayores hacia la derecha para hacer espacio
        while j >= 0 and ListaNum[j] > valor_actual:
            print(valor_actual,"<",ListaNum[j]) # Se imprime la comparación actual
            ListaNum[j + 1] = ListaNum[j]
            j -= 1  
            print("Si hay cambio")
        
        if ListaNum[j] < valor_actual:
            print(valor_actual,"<",ListaNum[j]) # Se imprime la comparación actual
            print("No hay cambio")
        
        ListaNum[j + 1] = valor_actual # Insertamos el valor actual en su lugar
        print(f"\nLa lista queda así después de la pasada {i + 1}:\n")
        print(ListaNum,"\n")
    return ListaNum
# Función Selección
def metodo_seleccion(ListaNum):
    for i in range(len(ListaNum) - 1):
        indicemenor = i # Guardamos el indice del primer elemento como el menor

        for j in range(i + 1,len(ListaNum)): # Ciclo desde el elemento que sigue al seleccionado como menor hasta el último elemento

            print(f"El elemento menor es:",ListaNum[indicemenor]) # Se imprime el elemento menor seleccionado
            print(ListaNum[indicemenor],"<",ListaNum[j]) # Se imprime la comparación

            if ListaNum[indicemenor] > ListaNum[j]: # Comparamos los números
                indicemenor = j
                print("Si hay cambio")
            else:
                print("No hay cambio")
    
        if indicemenor != i: # Actuatilizamos las posiciones
            ListaNum[i], ListaNum[indicemenor] = ListaNum[indicemenor], ListaNum[i]

        print(f"\nLa lista queda así después de la pasada {i + 1}:\n")
        print(ListaNum,"\n")
    return ListaNum
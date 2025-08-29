
list_numbers = [1, 2, 3, 2, 4, 5, 2, 2, 2, 2] #Listas ordenadas or sin orden
list_letters = ['a', 'b', 'c'] # lista de strings
list_mix = [2, 'z', True, [1, 2, 3], 5.5] # lista mixta

shopping_cart = ["Laptop", "Silla Gamer", "Café"]

print(type(list_mix))

# Métodos

# append
print(list_numbers)
list_numbers.append(100)
list_numbers.append(200)
print(list_numbers)

# remove
list_numbers.remove(4) # elimina el valor 4 de la lista
list_numbers.remove(100)
print(list_numbers)

# count
print(list_numbers.count(2)) # dice cuántas veces aparece el 2 en la lista

# .copy()
# .sort()
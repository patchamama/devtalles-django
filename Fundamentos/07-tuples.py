# A diferencia de las listas, las tuplas son inmutables, es decir, no se pueden cambiar los valores de la misma.

my_tuple = (1, 2, 3, 4, "Hola", True, False, 2, "hi", 3, 2)

print(my_tuple)
print(my_tuple.count(2)) # 3
print(my_tuple.index(2)) # 1

# my_tuple[1] = 20 esto da un error al ser inmutable
print(my_tuple)

week = ('Lunes', 'Martes', 'Miércoles')

user = {
    "name": "Ricardo",
    "age": 29,
    "email": "ricardo@email.com",
    "active": True,
    (19.12, -98.32): "Cancún México" # sí la key es una tupla el valor no es mutable
}

user["name"] = "Richard"
user["age"] = 27
user["country"] = "México"
# print(user[(19.12, -98.32)])

# values, items, keys
print(user)
print(user.items())
print(user.keys())
print(user.values())
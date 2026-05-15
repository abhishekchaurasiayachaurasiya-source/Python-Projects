number = 2, 5, 8, 10, 13, 15, 18, 20, 25
result = []

for n in number:
    if n % 5 == 0 and n % 2 !=0:
        result.append(n)
print(result)

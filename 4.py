number = int(input("Enter your number: "))
print(f"\nMultiplication Table of {number} ")

for i in range(1,11):
    result = number * i
    print(f"{number} * {i} = {result}")

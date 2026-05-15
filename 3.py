for i in range(2,22,2):
    print(i)

numbers = int(input("enter your Table number: "))
print(f"\nMultiplication Table of {numbers} ")

for i in range(1,11):
    result = numbers * i
    print(f"{numbers} * {i} = {result}")
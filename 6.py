numbers = int(input("Enter your number"))
for i in range(1, 11):
    result = numbers * i
    print(f"{numbers} * {i} = {result}")

for i in range(1, 100):
    if(i%2==0):
        print(i)

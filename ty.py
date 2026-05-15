balance = 5000
amount = int(input("Enter Your amount"))
if(amount<=0):
    print("Influcent balance")
elif(amount> balance):
    print("Please Enter your amount according to balance ")
elif(amount % 500 !=0):
 print("according to 500 notes available")
else:
  balance = balance - amount
  print(f"Successful!, New balance {balance}")
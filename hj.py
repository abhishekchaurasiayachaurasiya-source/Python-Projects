user_bill = int(input("Enter your bill: "))
if(user_bill<=100 ):
  
  print(f"Your bill is {user_bill} free")
else:
  print(user_bill * 5, ("is above then 100 unit"))
  print( f"Your bill is {user_bill * 5} is not free ")
current_Pin = 1234
Balance = 10000
cont = str(input("Do you continue this page? y/n: "))
for i in range(3):
  if cont=="y":
    user_Pin = int(input("Enter your Pin: "))
    if user_Pin == current_Pin:
        print("1.Deposit")
        print("2.Change Pin")
        print("3.Created balance")
        print("4.Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            Deposit = int(input("Enter your deposit amount: "))
            Deposit = Balance -Deposit
            print("Your balance is: ",Deposit)
        if choice ==2:
                    new_pin = int(input("Enter your change Pin: "))
                    Change_Pin = new_pin
                    print("Your change Pin: ", Change_Pin)
        if choice == 3:
                    Created_Balance = int(input("Enter your created balance: "))
                    created_Balance = Created_Balance + Balance
                    print("Your created balance is: ", created_Balance)
        if choice == 4:
         print("exit")
         break
    else:
       print(f"Your pin is incorrect You have only to chance {2-i}")
  else:
    print("Thanks for using me")
else:
     print("YOur card blocked")
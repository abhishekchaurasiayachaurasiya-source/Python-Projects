experience = int(input("Enter your experience"))
salary = int(input("Enter your salary"))
bonus = 0.05
new_salary = bonus * salary + salary
if(experience>=5):
    print(f"Congratulation you are eligible to bonus {bonus * salary}")
else:
    print(f"Sorry you are no eligible to bonus")
print(f"Your new salary is {new_salary}")

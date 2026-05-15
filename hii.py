menu = {
    'Pizza':40,
    'Pasta':50,
    'Burger':60,
    'Salad':70,
    'Coffee':80
}
print("Welcome to Python Restaurant")
print("Pizza: Rs 40\nPasta: Rs 50\nBurger: Rs 60\nSalad: 70\nCoffee: 80")

order_total = 0

item_1 = str(input("Enter the name of item you want to order = "))
if item_1 in menu:
    order_total += menu[item_1]
    print(f"YOur item {item_1} has been added to your order")

else:
    print("Ordered item {item_1} is not availble yet ")

another_order = str(input("Do you want to add another item? (Yes/No) "))
if another_order =="Yes":
    item_2 = str(input("Enter the name of second item = "))
    if item_2 in menu:
        order_total += menu[item_2]
        print(f"Item {item_2} has been added to order ")
    else:
        print(f"Ordered item {item_2} is not avaialable!")

    item_3 = str(input("Enter the name of Third item = "))
    if item_3 in menu:
        order_total += menu[item_3]
        print(f"Item {item_3} has been added to order")
    else:
        print(f"Ordered item {item_3} is not available!")

print(f"The total amout of items is {order_total}")

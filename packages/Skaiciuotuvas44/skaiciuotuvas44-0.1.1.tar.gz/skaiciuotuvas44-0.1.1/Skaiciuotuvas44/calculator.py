class Calculator:
    def __init__(self, number):
        self.number = number

    def add(self):
        skaicius1 = float(input("Enter your number here: "))
        skaicius2 = float(input("Enter your number here: "))
        suma = skaicius1 + skaicius2
        return f"{skaicius1} + {skaicius2} = {suma}"

    def deduct(self):
        skaicius1 = float(input("Enter your number here: "))
        skaicius2 = float(input("Enter your number here: "))
        suma = skaicius1 - skaicius2
        return f"{skaicius1} - {skaicius2} = {suma}"

     def sqr(self):
        skaicius1 = float(input("Enter your number here: "))
        suma = skaicius1 ** 2
        return f"{skaicius1} ** 2 = {suma}"

    def divide(self):
        skaicius1 = float(input("Enter your number here: "))
        skaicius2 = float(input("Enter your number here: "))
        santykis = skaicius1 / skaicius2
        return f"{skaicius1} / {skaicius2} = {santykis}"

    def multiply(self):
        skaicius1 = float(input("Enter your number here: "))
        skaicius2 = float(input("Enter your number here: "))
        suma = skaicius1 * skaicius2
        return f"{skaicius1} * {skaicius2} = {suma}"

calc = Calculator(0)

while True:
    print("\nSelect an operation:")
    print("1. Add")
    print("2. Deduct")
    print("3. Square")
    print("4. Multiply")
    print("5. Divide")
    print("6. Exit")

    choice = input("Enter your choice (1/2/3/4/5/6): ")

    if choice == "1":
        print(calc.add())
    elif choice == "2":
        print(calc.deduct())
    elif choice == "3":
        print(calc.sqr())
    elif choice == "4":
        print(calc.mult())
    elif choice == "5":
        print(calc.div())
    elif choice == "6":
        print("Exiting program...")
        break
    else:
        print("Invalid input! Please choose a valid option.")


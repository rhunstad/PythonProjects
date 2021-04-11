

departments = {
    0: ["Car Electronics & GPS", 0],
    1: ["Appliances", 0],
    2: ["TV Home & Theater", 0],
    3: ["Computers & Tablets", 0],
    4: ["Cameras & Camcorders", 0],
    5: ["Cell Phones", 0],
    6: ["Audio", 0],
    7: ["Video Games", 0],
    8: ["Movies & Music", 0],
    9: ["Wearable Fitness", 0],
    10: ["Health, Fitness & Personal Care", 0],
    11: ["Home, Furniture & Office", 0],
    12: ["Smart Home, Security & Wi-Fi", 0],
    13: ["Drones, Toys & Collectibles", 0]
}

products = {}
running = True


def main():
    choice = input('Menu: \n'
                   '\t(1) Enter a receipt\n'
                   '\t(2) View Totals\n'
                   '\t(3) Exit program\n\nYour choice: ')
    if choice == "1":
        receipt()
    elif choice == '2':
        totals()
    elif choice == '3':
        global running
        running = False
    else:
        print("Sorry, that is not an option. Try again. ")
        main()


def receipt():
    count = 1
    subtotal = 0
    taxes = 0
    rec_text = ""
    choice = 0
    print("-- Input ID of item, or press -1 to finish receipt -- ")
    while choice != "-1":
        choice = input("Item %s ID: " % count)
        prod = products.get(choice)
        if prod is None:
            if choice != "-1":
                print("Sorry, no product found under that ID. ")
            continue
        subtotal += float(prod.product_price)
        departments.get(int(prod.product_dept))[1] += float(prod.product_price)
        rec_text += "$%s  --  %s\n" % (prod.product_price, prod.product_name)
        count += 1

    subtotal = round(subtotal, 2)
    taxes = round(subtotal * .1, 2)
    total = round(subtotal + taxes, 2)
    print("\n%s\nSubtotal: $%s\nTaxes: $%s\nTotal: $%s\n\n" % (rec_text, subtotal, taxes, total))


def totals():
    total = 0.0
    print("\n")
    for key, value in departments.items():
        if int(float(value[1]) > 0):
            print("--%s: $%s" % (value[0], round(value[1], 2)))
            total += value[1]
    print("Total Sales: $%s" % round(total, 2))


def read_file():
    fi = open('inventory4.txt', 'r')
    f = fi.read()
    fi.close()

    for line in f.split("\n"):
        prod = line.split("#")
        p = Product(prod[0], prod[1], prod[2], prod[3])
        products[p.product_id] = p


class Product(object):
    def __init__(self, product_id, product_name, product_price, product_dept):
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.product_dept = product_dept


if __name__ == '__main__':
    read_file()
    while running:
        main()

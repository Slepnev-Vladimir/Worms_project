# the program contains a function that shows the goods from the menu
# that can be purchased with a certain amount of money

menu = {'product_1': 1, 'product_2': 2, 'product_3': 3, 'product_4': 4}
money = 3


def available(menu, money):
    available_goods = []

    for key in menu:
        if menu[key] <= money:
            available_goods.append(key)

    return(available_goods)


print(available(menu, money))

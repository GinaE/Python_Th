# bike_market.py

class Bicycle(object):
    def __init__(self, model, weight, cost):
        self.model = model
        self.weight = weight
        self.cost = cost

class Bike_shop(object):
    def __init__(self, shop_name, inventory, margin):
        self.shop_name = shop_name
        self.inventory = inventory # Have an inventory of different bicycles
        self.margin = margin # Sell bicycles with a margin over their cost 
    
    # Sell bicycles with a margin over their cost        
    def selling_price(self, bike):
        price = bike.cost + self.margin*bike.cost/100
        return price
        
    # Can see how much profit they have made from selling bikes
    
class Costumer(object):
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        
    # Can buy and own a new bicycle
    def canBuy(self, shop, bike):
        if shop.selling_price(bike) <= self.budget:
            print("I can buy it")
            return True
        else:
            return False
        


        
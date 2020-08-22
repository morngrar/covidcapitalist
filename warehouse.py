"""Module for displaying warehouse stock and demand"""

import pygame

# Check if stock is equal to demand
def checkWarehouse(gameData):
    stock_keys = [key for key in gameData.keys() if 'stock' in key]
    demand_keys = [key for key in gameData.keys() if 'demand' in key]
    
    # Iterate through the demand and stock and evaluate
    for i in stock_keys:    # Get the item name
        item = i.split(" ")[0]

                            # If the demand is equal to or less than the stock
        if gameData[item + " stock"] >= gameData[item + " demand"]:
            #sellMerch
            print("ja, vi kan selge " + item)


# Function reduces your stock and increases the revenue
def sellMerch(stock, price, revenue):
    revenue += (stock*price)
    stock -= stock




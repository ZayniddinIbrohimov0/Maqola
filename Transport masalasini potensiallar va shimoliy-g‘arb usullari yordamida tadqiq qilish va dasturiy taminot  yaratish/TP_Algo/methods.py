from utils import Price, matrix_to_pricematrix
from os import system

API_COSTS = "api/costs.txt"
API_DEMAND = "api/demand.txt"
API_OFFER = "api/offer.txt"

API_MODI = "api/rezult_modi.txt"
API_REZULT_SSM = "api/rezult_ssm.txt"
API_REZULT_LCM = "api/rezult_lcm.txt"

TOTAL_COSTS = "api/total_costs.txt"

class _Solution:
    def __init__(self, costs: list[list[float]], demand: list, offer: list) -> None:
        self.costs = matrix_to_pricematrix(costs)
        self.demand = demand
        self.offer = offer
        self.set_data_cpp()
        self.solve()
    
    def set_data_cpp(self):
        self.set_costs()
        self.set_offer()
        self.set_demand()

    def set_demand(self):
        text = ''
        for i in self.demand:
            text += str(i) + ' '
        with open(API_DEMAND, 'w') as file:
            file.write(text)
    
    def set_offer(self):
        text = ''
        for i in self.offer:
            text += str(i) + ' '
        with open(API_OFFER, 'w') as file:
            file.write(text)
    
    def set_costs(self):
        text = ''
        for i in self.costs:
            for j in i:
                text += str(j.arg) + ' '
            text += '\n'
        with open(API_COSTS, 'w') as file:
            file.write(text)

    def get_rezult(self, api) -> list[Price]:
        vc = []
        with open(api, 'r') as file:
            for line in file:
               arg, i, j = map(float, line.split())
               vc.append(Price(i=i, j=j, arg=arg))
        return vc

    def solve(self):
        system(".\\cpp\\main.exe")
    
    def solve_smm(self):
        return self.get_rezult(api=API_REZULT_SSM)
    
    def solve_lcm(self):
        return self.get_rezult(api=API_REZULT_LCM)
    
    def solve_modi(self):
        return self.get_rezult(api=API_MODI)



class LeastCostMethod:
    def __init__(self, costs, demand, offer) -> None:
        self.solve = _Solution(costs=costs, demand=demand, offer=offer)
    def get_rezault(self):
        return self.solve.get_rezult(api=API_REZULT_LCM)
    
class SteppingStone:
    def __init__(self, costs, demand, offer) -> None:
        self.solve = _Solution(costs=costs, demand=demand, offer=offer)
    def get_rezault(self):
        return self.solve.get_rezult(api=API_REZULT_SSM)
    
class MODIMethod:
    def __init__(self, costs, demand, offer) -> None:
        self.solve = _Solution(costs=costs, demand=demand, offer=offer)
    def get_rezault(self):
        return self.solve.get_rezult(api=API_MODI)
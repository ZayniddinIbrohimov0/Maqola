from gui import TransportationSolveGUI
from methods import LeastCostMethod, SteppingStone, MODIMethod

TransportationSolveGUI(demand_name='Talab', offer_name='Taklif', solution_class={
    "Stepping stone":   SteppingStone,
    "Least Cost":       LeastCostMethod,
    "MODI Method":      MODIMethod
})



""" Algoritmni GUIsiz ishlatish uchun DEBUG_ALGORITHM=True qilib kerakli qiymatlarni kiritib foydalanish mumkin """
DEBUG_ALGORITHM = False
if DEBUG_ALGORITHM:
    costs = [
        [140, 170, 180, 200],
        [60, 50, 60, 90],
        [120, 60, 80, 70]
    ]
    demand = [20, 15, 10, 12]
    offer = [25, 12, 20]
    
    # least cost metodining javobi
    solve_lcm = LeastCostMethod(demand=demand, offer=offer, costs=costs)
    # stepping stone metodining javobi
    solve_ssm = SteppingStone(demand=demand, offer=offer, costs=costs)
    # modi metodining javobi
    solve_modi = MODIMethod(demand=demand, offer=offer, costs=costs)
    
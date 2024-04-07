


class Price:
    def __init__(self, i: int, j: int, arg: int) -> None:
        self.i: int = int(i)
        self.j: int = int(j)
        self.arg = arg
    def __str__(self) -> str:
        return '%s (%s:%s)'%(
            self.arg,
            self.i,
            self.j,
        )

class Point(object):
    def __init__(self, money: Price, massa: int) -> None:
        self.money = money
        self.massa = massa

    
    def __str__(self) -> str:
        return '(%s, %s)' %(str(self.money), str(self.massa))

    def multi(self) -> int:
        return self.money.arg * self.massa
    



def matrix_to_pricematrix(matrix: list[list[int]]) -> list[list[Price]]:
    vc = []
    for i in range(len(matrix)):
        new_vc = []
        for j in range(len(matrix[0])):
            new_vc.append(Price(i=i, j=j, arg=matrix[i][j]))
        vc.append(new_vc)
        new_vc = []
    return vc


def real_or_int(number: float) -> float|int:
    real_number = float(number)
    int_number = int(number)
    if float(int_number) == real_number:
        return int_number
    else:
        return real_number

def price_real_or_int(arg: Price) -> Price:
    arg.arg = real_or_int(arg.arg)
    return arg

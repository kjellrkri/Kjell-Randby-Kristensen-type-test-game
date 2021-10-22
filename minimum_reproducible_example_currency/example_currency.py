from decimal import *

from attr import dataclass

getcontext().prec = 5


class Currency:
    """
    Currency represents money.
    Unit represents the lowest unit of a currency.
    Unit can not be < 0.
    Currency only accept positive integers of type Int or Decimal as arguments.
    """

    def __init__(self, unit, currency="NOK"):
        self.unit = unit
        self.currency = currency

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        if not (isinstance(unit, int) or isinstance(unit, Decimal)):
            raise TypeError("Unit must be type int or Decimal.")
        if unit < 0:
            raise ValueError("Unit must be greater than zero.")
        self._unit = Decimal(unit)

    def __add__(self, other):
        if isinstance(other, Currency):
            return Currency(self._unit + other.unit)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Decimal):
            return Currency(round(self._unit + Decimal(other), 0))
        else:
            raise TypeError("Currency must be added with Currency or numeric type.")

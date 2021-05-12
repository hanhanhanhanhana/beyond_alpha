#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np

from broker import Broker

class Strategy:
    def __init__(self):
        self.__orders = []

    @property
    def orders(self):
        return self.__orders

    def add_order(self, *args):
        for order in args:
            self.__orders.append(order)

    def zero_orders(self):
        self.__orders = []

    def strategy(self, stocks, broker: Broker):
        pass

    def __call__(self, stocks, broker: Broker):
        self.strategy(stocks, broker)

class multi(Strategy):
    def strategy(self, stocks):
        self.add_order()

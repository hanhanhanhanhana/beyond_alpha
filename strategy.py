#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np

class Strategy:
    def __init__(self):
        self.__orders = []

    @property
    def orders(self):
        return self.__orders

    def add_order(self, *args):
        pass

    def del_order(self, *args):
        pass

    def strategy(self, stocks):
        pass

    def __call__(self, stocks):
        self.strategy(stocks)

class multi(Strategy):
    def strategy(self, stocks):
        self.add_order()

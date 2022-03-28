"""Dependancies injection handler

This module give access to the global variable named injector used as dependancies manager.
This relies on the Injector module.
"""

from injector import Injector

global injector
injector = Injector()

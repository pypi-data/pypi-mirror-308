from rdflib import Graph, Namespace
import importlib.resources
from functools import cache

SIM = Namespace("https://simpsons.example.org/")
FAM = Namespace("https://vocab.example.org/family#")

class Simpsons():
    @property
    @cache
    def graph(self):
        with importlib.resources.path(__name__, "simpsons.ttl") as data_path:
            return Graph().parse(data_path, format="turtle")

simpsons = Simpsons()

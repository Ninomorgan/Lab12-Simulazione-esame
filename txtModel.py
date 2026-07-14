from database.DAO import DAO
from model.model import Model

mymodel = Model()

mymodel.creaGrafo(2018, 2019 )
#attori = DAO.getAllActors(1.2, 2.7)
#print(len(attori))

#NODI
n= mymodel.getNodi()
print(f"il Grafo ha {len(n) } nodi")

#archi

#tutto dettagli
n, m = mymodel.getGrafoDetails()
print(f"Grafo creato: {n} nodi, {m} archi")

# for o, d in mymodel.getEdges():
#     peso = mymodel.getPesoArco(o, d)
#     print(f"{o} --> {d}   peso={peso}")
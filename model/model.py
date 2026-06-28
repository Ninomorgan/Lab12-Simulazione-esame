import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

      #METODI PER CREARE GRAFICI

        self._grafo = nx.Graph()  # grafo semplice non diretto


        self._attori=[] #lista nodi
        self._idMapAttori={}

        self._bestCammino = []
        self._bestScore = 0


    def getAllRate(self): #2 aggiungere da dao a model - ora mettre su controller
        return DAO.getAllRate()

    def getALlActors(self, rate1, rate2): #nodi
        return DAO.getAllActors(rate1, rate2)

    def getAllEdges(self, rate1, rate2, idMapAttori):
        return DAO.getAllEdges(rate1, rate2, idMapAttori)

    def creaGrafo(self, rate1, rate2):
        self._grafo.clear()

        # agggiungiamo nodi
        self._attori = self.getALlActors( rate1, rate2)
        self._grafo.add_nodes_from(self._attori)

        #mappa NODI --> dato un ID riprendiamo un Oggeto
        for n in self._attori:
            self._idMapAttori[n.id] = n

        #aggiungiamo archi
        edges = self.getAllEdges(rate1, rate2, self._idMapAttori)
        for  a1, a2, peso  in edges:
            self._grafo.add_edge(a1, a2, weight=peso)

        #aggiugno nodi direzione


    #METODI DESCRIZIONE GRAFICO
    def getNodi(self):
        return self._grafo.nodes()

    def getEdges(self):
        return self._grafo.edges()

    def getPesoArco(self, v1, v2):
        return self._grafo[v1][v2]["weight"]

    def getGrafoDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    #metodo best archi
    def getBestEdges(self):
        result = []
        for o,d in self._grafo.edges(): #origine , destinazione
            peso= self._grafo[o][d]['weight']
            result.append((o,d,peso))

        result.sort(key=lambda x: (x[2], str(x[0])), reverse=True) #ordino per il TERZO PARAMETRO x[2]


        return result[:5] #prendo i primi [5
    #GESTIONE COMPONENTI
    def getComponenti(self):
        return nx.number_connected_components(self._grafo)

    def getBiggestComponent(self):
        componenti = list(nx.connected_components(self._grafo))
        componenti.sort(
            key=lambda c: (len(c), max(str(a) for a in c)),
            reverse=True
        )

        return list(componenti[0])
        # compMax = max(componenti, key=len)
        # result = list(compMax)
        # return result
        # CAMMINO MINIMO

    def getPath(self):  # partenza, arrivo, lunghezza max
        self._bestCammino = []
        self._bestScore = 0

        for n in self._grafo.nodes():
            parziale = [n]
            self._ricorsione(parziale)


        # GRAFO NORMALE

            parziale.pop()
        return self._bestCammino, self._bestScore

        # VARIA

    def _ricorsione(self, parziale):

        # 1) parziale uguale best score e terminate
        # condizione che mi fa terminare

            if self._score(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._score(parziale)


        # 3)RICORSIONE
        # GRAFO NON DIRETTO
                #gesione sui nodi
            for v in self._grafo.neighbors(parziale[-1]):
                # ultimo nodo aggiunto ha peso maggiore
                if v.date_of_birth > parziale[-1].date_of_birth and v not in parziale:
                    parziale.append(v)
                    self._ricorsione(parziale)
                    parziale.pop()

        # UGUALEE

    def _score(self, parziale):  # UGUALE

        # arrivano nodi e preso il parziale e quellodopo prende il peso e lo somma a score
        score = 0
        for i in range(0, len(parziale) - 1):
            score += self._grafo[parziale[i]][parziale[i + 1]]["weight"]

        return score
import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self._idMapInfo = None
        self._grafo = nx.DiGraph() #grafo diretto


        self._attori=[] #lista nodi
        self._idMapAttori = {}

        self._film= []
        self._idMapFilm = {}


        self._bestCammino = []
        self._bestScore = 0


    def getAllDate(self): #2 aggiungere da dao a model - ora mettre su controller
        return DAO.getAllDate()

    def getAllFilms(self , date1, date2): #nodi
        return DAO.getAllFilms(date1, date2)



    def creaGrafo(self, date1, date2):
        self._grafo.clear()

        # agggiungiamo nodi
        self._film = self.getAllFilms(date1, date2)
        self._grafo.add_nodes_from(self._film)

        #mappa NODI --> dato un ID riprendiamo un Oggeto
        for n in self._film:
            self._idMapFilm[n.id] = n

        #aggiungiamo archi
        self._idMapInfo = DAO.getInfoFilm(date1, date2)
        edges = DAO.getAllEdges()
        for id1, id2, attoriComuni in edges:

            # Tengo solo coppie formate da film presenti nei nodi
            if id1 in self._idMapFilm and id2 in self._idMapFilm:

               # Recupero rating e incasso dai nodi
                film1 = self._idMapFilm[id1]
                film2 = self._idMapFilm[id2]

                rating1, incasso1 = self._idMapInfo[id1]
                rating2, incasso2 = self._idMapInfo[id2]

                peso = attoriComuni

                if rating1 > rating2:
                    self._grafo.add_edge(film1, film2, weight=peso)

                elif rating2 > rating1:
                    self._grafo.add_edge(film2, film1, weight=peso)

                else:
                    self._grafo.add_edge(film1, film2, weight=peso)
                    self._grafo.add_edge(film2, film1, weight=peso)
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


        return result[:5] #prendo i primi [5]

    def _getBestProdotti(self):

            result = []
            for p in self._grafo.nodes:
                totUscenti = 0
                totEntranti = 0
                score = 0
                for o,d in self._grafo.in_edges(p): #origine , destinazione
                    peso= self._grafo[o][d]['weight']
                    totEntranti+=peso

                for o,d in self._grafo.out_edges(p):
                    peso = self._grafo[o][d]['weight']
                    totUscenti += peso

                score = totUscenti-totEntranti
                result.append((p, score))

            result.sort(key=lambda x: x[1], reverse=True)

            return result[:5] #UNO SOLO = [0]

    def _getBestFilm(self):

            result = []
            for p in self._grafo.nodes:
                totUscenti = 0
                totEntranti = 0
                score = 0
                for o,d in self._grafo.in_edges(p): #origine , destinazione
                    peso= self._grafo[o][d]['weight']
                    totEntranti+=peso

                for o,d in self._grafo.out_edges(p):
                    peso = self._grafo[o][d]['weight']
                    totUscenti += peso

                score = totUscenti-totEntranti
                result.append((p, score))

            result.sort(key=lambda x: x[1], reverse=True)

            return result[0] #UNO SOLO = [0]


    def getPath(self, partenza,maxArchi):  # partenza, arrivo, lunghezza max
        self._bestCammino = []
        self._bestScore = 0

        parziale = [partenza]
        for v in self._grafo.successors(partenza): #self._grafo.neighbors(partenza)
            parziale.append(v)
            self._ricorsione(parziale, maxArchi)
            parziale.pop()
        return self._bestCammino, self._bestScore


    def _ricorsione(self, parziale, maxArchi):
        score = self.score(parziale)
        if score > self._bestScore:
            self._bestCammino = copy.deepcopy(parziale)
            self._bestScore = score

        if len(parziale) - 1 == maxArchi:
            return

        vicini = self._grafo.successors(parziale[-1])

        # 4. Ricorsione
        for v in vicini:
            # arco che sto provando ad aggiungere
            pesoNuovo = self._grafo[parziale[-1]][v]["weight"]

            # il nuovo arco deve avere peso maggiore del precedente
            pesoPrec = self._grafo[parziale[-2]][parziale[-1]]["weight"]

            if pesoPrec < pesoNuovo and v not in parziale:  # > per peso decrescente
                parziale.append(v)
                self._ricorsione(parziale, maxArchi)
                parziale.pop()

    def score(self, parziale):  # UGUALE

        # arrivano nodi e preso il parziale e quellodopo prende il peso e lo somma a score
        score = 0
        for i in range(0, len(parziale) - 1):
            score += self._grafo[parziale[i]][parziale[i + 1]]["weight"]

        return score
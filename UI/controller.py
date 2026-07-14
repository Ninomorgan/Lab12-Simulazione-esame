import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handleCreaGrafo(self, e):
        ratings1 = self._view._ddrating1.value
        ratings2 = self._view._ddrating2.value

        # cotnrollo dei parametri
        if ratings1 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona una data iniziale", color="red"))
            self._view.update_page()
            return
        if ratings2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona una data finale ", color="red"))
            self._view.update_page()
            return

        # creo grafo
        self._model.creaGrafo(ratings1,ratings2)
        n, m = self._model.getGrafoDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"Grafo creato correttamente\n"
            f"Numero di nodi: {n}\n"
            f"Numero di archi: {m}"))
        self._view.update_page()

        #archi migliori
        bestEdges = self._model.getBestEdges()

        self._view.txt_result.controls.append(ft.Text("Top 5 archi", color="green"))
        for o, d, score in bestEdges:
            self._view.txt_result.controls.append(ft.Text(f"{o} -> {d}: {score}"))
        self._view.update_page()

        #bestNodes

        bestFilm = self._model._getBestFilm()
        self._view.txt_result.controls.append(ft.Text("MIGLIOR FILM", color="green"))
        film,score= bestFilm
        self._view.txt_result.controls.append(ft.Text(f"{film} -> {score}"))
        self._view.update_page()


    def handleCammino(self, e):

        # CERCO CAMMINO MINIMO
        bestFilm = self._model._getBestFilm()
        film, score = bestFilm

        MaxArchi= 10
        cammino, score = self._model.getPath(film,MaxArchi )

        self._view.txt_result.controls.clear()

        if len(cammino) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun cammino trovato")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Percorso ottimo:")
        )

        # print NODI E PESO
        for i in range(len(cammino) - 1):
            peso = self._model.getPesoArco(cammino[i], cammino[i + 1])
            self._view.txt_result.controls.append(
                ft.Text(f"{cammino[i]} -> {cammino[i + 1]} | peso: {peso}")
            )

        self._view.txt_result.controls.append(
            ft.Text(f"Peso totale: {score}")
        )

        self._view.update_page()



    def fillDDsDate(self):
        date = self._model.getAllDate()
        dateDD = list(map(lambda x: ft.dropdown.Option(x), date))

        self._view._ddrating1.options = dateDD
        self._view._ddrating2.options = dateDD

        self._view.update_page()

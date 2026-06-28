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
                f"Seleziona un rating iniziale", color="red"))
            self._view.update_page()
            return
        if ratings2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(
                f"Seleziona un rating finale ", color="red"))
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

        #compoennti
        numComponenti = self._model.getComponenti()

        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numComponenti} componenti connesse",
                                                      color="green"))

        MaxComponenti = self._model.getBiggestComponent()

        self._view.txt_result.controls.append(ft.Text(
            f"Componente più grande ({len(MaxComponenti)} nodi)",
            color="green "))

        for p in MaxComponenti:
            self._view.txt_result.controls.append(ft.Text(
                f"{p}"))


        self._view.update_page()

    def handleCammino(self, e):

        # CERCO CAMMINO MINIMO
        cammino, score = self._model.getPath()

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



    def fillDDsRating(self):
        ratings = self._model.getAllRate()
        ratingsDD = list(map(lambda x: ft.dropdown.Option(x), ratings))

        self._view._ddrating1.options = ratingsDD
        self._view._ddrating2.options = ratingsDD

        self._view.update_page()

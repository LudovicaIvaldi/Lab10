import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._g=None
        self._ddCountryValue=None

    def handleCalcola(self, e):
        anno=self._view._txtAnno.value
        if anno=="":
            self._view._txt_result.controls.append(ft.Text("Inserire un anno", color="red"))
            self._view.update_page()
            return
        try:
            a=int(anno)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserire un numero intero", color="red"))
            self._view.update_page()
            return

        if (a<1816 or a>2016):
            self._view._txt_result.controls.append(ft.Text("Inserire un anno fra 1816 e 2006", color="red"))
            self._view.update_page()
            return

        lista, compConn, grafo=self._model.buildGraph(a)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {compConn} componenti connesse"))
        for str in lista:
            self._view._txt_result.controls.append(ft.Text(str))
        self._view._btnRaggiungibili.disabled=False
        self._view._ddStato.disabled=False
        self._g=grafo
        self.fillddStato()
        self._view.update_page()

    def fillddStato(self):
        for node in self._g.nodes():
            self._view._ddStato.options.append(ft.dropdown.Option(key=node.CCode, text=node.StateNme, data=node, on_click=self.readState))
        self._view._ddStato.options.sort(key=lambda x:x.data.StateNme)


    def readState(self,e):
        self._ddCountryValue=e.control.data

    def handleRaggiungibili(self,e):
        #modo 1
        #listaConn=self._model.nodiRaggiungibili(self._ddCountryValue)
        #modo 2 ricorsione
        #listaConn=self._model.calcolaComponenteConnessaRicorsione(self._ddCountryValue)
        #modo 3 iterativo
        listaConn=self._model.componenteConnessaIterativa(self._ddCountryValue)


        self._view._txt_result.controls.clear()
        if len(listaConn)==0:
            self._view._txt_result.controls.append(ft.Text(f"Non ci sono nodi raggiungibili da: {self._ddCountryValue}"))
            self._view.update_page()
            return
        self._view._txt_result.controls.append(ft.Text(f"I nodi raggiungibili da {self._ddCountryValue} sono:"))
        self._view._txt_result.controls.append(ft.Text(f"Totale degli stati raggiungibili: {len(listaConn)}"))
        for node in listaConn :
                self._view._txt_result.controls.append(ft.Text(node))

        self._view.update_page()


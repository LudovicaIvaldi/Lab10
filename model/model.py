import copy

import networkx as nx
from networkx.classes import all_neighbors

from database.DAO import DAO


class Model:

    def __init__(self):
        self._listaVicini = None
        self._countries=DAO.getAllStates()
        self._idMap={}
        for c in self._countries:
            self._idMap[c.CCode]= c
        self._grafo=nx.Graph()


    def buildGraph(self, anno):
        listaStatiEsistenti=DAO.getStatesAnno(anno)
        for id in listaStatiEsistenti:
            self._grafo.add_node(self._idMap[id])
        listaTupleArchi=DAO.getAllEdges(anno)
        for tupla in listaTupleArchi:
            self._grafo.add_edge(self._idMap[tupla[0]],self._idMap[tupla[1]])
        print(len(self._grafo.nodes()))
        print(len(self._grafo.edges()))
        listaDaStampare=self.getGradoNodi()
        numCompConnesse=self.getComponentiConnesse()
        return listaDaStampare, numCompConnesse, self._grafo


    def getGradoNodi(self):
        result={}
        lista=[]
        for node in self._grafo.nodes():
            result[node]=self._grafo.degree(node)
        ordinato=sorted(result.keys(),key=lambda x:x.StateAbb )
        for stato in ordinato:
            lista.append(f"{stato.StateNme} -- {result[stato]} vicini")

        return lista

    def getComponentiConnesse(self):
        return ( nx.number_connected_components(self._grafo))


    def nodiRaggiungibili(self,source):
        conn=nx.node_connected_component(self._grafo,source)
        conn.remove(source)
        return conn

    def calcolaComponenteConnessaRicorsione(self,source):
        self._listaVicini=[]
        succ=self.getSuccessori(source,[source])
        print(succ)
        self.ricorsione(succ,[source])
        for i in self._listaVicini:
            print(i)
        return self._listaVicini

    def ricorsione(self,successori,parziale):
        #print("chiamo ricorsione")
        #non posso chimare sempre successori e sperare che sia vuota perchè tutti i nodi hanno dei successori
        #devo controllare quando li creo che non siano in parziale
        if len(successori)==0:
            self._listaVicini=copy.deepcopy(parziale)

        else:
            for nodo_nuovo in successori:
                if nodo_nuovo not in parziale:
                    parziale.append(nodo_nuovo)
                    succ_nuovi=self.getSuccessori(nodo_nuovo,parziale)
                    self.ricorsione(succ_nuovi,parziale)
                    parziale.pop()

    def getSuccessori(self,nodo_nuovo,parziale):
        successori=list(self._grafo.neighbors(nodo_nuovo))
        possibili_successori=[]
        for nodo in successori:
            if nodo not in parziale:
                possibili_successori.append(nodo)
        return possibili_successori

    def componenteConnessaIterativa(self,source):
        daVisitare=[source]
        visitati=[]
        for nodo in daVisitare:
            daVisitare.remove(nodo)
            successori = list(self._grafo.neighbors(nodo))
            for succ in successori:
                if succ not in visitati:
                    daVisitare.append(succ)
            visitati.append(nodo)
        return visitati




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
        # self._listaVicini=[]
        # succ=self.getSuccessori(source,[])
        # # print(succ)
        # self.ricorsione(succ,[source])
        # for i in self._listaVicini:
        #     print(i)
        # return self._listaVicini
        self._listaVicini = []
        parziale=[source]
        succ=self.getSuccessori(source,parziale)
        self.ricorsione(succ,parziale)
        print (self._listaVicini)
        return self._listaVicini

    def ricorsione(self,successori,parziale):
        # print(parziale)
        # #print("chiamo ricorsione")
        # #non posso chimare sempre successori e sperare che sia vuota perchè tutti i nodi hanno dei successori
        # #devo controllare quando li creo che non siano in parziale
        # if len(successori)==0:
        #     self._listaVicini=copy.deepcopy(parziale)
        #     print("condizione terminale")
        #     print(self._listaVicini)
        # else:
        #     nodo_nuovo=parziale[-1]
        #     succ_nuovi = self.getSuccessori(nodo_nuovo, parziale)
        #     for s in succ_nuovi:
        #         parziale.append(s)
        #         self.ricorsione(succ_nuovi,parziale)
        #         parziale.pop()
        if len(successori)==0:
            if len(parziale)>len(self._listaVicini):
                #print("finito")
                self._listaVicini = copy.deepcopy(parziale)
        else:
            for nodo in successori:
                if nodo not in parziale:
                    parziale.append(nodo)
                    nuovi_successori=self.getSuccessori(nodo,parziale)
                    self.ricorsione(nuovi_successori,parziale)
                    parziale.pop()


    def getSuccessori(self,nodo_nuovo,parziale):
        # successori=list(self._grafo.neighbors(nodo_nuovo))
        # print(f"lunghezza successori completi: {len(successori)}")
        # possibili_successori=[]
        # for nodo in successori:
        #     if nodo not in parziale:
        #         possibili_successori.append(nodo)
        # print (f"linghezza possibili: {len(possibili_successori)}")
        # return possibili_successori
        tuttiSucc=list(nx.neighbors(self._grafo,nodo_nuovo))
        succ=[]
        for s in tuttiSucc:
            if s not in parziale:
                succ.append(s)
        return succ

    def componenteConnessaIterativa(self,source):
        daVisitare=[source]
        visitati=[]
        while len(daVisitare)!=0:
            for nodo in daVisitare:
                daVisitare.remove(nodo)
                successori = list(self._grafo.neighbors(nodo))
                for succ in successori:
                    if succ not in visitati:
                        daVisitare.append(succ)
                if nodo not in visitati:
                    visitati.append(nodo)
        return visitati




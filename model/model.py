import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
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



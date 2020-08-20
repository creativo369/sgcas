import collections
import matplotlib
from networkx import has_path

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from SGCAS.settings.desarrollo import MEDIA_ROOT

from django.shortcuts import get_object_or_404
from apps.fase.models import Fase
from apps.item.models import Item


def exclude_potencial_cycles(pk, id_fase, items_query):
    """
    Permite la busqueda de relaciones que conllevan a ciclos en el grafo para excluir el item correspondiente del queryset.<br/>
    **:param pk:** Es el nodo fuente sobre el cual se basa la busqueda de posibles ciclos.<br/>
    **:param id_fase:** id de la fase al cual pertenece el proyecto sobre el que se realizara el grafo.<br/>
    **:param items_query:** Es el queryset de los items que pueden relacionarse la instancia de item de turno en particular.<br/>
    **:return:** Un grafo no dirigido (En realidad los vertices (items) poseen relacion bidireccional).<br/>
    """
    lead_to_cycle = set()
    source_node = Item.objects.get(pk=pk)
    G = create_graph(id_fase)
    for vertex in items_query:
        G.add_edge(source_node, vertex)
        if bfs(G):
            lead_to_cycle.add(vertex)
        G.remove_edge(source_node, vertex)
    for vx in lead_to_cycle:
        items_query = items_query.exclude(pk=vx.pk)
    return items_query


def create_graph(id_fase):
    """
    Permite la creacion de un grafo de los items de un proyecto que se encuentra relacionados.<br/>
    **:param id_fase:** id de la fase al cual pertenece el proyecto sobre el que se realizara el grafo.<br/>
    **:return:** Un grafo no dirigido (En realidad los vertices (items) poseen relacion bidireccional).<br/>
    """
    print('Creating graph...')
    id_proyecto = get_object_or_404(Fase, pk=id_fase).proyecto.pk
    fases_query = Fase.objects.filter(proyecto=id_proyecto)
    node_list = []
    edge_list = []
    for fase in fases_query:  ##Adding nodes
        for item in Item.objects.filter(fase=fase):
            node_list.append(item)
    for fase in fases_query:  ##Adding edges
        for item in Item.objects.filter(fase=fase):
            for hijo in item.hijos.all():
                edge_list.append((item, hijo, {'weight': item.costo, 'costo': str(item.costo) + ' horas.'}))
            for sucesor in item.sucesores.all():
                edge_list.append((item, sucesor, {'weight': item.costo, 'costo': str(item.costo) + ' horas.'}))
    G = nx.Graph()
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)

    return G


def create_graph_trazabilidad(path):
    """
    Permite la creacion de la trazabilidad de un item.<br/>
    **:param path:** Recibe el path sobre el cual se desea realizar la trazabilidad.<br/>
    **:return:** Un grafo de tipo networkx.<br/>
    """

    node_list = [item for item in path]
    edge_list = []
    for node in node_list:
        if node_list.index(node) != (len(node_list) - 1):
            edge_list.append((node, node_list[node_list.index(node) + 1], {'costo': str(node.costo) + ' horas.'}))
        else:
            break
    G = nx.Graph()
    G.add_edges_from(edge_list)
    G.add_nodes_from(node_list)

    return G


def bfs(G):
    """
    Algoritmo Breadth First Search para deteccion de ciclos en el grafo.<br/>
    **:param G:** Recibe un grafo no dirigido de tipo networkx.<br/>
    **:return:** True si el grafo contiene ciclo y False si no contiene.<br/>
    """
    root = (list(G.nodes))[0]
    visited, queue = set(), collections.deque([root])
    visited.add(root)
    while queue:
        node = queue.popleft()
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
            else:
                if neighbor in queue:
                    return True
    return False


def draw_graph(G):
    """
    Genera una imagen con formato .png del grafo.<br/>
    **:param G:** Recibe un grafo no dirigido de tipo networkx.<br/>
    **:return:** Una imagen .png del grafo.<br/>
    """
    nx.draw_spring(G, with_labels=True)
    labels = nx.get_edge_attributes(G, 'costo')
    nx.draw_networkx_edge_labels(G, nx.spring_layout(G), edge_labels=labels)
    plt.savefig(MEDIA_ROOT + '/item_trazabilidad.png')
    plt.clf()


def shortest_path(source, target, id_fase):
    """
    Devuelve el camino mas corto a un item en el grafo.<br/>
    **:param source:** Es el item con el cual se da inicio al grafo en el proyecto.<br/>
    **:param target:** Es el item al cual se desea llegar.<br/>
    **:param id_fase:** Recibe el id de una fase el cual sirve como referencia para saber el proyecto.<br/>
    **:return:** Una imagen .png del grafo.<br/>
    """
    G = create_graph(id_fase)
    path = nx.shortest_path(G, source=source, target=target, weight='weight')
    return path


def item_has_path(id_fase, source, target):
    """
    Permite saber si un item contiene una ruta desde el comienzo del proyecto.<br/>
    **:param id_fase:** Recibe el id de una fase el cual sirve como referencia para saber el proyecto.<br/>
    **:param source:** Es el item con el cual se da inicio al grafo en el proyecto.<br/>
    **:param target:** Es el item al cual se desea llegar.<br/>
    **:return:** True si el item contiene un camino al inicio del proyecto, en otro caso, false.<br/>
    """
    return has_path(create_graph(id_fase), source, target)

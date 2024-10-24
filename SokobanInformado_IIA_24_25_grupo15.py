"""IIA Grupo 15: Pedro Marques n48674
                 Daniel Rodrigues n56912"""

def h_util(self, node):
    """Para cada objetivo (lugar de armazenamento), calcula a distância de Manhattan à caixa mais próxima
    que ainda não foi alocada, ignorando a existência de paredes e/ou obstáculos, e aloca essa caixa ao objetivo.
    O valor da heurística é a soma todas estas distâncias + a distância entre o sokoban e a caixa mais longínqua
    que ainda não está arrumada. Se estamos num estado final, devolve 0."""

    clone = copy.deepcopy(node.state)
    

    if self.goal_test(clone):
        return 0

    total_dist = 0
    caixas_removidas = set() 
    

    for objetivo in self.goal:
        menor_dist = float('inf')
        caixa_mais_proxima = None
        
        for caixa in clone['caixas']:
            if caixa in caixas_removidas:
                continue
            dist = manhattan(caixa, objetivo)
            if dist < menor_dist:
                menor_dist = dist
                caixa_mais_proxima = caixa

        if caixa_mais_proxima:
            total_dist += menor_dist
            caixas_removidas.add(caixa_mais_proxima)


    max_dist_sokoban = 0
    sokoban = clone['sokoban']
    for caixa in clone['caixas']:
        if caixa not in self.goal:
            dist_sokoban = manhattan(sokoban, caixa)
            if dist_sokoban > max_dist_sokoban:
                max_dist_sokoban = dist_sokoban

    return total_dist + max_dist_sokoban


def beam_search_plus_count(problem, W, f):
    """Beam Search: search the nodes with the best W scores in each depth.
       Return the solution and how many nodes were expanded."""
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node, 0

    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = set()
    nodes_expanded = 0

    while frontier:
        beam = []
        for _ in range(len(frontier)):
            node = frontier.pop()
            if problem.goal_test(node.state):
                return node, nodes_expanded
            
            if node.state not in explored:
                nodes_expanded += 1
                explored.add(node.state)
                for child in node.expand(problem):
                    if child.state not in explored and child not in beam:
                        beam.append(child)
                    elif child in beam:
                        incumbent = next(n for n in beam if n.state == child.state)
                        if f(child) < f(incumbent):
                            beam.remove(incumbent)
                            beam.append(child)
        beam.sort(key=lambda n: (f(n), n.path_cost, n.state))
        for node in beam[:W]:
            if node.state not in explored:
                frontier.append(node)

    return None, nodes_expanded


def IW_beam_search(problem, h):
    """IW_beam_search (Iterative Widening Beam Search) começa com beam width W=1 e aumenta W iterativamente até
    se obter uma solução. Devolve a solução, o W com que se encontrou a solução, e o número total (acumulado desde W=1)
    de nós expandidos. Assume-se que existe uma solução."""

    total_expanded_nodes = 0
    W = 1
    
    while True:
        solution, expanded_nodes = beam_search(problem, W, h)
        total_expanded_nodes += expanded_nodes
        
        if solution is not None:
            return solution, W, total_expanded_nodes
        
        W += 1
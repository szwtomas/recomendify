
ITERACIONES_DEFECTO = 500
AMORTIGUACION_DEFECTO = 0.85

def ranking_cancion(grafo, coeficiente_amortiguacion, cancion, rankings):
    termino_amortiguacion = (1 - coeficiente_amortiguacion) / grafo.cantidad_vertices()
    termino_ranking = 0
    for ady in grafo.obtener_adyacentes(cancion):
        termino_ranking += rankings[ady] / len(grafo.obtener_adyacentes(ady))
    return termino_amortiguacion + coeficiente_amortiguacion * termino_ranking

def page_rank_canciones(grafo, iteraciones = ITERACIONES_DEFECTO, coeficiente_amortiguacion = AMORTIGUACION_DEFECTO):
    rankings = {}
    #termino_amortiguacion = (1 - coeficiente_amortiguacion) / grafo.cantidad_vertices()
    for cancion in grafo.obtener_vertices():
        rankings[cancion] = 0.99 #CAMBIAR!! Es aprox 1/vertices o mayor
    for i in range(iteraciones):
        for cancion in grafo.obtener_vertices(): 
            rankings[cancion] = ranking_cancion(grafo, coeficiente_amortiguacion, cancion, rankings)
    lista_rankings = []
    for cancion in rankings:
        lista_rankings.append((rankings[cancion], cancion))
    lista_rankings.sort(key = lambda tupla: tupla[0])
    lista_rankings.reverse()
    return lista_rankings



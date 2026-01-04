# Funcion para determinar si un segmento intersecta un polígono
def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

# Determina si los segmentos s1 y s2 se intersectan
def intersectan(s1, s2):
    a, b = s1
    c, d = s2
    return (
        orient(a, b, c) * orient(a, b, d) < 0 and
        orient(c, d, a) * orient(c, d, b) < 0
    )

# Determina si el segmento p1-p2 intersecta el polígono pol
def segmento_intersecta_poligono(p1, p2, pol):
    for i in range(len(pol)):
        q1 = pol[i]
        q2 = pol[(i+1) % len(pol)]
        if intersectan((p1, p2), (q1, q2)):
            return True
    return False

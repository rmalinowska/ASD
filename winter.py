from typing import List
import random
import sys
import time

# Roksana Malinowska

class Node:

    def __init__(self, id):
        self.id = id
        self.parent = self
        self.rank = 0
        self.num_of_b = 0 # atrybut do odczytywania liczby budynków z reprezentanta drzewa
        self.kids = [] # lista dzieci do dfs w funkcji wypisywania wszystkich osiągalnych punktów


class StreetNetwork:
    def __init__(self, nb, ns):
        self.nb = nb
        self.ns = ns
        self.nodes = {i: Node(i) for i in range(nb+ns)}
        for i in range(nb):
            self.nodes[i].num_of_b += 1

    def find(self, x):
        # funkcja znajdująca reprezentanta drzewa, w którym znajduje się x stosująca kompresję ścieżek
        if self.nodes[x].parent.id == self.nodes[x].id:
            return self.nodes[x].parent
        self.nodes[x].parent = self.find(self.nodes[x].parent.id)
        return self.nodes[x].parent

    def clear(self, x, y):
        # funkcja będąca odpowienikiem funkcji union, na podstawie rang wybiera, które drzewo zostanie podczepione pod które
        x_repr = self.find(x)
        y_repr = self.find(y)
        if x_repr.id == y_repr.id:
            # gdy dwa wierzchołki są w tym samym drzewie to wykonywanie funkcji zostaje zatrzymane
            return
        if x_repr.rank > y_repr.rank:
            y_repr.parent = x_repr
            x_repr.num_of_b += y_repr.num_of_b
            x_repr.kids.append(y_repr)
        elif x_repr.rank < y_repr.rank:
            x_repr.parent = y_repr
            y_repr.num_of_b += x_repr.num_of_b
            y_repr.kids.append(x_repr)
        else:
            y_repr.parent = x_repr
            x_repr.rank += 1
            x_repr.num_of_b += y_repr.num_of_b
            x_repr.kids.append(y_repr)

    def number_of_reachable_buildings(self, x):
        x_repr = self.find(x)
        return x_repr.num_of_b

    def list_reachable_points(self, x):
        x_repr = self.find(x)
        result = []

        def dfs(node):
            result.append(node.id)
            for kid in node.kids:
                dfs(kid)

        dfs(x_repr)
        return result

# Testy.


print('Wstępne testy...')

# Przykład z treści zadania.
sn = StreetNetwork(3, 1)
sn.clear(0, 3)
sn.clear(1, 3)
assert set(sn.list_reachable_points(0)) == {0, 1, 3}
assert sn.number_of_reachable_buildings(1) == 2
assert sn.number_of_reachable_buildings(2) == 1
sn.clear(0, 2)
assert sn.number_of_reachable_buildings(2) == 3

# Inny przykład; stopniowo odśnieżamy wszystkie ulice.
sn = StreetNetwork(3, 3)
for i in range(3):
    assert sn.number_of_reachable_buildings(i) == 1
    assert sn.list_reachable_points(i) == [i]
for i in range(3):
    sn.clear(i, i+3)
for i in range(3):
    assert sn.number_of_reachable_buildings(i) == 1
    assert sn.list_reachable_points(i) in ([i, i+3], [i+3, i])
sn.clear(2, 3)
assert sn.number_of_reachable_buildings(0) == 2
assert sn.number_of_reachable_buildings(2) == 2
assert set(sn.list_reachable_points(0)) == {0, 2, 3, 5}
assert sn.number_of_reachable_buildings(1) == 1
assert sn.list_reachable_points(1) in ([1, 4], [4, 1])
sn.clear(0, 2)
sn.clear(0, 5)
sn.clear(3, 5)
assert sn.number_of_reachable_buildings(0) == 2
assert sn.number_of_reachable_buildings(2) == 2
assert set(sn.list_reachable_points(0)) == {0, 2, 3, 5}
assert sn.number_of_reachable_buildings(1) == 1
assert sn.list_reachable_points(1) in ([1, 4], [4, 1])
sn.clear(4, 2)
for i in range(3):
    assert sn.number_of_reachable_buildings(i) == 3
    assert set(sn.list_reachable_points(i)) == {0, 1, 2, 3, 4, 5}
sn.clear(0, 1)
sn.clear(0, 4)
sn.clear(1, 2)
sn.clear(1, 3)
sn.clear(1, 5)
sn.clear(3, 4)
sn.clear(4, 5)
for i in range(3):
    assert sn.number_of_reachable_buildings(i) == 3
    assert set(sn.list_reachable_points(i)) == {0, 1, 2, 3, 4, 5}

print('Wstępne testy zaliczone!')

# Testy automatyczne. Kilka rzeczy losujemy, ale nie powinny mieć wpływu na wynik.


def equal_unordered_lists(l1: List[int], l2: List[int]):
    return len(l1) == len(l2) and set(l1) == set(l2)


print('Małe testy...')

# Ścieżki (odśnieżamy tylko drogi (x, x+1)).


def test_path(nb: int, ns: int, asserts: bool):
    points = list(range(nb+ns))
    sn = StreetNetwork(nb, ns)
    # Czyścimy drogi (x, x+1); czasem wywołujemy clear(x, x+1), czasem clear(x+1, x).
    for x, y in zip(points, points[1:]):
        if asserts and y < nb:
            assert sn.list_reachable_points(y) == [y]
        if x % 2:
            sn.clear(x, y)
        else:
            sn.clear(y, x)
        if asserts:
            assert sn.number_of_reachable_buildings(
                random.randint(0, min(nb-1, y))) == min(nb, y+1)
    assert equal_unordered_lists(
        sn.list_reachable_points(random.randint(0, nb-1)), points)
    assert sn.number_of_reachable_buildings(random.randint(0, nb-1)) == nb


for nb in range(1, 10):
    for ns in range(1, 10):
        test_path(nb, ns, asserts=True)
        test_path(nb, ns, asserts=False)

# Drzewa binarne (odśnieżamy drogi (x, 2x+1) i (x, 2x+2), jak w kopcu [z indeksowaniem od 0], od dołu).


def test_bintree(nb: int, ns: int, asserts: bool):
    sn = StreetNetwork(nb, ns)
    reach = [1] * nb + [0] * ns
    for x in reversed(range(1, nb+ns)):
        if asserts and x < nb:
            assert sn.number_of_reachable_buildings(x) == reach[x]
        if x % 2:
            sn.clear(x, (x-1)//2)
        else:
            sn.clear((x-1)//2, x)
        reach[(x-1)//2] += reach[x]
        if asserts and x < nb:
            assert sn.number_of_reachable_buildings(x) == reach[(x-1)//2]


for nb in range(1, 10):
    for ns in range(1, 10):
        test_bintree(nb, ns, asserts=True)
        test_bintree(nb, ns, asserts=False)

print('Małe testy zaliczone!')

# Duże testy.

print('Duże testy wydajnościowe...')


def test_performance(desc: str, test):
    print(desc, end='... ')
    sys.stdout.flush()
    beg = time.time()
    test()
    end = time.time()
    print(f'{end-beg:.3f}s')


test_performance('Ścieżka długości 100 000, głównie clear',
                 lambda: test_path(50001, 49999, asserts=False))
test_performance('Ścieżka długości 100 000, z dodatkowymi sprawdzeniami',
                 lambda: test_path(50001, 49999, asserts=True))
test_performance('Drzewo binarne wielkości 100 000, głównie clear',
                 lambda: test_bintree(50001, 49999, asserts=False))
test_performance('Drzewo binarne wielkości 100 000, z dodatkowymi sprawdzeniami',
                 lambda: test_bintree(50001, 49999, asserts=True))

print('1000 budynków, 1000 skrzyżowań; najpierw odśnieżamy wszystko, później pytamy o osiągalne punkty.')
nb = ns = 1000
sn = StreetNetwork(nb, ns)
n = nb + ns
print('\tOdśnieżam wszystkie drogi; może to chwilę potrwać', end='... ')
sys.stdout.flush()
beg = time.time()
for i in range(n):
    for j in range(i+1, n):
        sn.clear(i, j)
end = time.time()
print(f'wszystkie drogi odśnieżone! {end-beg:.3f}s')
print('\tPytam o listę wszystkich punktów osiągalnych z 0; to powinno zadziałać bardzo(!) szybko', end='... ')
sys.stdout.flush()
beg = time.time()
assert equal_unordered_lists(sn.list_reachable_points(0), list(range(n)))
end = time.time()
print(f'zrobione! {end-beg:.3f}s')

from datetime import datetime, date, time
from math import dist, inf
from typing import List, Tuple
from numpy import empty
from numpy.core.numeric import Infinity
from numpy.lib.function_base import append
from numpy.matrixlib.defmatrix import matrix
import time
import random


class Sample:
    sample_id: str
    country: str
    date: datetime.date
    seq: str
    index: int
    distance: int
    children: list

    def __init__(self, id, country, date, seq):
        self.sample_id = id
        self.country = country
        self.date = date
        self.seq = seq
        self.children = []
        self.distance = None
        self.parent = None

    def copy_sample(self):
        return Sample(self.sample_id, self.country, self.date, self.seq)


def printTree(node, level=0):
    print(' ' * 6 * level + '->', node.sample_id, node.country)
    for child in node.children:
        printTree(child, level + 1)


class Tree:
    def __init__(self):
        self.root = None
        self.cost = 0

    def edges(self) -> List[Tuple[str, str]]:

        res = []

        def req(sample):
            # Funkcja rekurencyjna przechodząca po wierzchołkach w głąb i dodająca do listy res tuple postaci (id próbki, id dziecka próbki).
            for child in sample.children:
                res.append((sample.sample_id, child.sample_id))
                req(child)
        req(self.root)

        return res

    def filter(self, country: str) -> List['Tree']:

        result = []  # ostatecznie będzie to lista drzew po przefiltrowaniu drzewa po kraju

        def find_children(parent, nodes):
            # Funkcja rekurencyjna, która znajduje wszystkie dzieci wierzchołka parent, które powinny być w nowym drzewie i dodaje je do parent.children.
            # Działa na podstawie przeszukiwania każdej gałęzi w dół, aż nie znajdziemy dziecka lub aż drzewo się nie skończy.
            if nodes != []:  # jeśli drzewo się nie skończyło
                for node in nodes:
                    if node.country == country:  # jeśli kraj się zgadza z podanym przy wywołaniu funkcji filter
                        # tworzenie nowej próbki z przepisanymi odpowiednimi atrybutami
                        new_child = node.copy_sample()
                        # dodawanie próbki jako dziecko
                        parent.children.append(new_child)
                        # szukanie dzieci dla kolejnego wierzchołka w głąb
                        find_children(new_child, node.children)
                    else:
                        # jeśli node nie jest dzieckiem parent, to przeszukujemy poziom niżej tzn. dzieci node
                        find_children(parent, node.children)

        def subtree(node):
            # Funkcja znajduje wierzchołki, które będą korzeniami nowych drzew i wywołuje na nich funkcję find_children <=> tworzy drzewa zaczynające się w tych wierzchołkach.
            if node.country == country:
                T = Tree()
                T.root = node.copy_sample()
                find_children(T.root, node.children)
                result.append(T)
            else:
                if node.children != []:
                    for child in node.children:
                        subtree(child)

        # rozpoczęcie szukania nowych korzeni i tworzenia drzew we własnym korzeniu
        subtree(self.root)

        return result


def read_data(filename: str) -> List[Sample]:
    # Funkcja tnie plik fasta na pojedyncze próbki i wyciąga informacje o nich, dodaje próbki do listy, sortuje je po dacie i zapamiętuje tę kolejność.
    with open(filename) as f:
        text = f.read().split(">")
        result = []
        for sample in text[1:]:
            sample = sample.strip().split("\n")
            seq = sample[1]
            sample = sample[0].split("|")
            obj = Sample(sample[0], sample[1], datetime.strptime(
                sample[2], "%Y-%m-%d"), seq)
            result.append(obj)
        result = sorted(result, key=lambda x: x.date)
        for i in range(len(result)):
            result[i].index = i
        return result


def count_edit_len(seq1: str, seq2: str):
    # Funkcja dynamicznie liczy odległość edycyjną dla dwóch sekwencji. Opiera się na globalnym uliniowieniu z karą wszędzie równą +1.
    matrix = empty((len(seq1)+1, len(seq2)+1), 'int')
    matrix[0, 0] = 0
    for i in range(len(seq1)):
        matrix[i+1, 0] = i+1
    for j in range(len(seq2)):
        matrix[0, j+1] = j+1
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                cost = 0
            else:
                cost = 1
            matrix[i+1, j+1] = min(matrix[i, j+1]+1,
                                   matrix[i+1, j]+1, matrix[i, j]+cost)
    return matrix[len(seq1), len(seq2)]


def construct_optimal_tree(samples: List[Sample]) -> Tree:
    # Funkcja tworzy optymalne drzewo na podstawie podanej listy próbek.
    # Polega na szukaniu rodzica każdej próbki poprzez liczenie odległości edycyjnych od jej sekwencji do sekwencji wszystkich starszych od niej próbek
    # i wybieraniu pierwszej próbki o najmniejszej odległości, a następnie dodawaniu do jej dzieci tej próbki. Nie ustawiam tutaj atrybutu parent, bo nie jest to potrzebne przy budowaniu optymalnego drzewa.
    T = Tree()
    T.root = samples[0]
    for s in samples:
        if s.index == 0:
            continue
        else:
            min = Infinity
            best = None
            for i in range(s.index):
                d = count_edit_len(s.seq, samples[i].seq)
                if d < min:
                    min = d
                    best = samples[i]
            s.distance = min
            best.children.append(s)
            T.cost += min
    return T


def construct_approximate_tree(samples: List[Sample]) -> Tree:
    T = Tree()
    T.root = samples[0]
    for sample in samples[1:]:
        candidates = {}  # {kandydat:odległość do niego,...}
        checked = {}  # {próbka:odległość do niej,...}, zapobieganie liczenia tych samych odległości kilkukrotnie

        def better(node, distance):
            # Funkcja zwracająca None jeśli node jest kandydatem na rodzica próbki lub zwracająca jego sąsiada, do którego trzeba się następnie udać.
            neighbours = node.children
            if node.parent is not None:
                neighbours = neighbours + [node.parent]
            next = None
            better_dist = distance
            for neigh in neighbours:
                if neigh not in checked:
                    d = count_edit_len(sample.seq, neigh.seq)
                    checked[neigh] = d
                    # jeśli odległość edycyjna od danej próbki do sąsiada jest mniejsza niż obecna najlepsza (początkowo podana przy wywołaniu)
                    if d < better_dist:
                        # jeśli dla żadnego sąsiada ten warunek nie zostanie spełniony to node jest kandydatem, zwracany jest None
                        better_dist = count_edit_len(sample.seq, neigh.seq) # zapamiętuję najlepszą obecnie odległość
                        next = neigh  # zapamiętuję, dla którego wierzchołka
                else:
                    continue
            return next  # jak None, to żaden sąsiad nie ma odl mniejszej niż distance

        def find_cand(rand):
            # Funkcja szukająca kandydatów na rodzica próbki rozpoczynając od rand.
            dist = count_edit_len(sample.seq, rand.seq)
            res = better(rand, dist)
            if res is None:
                candidates[rand] = dist
            else:
                find_cand(res)
        for i in range(3):
            # Trzykrotne losowanie jakiejś starszej próbki <=> będącej już w drzewie i wywoływanie na niej funkcji find_cand.
            rdm = random.choice(samples[:sample.index])
            find_cand(rdm)

        # Znajdowanie najlepszego z kandydatów i ustawianie atrybutów
        winner = None
        shortest = float('inf')
        for cand in candidates:
            if candidates[cand] < shortest:
                shortest = candidates[cand]
                winner = cand

        sample.parent = winner  # Ustawiam najlepszego kandydata jako rodzica.
        winner.children.append(sample)  # Dodaję do jego dzieci sample.
        T.cost += candidates[winner]  # Liczenie kosztu drzewa.

    return T


def test(filename):
    L = read_data(filename)
    beg = time.time()
    T = construct_optimal_tree(L)
    end = time.time()
    print(filename, "Koszt optymalnego drzewa: ",
          T.cost, f'Czas wykonania: {end-beg:.2f}s')

# test("all1024seq5.fasta")
# test("bin31seq60mut3.fasta")
# test("bin63seq120mut3.fasta")
# test("break61_seq60_mut3.fasta")
# test("small1.fasta")
# test("small2.fasta")


def test2(filename):
    L = read_data(filename)
    beg = time.time()
    T = construct_approximate_tree(L)
    end = time.time()
    print(filename, "Koszt drzewa utworzonego szybciej: ",
          T.cost, f'Czas wykonania: {end-beg:.2f}s')

# test2("all1024seq5.fasta")
# test2("bin31seq60mut3.fasta")
# test2("bin63seq120mut3.fasta")
# test2("break61_seq60_mut3.fasta")
# test2("small1.fasta")
# test2("small2.fasta")


def test_filter(filename, country):
    L = read_data(filename)
    T = construct_optimal_tree(L)
    trees = T.filter(country)
    print("Wynik testu: ", trees)


# test_filter("small2.fasta", "China")
# test_filter("small2.fasta", "Greenland")
# test_filter("break61_seq60_mut3.fasta",'Spain')

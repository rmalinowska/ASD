#Weronika Trawińska i Roksana Malinowska
from typing import Any, Optional

# Pomocnicza funkcja, dodająca spację na początku każdej linijki w napisie.
def indent(s: str) -> str:
    return '\n'.join(' '+line for line in s.splitlines())

class PosBinNode:
    # Pola poniżej należą do instancji, nie do klasy! (nie są statyczne)
    # Gdyby nie było typów, zmienna zadeklarowana tutaj byłaby statyczna.
    value: Any
    left: Optional['PosBinNode']
    right: Optional['PosBinNode']
    size: int

    def __init__(self,
                 value: Any,
                 left: Optional['PosBinNode'] = None,
                 right: Optional['PosBinNode'] = None):
        self.value = value
        self.left = left
        self.right = right
        self.size = -1
    
    # Prosta pomocnicza funkcja do wypisywania (pod)drzewa (można napisać własną, bardziej czytelną).
    def __str__(self):
        return f'{self.value} (size: {self.size})\n{indent(str(self.left))}\n{indent(str(self.right))}'

    def size_of_subtree(self):
        value = 0
        if self.left is not None:
            self.left.size = 1 + self.left.size_of_subtree()   # rozmiar lewego syna to rozmiar jego poddrzew/a + on sam
            value += self.left.size
        if self.right is not None:
            self.right.size = 1 + self.right.size_of_subtree()    # analogicznie dla prawego syna
            value += self.right.size    # value to rozmiar poddrzew/a wierzchołka, dla którego wywołujemy funkcję
        return value


class PosBinTree:
    # Pole "root" należy do instancji, nie do klasy! (nie jest statyczne)
    root: Optional[PosBinNode]

    def __init__(self, node: Optional[PosBinNode] = None):
        self.root = node
    
    def calculate_sizes(self):
        if self.root is None: return None 
        self.root.size = self.root.size_of_subtree() + 1


    def find_centroid(self) -> Optional[PosBinNode]:
        if self.root is None: return None
        n = self.root.size

        def centro(node: PosBinNode):
            if node.size - 1 <= n//2:     # zwroci nam korzen tylko wtedy gdy jest on cetroidem; poniewaz poruszamy sie po drzewie przechodzac na syna ktorego wielkosc jest wieksza nie dojdzie do sytuacji ze zwroci nam cos nie bedacego centroidem
                return node
            if node.left is not None:
                if node.right is not None:         # wierzcholek ma 2 synow
                    if node.left.size > n//2:     # wielkosc lewego syna jest > niz n//2, wiec idziemy w lewo
                        return centro(node.left)
                    elif node.right.size > n//2:     # wielkosc prawego syna jest > niz n//2, wiec idziemy w prawo
                        return centro(node.right)
                    else:
                        return node     # lewy i prawy syn są tej samej wielkości <= n//2, więc mamy centroid
                else:
                    return centro(node.left)         # wierzcholek ma tylko lewego syna, ktorego wielkosc nie jest <= n//2
            if node.right is not None and node.left is None:       # wierzcholek ma tylko prawego syna, ktorego wielkosc nie jest <= n//2
                return centro(node.right)

        return centro(self.root)

    def __str__(self):
        return '(Empty tree)' if self.root is None else str(self.root)

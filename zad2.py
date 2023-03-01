# Roksana Malinowska i Mateusz Sikorski
from typing import Any, List, Optional


def moves_sequence(board: str, moves: List[int]) -> Optional[List[int]]:
    # TODO: napisz tę funkcję (lub tylko uzupełnij funkcje pomocnicze).
    # Powinna zwracać listę liczb (długości skoków) lub None, jeśli nie da się dojść do ostatniego pola.
    # Sugerowany podział na funkcje (ale można swobodnie zmieniać argumenty / zwracane wartości,
    # albo napisać całkiem po swojemu):
    intermediate_information = does_sequence_exist(board, moves)
    if intermediate_information is None: return None
    return calculate_sequence(board, moves, intermediate_information)


def does_sequence_exist_dict(board: str, moves: List[int]) -> Any:
    # Sugerowana pierwsza część zadania: sprawdzenie, czy w ogóle da się dojść do ostatniego pola.
    # Przy okazji powinna obliczać jakieś dodatkowe informacje, które będą potrzebne do drugiej części zadania.
    # Jeśli nie da się dojść, powinna zwrócić None.
    """
    Funkcja alternatywna do rozwiązania z DFS. Tworzy słownik, w którym kluczami są indeksy pól, a wartościami tablice z indeksami pól, z których
    da się tam dotrzeć. Zwraca ten słownik, gdy istnieje sekwencja skoków z 0 do n-1 oraz None w p.p.
    """
    result = dict((i, []) for i in range(len(board)))
    entry = False #informuje o tym, czy da się ruszyć z pierwszego pola
    board = list(board)
    for i in range(len(board)):
        if i == 0:
            #Oddzielna pętla dla pierwszego pola, by móc zatrzymać funkcję, gdy nie da się wykonać żadnego ruchu.
            for mv in moves:
                if i + mv < len(board):
                    if board[i + mv] != 'X':
                        entry = True #True, jeśli jakikolwiek ruch z pierwszego pola jest możliwy, wtedy przechodzimy dalej już do końca
                        result[i + mv].append(i)
                        board[i + mv] = True
            if entry == False: return None
        else:
            for mv in moves:
                if i + mv < len(board): #sprawdzam, czy indeks, do którego chce się udać, nie wychodzi poza planszę
                    if board[i] == True: #sprawdzam, czy da się dotrzeć do danego pola
                        if board[i + mv] != 'X':
                            result[i + mv].append(i) #dodaję do wartości indeksu i+mv pole, z którego da się tam dotrzeć
                            board[i + mv] = True #przypisanie wartości True na pole, na które da się dojść idąc od początku
    if result[len(board) - 1]: #zwracany jest słownik, gdy dla ostatniego pola lista pól, z których da się tam dojść, nie jest pusta
        return result
    return None #w p.p.


def does_sequence_exist(board: str, moves: List[int]) -> Any:
    """
    Funkcja zwracająca listę 0 i 1 (1, gdy da się dojść na dale pole i 0 w p.p.), gdy istnieje sekwencja skoków z 0 do n-1 oraz None, jeśli nie istnieje.
    Funkcja iteruje od początku, natomiast funkcja wyznaczająca sekwencję skoków od końca, więc mamy pewność, że idąc od końca i natrafiając na pole o wartości 1,
    da się na nie dotrzeć startując z zera.
    """
    board = list(board)
    result = [1] + [0] * (len(board) - 1)
    for i in range(len(board)):
        for mv in moves:
            if i + mv < len(board):
                if board[i] == True or i == 0: #sprawdzam, czy da się dojść na to pole
                    if board[i + mv] != 'X': #czy kolejne pole nie jest zablokowane
                        result[i + mv] = 1
                        board[i + mv] = True
    if result[len(board) - 1] == 1: return result #zwracana jest lista, jeśli ostatnie pole == 1 <=> da się na nie dotrzeć
    return None

# does_sequence_exist z tablicą ma lepszą złożoność czasową O(n) zamiast O(nk)

def calculate_sequence_dfs(board: str, moves: List[int], info: Any) -> List[int]:
    # Sugerowana druga część zadania: odtworzenie rozwiązania (listy skoków) z informacji policzonych w pierwszej części.
    """
    Gorsze rozwiązanie korzystające ze słownika, ale bardzo łatwo można przerobić, żeby działało z tablicą
    implementuje DFS'a znajdującego dowolną ścieżkę do 0, wybrałem DFS'a bo interesuje nas dowolna ścieżka,
    DFS będzie chyba działał szybciej niż BFS(ale BFS może nam zwrócić najkrótszą)

    złożoność czasowa - powinna być O(n + nk)
    złożoność pamięciowa - chyba nie najlepsza z uwagi na to, że dla każdego wierzchołka zapisuję ścieżkę do niego samego

    jestem ciekaw jak wyglądałaby wydajna pamięciowo implementacja znajdująca taką dowolną ścieżke
    """

    start_node = len(board) - 1

    stack = [(start_node, [start_node])]
    discovered = set()

    answer = None
    while stack:
        node, path = stack.pop()
        if node not in discovered:
            discovered.add(node)
            for edge in info[node]:
                if edge == 0:
                    answer = path + [edge]
                    break
                stack.append((edge, path + [edge]))

    if answer:
        output = []
        for i in range(len(answer) - 1):
            output.append(answer[i] - answer[i + 1])
        return output[::-1]
    return []


def calculate_sequence(board: str, moves: List[int], info: Any) -> List[int]:
    """
    moja najlepsza implementacja, ze złożonością czasową w najgorszym wypadku chyba O(nk) i pamięciową O(n)
    dla info w postaci tablicy.

    Działa w ten sposób:
    skoro wiem, że doszedłem do ostatniego pola to wiem, że jakoś doszedłem do tego z którego przyszedłem
    czyli iterując po MOVES mamy pewność, że conajmniej jeden z ruchów będzie tym który nas tutaj przyprowadził,
    gdy go znajdziemy, cofamy się o "move" do niego "tmp".
    Postępuje tak do samego początku, tutaj też ciekawa rzecz, wiadomo, że zaczeliśmy od 0,
    więc mamy pewność, że do niego dojdziemy
    """

    answer = []
    index = len(board) - 1
    while index != 0:
        for move in moves:
            tmp = index - move
            if tmp >= 0 and info[tmp]:
                index = tmp
                answer.append(move)
                break

    return list(reversed(answer))


def gen_dict(n):
    """ funkcja generująca info4 dla rozwiązania słownikowego """
    slownik = {i: [] for i in range(n + 1)}
    num = 4
    for i in range(2, n + 1):
        if i == num:
            num += 3
        else:
            if i == num - 2:
                slownik[i] = [i - 2]
            elif i == num - 1:
                slownik[i] = [i - 1]
    return slownik


def gen_array(n):
    """ funkcja generująca info4 dla rozwiązania tablicowego """
    array = [1 for _ in range(n + 1)]
    num = 1
    for i in range(n + 1):
        if i == num:
            array[num] = 0
            num += 3
    return array


# Spójrz też na kod poniżej!

# Skrypt testujący zaimportuje funkcję "moves_sequence" z tego pliku.
# Ten warunek pozwala na to, żeby przy importowaniu nie uruchomił się kod poniżej.
if __name__ == '__main__':
    # Pierwszy przykład z treści zadania.
    board1 = '..X.X..'
    moves1 = [1, 2]
    print('Pierwszy test z treści zadania:', board1, moves1)
    print('does_sequence_exist:', does_sequence_exist(board1, moves1))

    info1_array = [1, 1, 0, 1, 0, 1, 1]
    info1_dict = {0: [], 1: [0], 2: [], 3: [1], 4: [], 5: [3], 6: [
        5]}
    info1 = info1_array
    # Wpisz ręcznie dane, jakie ma wyliczyć funkcja does_sequence_exist (najlepiej przed rozpoczęciem pracy nad rozwiązaniem).

    print('calculate_sequence:', calculate_sequence(board1, moves1, info1))
    print('moves_sequence:', moves_sequence(board1, moves1))
    # Poprawna odpowiedź: [1, 2, 2, 1].

    board2 = '..XX..'
    moves2 = [1, 2]
    print('Drugi test z treści zadania:', board2, moves2)
    print('does_sequence_exist:', does_sequence_exist(board2, moves2))
    # Nie ma sensu testować pozostałych funkcji - does_sequence_exist powinno zwrócić None.

    board3 = '...X.X..'
    moves3 = [1, 3]
    print('Trzeci test z treści zadania:', board3, moves3)
    print('does_sequence_exist:', does_sequence_exist(board3, moves3))

    info3_array = [1, 1, 1, 0, 1, 0, 0, 1]
    info3_dict = {0: [], 1: [0], 2: [1], 3: [], 4: [1], 5: [], 6: [],
                  7: [4]}
    info3 = info3_array  # Wpisz ręcznie dane, które ma wyliczyć funkcja does_sequence_exist.
    print('calculate_sequence:', calculate_sequence(board3, moves3, info3))
    print('moves_sequence:', moves_sequence(board3, moves3))
    # Poprawna odpowiedź: [1, 3, 3].

    board4 = '.X.' * 50000  # Powtarzamy ten napis 50 000 razy; powstaje plansza ".X..X..X..X..X.", i tak dalej.
    moves4 = [1, 2]
    print('Bardzo duży test (plansza o długości 150 000, ale tylko dwa możliwe ruchy)')
    print('does_sequence_exist (None czy nie None):',
          'None' if does_sequence_exist(board4, moves4) is None else 'nie None')
    # Docelowo powinno wypisać "nie None".

    info4_array = gen_array(len(board4))
    info4_dict = gen_dict(len(board4))  # Oczywiście nie ma sensu wpisywać tych danych ręcznie.
    info4 = info4_array
    # (choć może da się napisać prostą funkcję, która je uzupełni, dla tego konkretnie testu?)
    # Natomiast warto przeliczyć, jak dużo danych tutaj będzie. Chcemy uniknąć O(n^2).
    # (150 000 * 150 000 to 22.5 miliarda; tyle liczb to może być z 90GB w pamięci RAM...)
    print('calculate_sequence:', calculate_sequence(board4, moves4, info4))
    print('moves_sequence:', moves_sequence(board4, moves4))
    # Jest tylko jedna poprawna sekwencja: [2, 1, 2, 1, 2, 1, 2, 1, ...].

    board5 = '............'
    moves5 = [2, 3]
    print('Test bez zablokowanych pól (12 pól):', board5, moves5)
    print('does_sequence_exist:', does_sequence_exist(board5, moves5))

    info5_array = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    info5_dict = {0: [], 1: [], 2: [0], 3: [0], 4: [2], 5: [2, 3], 6: [3, 4], 7: [4, 5], 8: [5, 6], 9: [6, 7],
                  10: [7, 8], 11: [8, 9]}  # Wpisz ręcznie dane, które ma wyliczyć funkcja does_sequence_exist.
    info5 = info5_array
    print('calculate_sequence:', calculate_sequence(board5, moves5, info5))
    print('moves_sequence:', moves_sequence(board5, moves5))
    # Tu jest wiele poprawnych odpowiedzi:
    # [2, 2, 2, 2, 3]
    # [2, 3, 3, 3]
    # ...albo dowolne przemieszanie powyższych ([2, 2, 3, 2, 2] i tak dalej).

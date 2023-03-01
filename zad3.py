
#Roksana Malinowska

def Parent(i):
    return i//2   

def Left(i):
    return i*2   

def Right(i):
    return i*2+1

class League:
    def __init__(self):
        self.players = [None] # lista w postaci [None, słowniki dla każdego zawodnika, gdzie słownik wygląda tak: {'name':'jakieśImię','score':jakiśInt}]
        self.names={} # Dodatkowy słownik do trzymania indeksów postaci {'konkretneImię':indeks_w_liście_self.players,...}
        r = len(self.players)//2
        for i in range(r, 0, -1):
            self.DownHeap(i)

    def UpHeap(self, i):
        # Zamiast self.heap[i] mamy self.players[i]['score'] - wartością do porównywania jest score.
        # Dodatkowe operacje do zmieniania indeksów w słowniku self.names.
       while i>1 and self.players[i]['score']>self.players[Parent(i)]['score']:
          self.players[i],self.players[Parent(i)] = self.players[Parent(i)],self.players[i]
          self.names[self.players[Parent(i)]['name']], self.names[self.players[i]['name']]= Parent(i), i
          i = Parent(i)

    def DownHeap(self, i):
        # Jak wyżej
       while True:
          MaxEl = i
          for j in (Left(i), Right(i)):
             if j<len(self.players) and self.players[j]['score']>self.players[MaxEl]['score']:
                MaxEl = j
          if MaxEl!=i:
             self.players[i],self.players[MaxEl] = self.players[MaxEl],self.players[i]
             self.names[self.players[MaxEl]['name']], self.names[self.players[i]['name']]=MaxEl, i
             i = MaxEl
          else: break
    
    def ReplaceMax(self, x):
        self.names.pop(self.players[1]['name']) # usuwam ze słownika self.names najlepszego zawodnika
        x,self.players[1] = self.players[1],x
        self.names[self.players[1]['name']] = 1 # x jest teraz na pierwszym miejscu w liście
        self.DownHeap(1)
        return x['name']


    def add_player(self, name: str):
        self.players.append({'name':name, 'score':0})
        self.names[name]=len(self.players)-1 # dodawany zawodnik jest w pierwszym momencie na ostatnim miejscu w kolejce
        # self.UpHeap(len(self.players)-1) # jednak niepotrzebne, bo ma teraz score 0, więc niech zostanie na końcu
    

    def change_score(self, name: str, score: int):
        i = self.names[name] # właśnie po to powstał słownik self.names (o wiele szybsze wyszukiwanie indeksu niż w pętli for)
        if self.players[i]['score']<score: # jak zwiększamy score to zmieniamy i przeciągamy w górę
            self.players[i]['score']=score
            self.UpHeap(i)
        else: # jak zmniejszamy score to zmieniamy i przeciągamy w dół
            self.players[i]['score']=score
            self.DownHeap(i)

    def pop_best_player(self) -> str:
        x = self.players.pop()
        if len(self.players)>1:
            return self.ReplaceMax(x) # usuwanie jest w ReplaceMax
        else:
            self.names.pop(x['name']) # usuwanie ze słownika z indeksami ostatniego zawodnika
            return x['name']

    

# Kod poniżej się nie wykona przy importowaniu tego pliku (jest to przydatne przy testowaniu).
if __name__ == '__main__':
    # Przykład z treści zadania.
    l = League()
    l.add_player('A')  
    l.add_player('B')
    l.add_player('C') 
    l.change_score('A', 5)  
    l.change_score('B', 15)
    l.change_score('A', 20)
    l.change_score('C', 10)
    print(l.pop_best_player()) # 'A'
    l.change_score('B', 1)
    print(l.pop_best_player())  # 'C'
    l.add_player('D')
    print(l.pop_best_player())  # 'B'
    print(l.pop_best_player())  # 'D'
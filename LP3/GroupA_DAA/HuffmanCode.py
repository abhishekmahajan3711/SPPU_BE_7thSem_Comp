import heapq 
class Node: 
    def __init__(self, freq, char, l=None, r=None): 
        self.freq = freq 
        self.char = char 
        self.l = l 
        self.r = r 
        self.code = '' 

    def __lt__(self, other): 
        return self.freq < other.freq 

def generateCodes(node, code_val=''): 
    code_val += str(node.code) 
    if node.l: 
        generateCodes(node.l, code_val) 
    if node.r: 
        generateCodes(node.r, code_val) 
    if not node.l and not node.r: 
        print(f"{node.char} -> {code_val}") 


n = int(input("Enter the number of characters: "))
chars = []
freqs = []

for i in range(n):
    char = input(f"Enter character {i+1}: ")
    chars.append(char)
    freq = int(input(f"Enter frequency of {char}: "))
    freqs.append(freq)

heap = [] 

for i in range(len(chars)): 
    heapq.heappush(heap, Node(freqs[i], chars[i])) 

while len(heap) > 1: 
    l = heapq.heappop(heap) 
    r = heapq.heappop(heap) 
    l.code = 0
    r.code = 1
    new_node = Node(l.freq + r.freq, l.char + r.char, l, r) 
    heapq.heappush(heap, new_node) 

print("Huffman Codes:")
generateCodes(heap[0])

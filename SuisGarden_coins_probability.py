import sys
import math
import collections
import functools
import heapq

# 增加遞迴深度限制（Python 預設只有 1000，寫 DFS 必加）
sys.setrecursionlimit(2000)

def single_coins_probs():
    try:
        print('---輸入通寶資訊---')
        counts = list(map(int, input('擁有 [花錢 衡錢 厲錢]: ').split()))    
        n = int(input('擲出通寶數: '))
        requires = list(map(int, input('需要擲出 [花錢 衡錢 厲錢] (不需要為0): ').split()))
        
        if len(counts) != 3 or len(requires) != 3:
            raise ValueError
        
    except ValueError:
        print('輸入錯誤，確保格式以及輸入數量')
        return
    
    tot_coins = sum(counts)
    base_probs = [c / tot_coins for c in counts] # 每個錢幣單獨投出的機率
    name_coins = ['花錢', '衡錢', '厲錢']
    

    def get_cumulative_binomial_probs(p, k): # 計算至少擲出k的機率
        if k <= 0:
            return 1.0
        
        if k > n:
            return 0.0
        
        prob_sum = 0
        
        for i in range(k, n + 1):
            prob_sum += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
        return prob_sum
    
    
    results = []
    for i in range(3):
        prob = get_cumulative_binomial_probs(base_probs[i], requires[i])
        results.append((prob, f'{name_coins[i]} ({requires[i]})'))

    print(f'----結果----')
    
    for prob, name_coins in results:
        print(f'{name_coins}: {prob:.2%}')

    print('----結論----')
    max_prob = max(prob for prob, name in results)
    winners = [name for prob, name in results if prob == max_prob]
    
    if max_prob == 0:
        print(f'全部選項機率皆為0%')
    else:
        str = ' '.join(winners)
        print(f'{str} 為機率最高的選項')
        
def multiple_coins_probs():
    try:
        print('---輸入通寶資訊---')
        counts = list(map(int, input('擁有 [花錢 衡錢 厲錢]: ').split()))
        
        if len(counts) != 3:
            raise ValueError
        
        n = int(input('擲出通寶數: '))
        requires = []
        print(f'逐行輸入各組選項需求 [花錢 衡錢 厲錢] (不需要為0且輸入完成按Ctrl + Z): ')
        
        while True:
            try:
                line = input()
                if not line.strip():
                    continue
                r = list(map(int, line.split()))
                
                if len(r) == 3:
                    requires.append(r)
                else:
                    print(f'格式錯誤 確保輸入3個數字')
            except EOFError:
                break
            
        if not requires:
            print(f'未輸入需求 計算結束')
            return
            
        options = len(requires)
            
    except ValueError:
        print('輸入錯誤，確保格式以及輸入數量')
        return
    
    tot_coins = sum(counts)
    base_probs = [c / tot_coins for c in counts] # 每個錢幣單獨投出的機率
    name_coins = ['花錢', '衡錢', '厲錢']
    
    def get_cumulative_multinomial_probs(probs, requires):
        prob_sum = 0
        p1, p2, p3 = probs
        r1, r2, r3 = requires
        for k1 in range(r1, n + 1):
            for k2 in range(r2, n + 1 - k1 - r3):
                k3 = n - k1 - k2
                prob_sum += math.factorial(n) / (math.factorial(k1) * math.factorial(k2) * math.factorial(k3)) * (p1**k1) * (p2**k2) * (p3**k3)
        return prob_sum
    
    results = []
    for i in range(options):
        results.append((get_cumulative_multinomial_probs(base_probs, requires[i]), f'選項{i + 1} ({name_coins[0]}: {requires[i][0]} {name_coins[1]}: {requires[i][1]} {name_coins[2]}: {requires[i][2]})'))
        
    for prob, option in results:
        print(f'{option}: {prob:.2%}')
        
    print('----結論----')
    max_prob = max(prob for prob, option in results)
    winners = [option for prob, option in results if prob == max_prob]
    
    if max_prob == 0:
        print(f'全部選項機率皆為0%')
    else:
        str = ' '.join(winners)
        print(f'{str} 為機率最高的選項')
    

if __name__ == "__main__":
    mode = input('輸入\'s\'為單種錢幣\'m\'為多種錢幣: ')
    
    match mode:
        case 's':
            single_coins_probs()
        case 'm':
            multiple_coins_probs()
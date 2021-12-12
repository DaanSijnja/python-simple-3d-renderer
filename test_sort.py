def sorteer(list):
    gestorteerd = list[:]
    alles_klaar = True
    for i in range(1,len(list)):

        if(gestorteerd[i-1] > gestorteerd[i]):
            a = gestorteerd[i-1]
            gestorteerd[i-1] = gestorteerd[i]
            gestorteerd[i] = a
            alles_klaar = False
    
    if(alles_klaar == False):
        return sorteer(gestorteerd)
    
    return gestorteerd


lijst = [12,32,1,24,21,3,1,23,1,23,43,54,43,234,93]

print(sorteer(lijst))
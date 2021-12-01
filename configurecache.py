import math

global cache, C, B, E, S, s, b, t

def configure_cache():
    print("configure the cache:")
    C = input("cache size: ")
    B = input("data block size: ")
    E = input("associativity: ")
    replacementPolicy = input("replacement policy: ")
    writeHit = input("write hit policy: ")
    writeMiss = input("write miss policy: ")
    print("cache successfully configured!")
    S = int(C/(B*E))
    s = math.log2(S)
    b = math.log2(B)
    t = m-(s+b)
    cache.build_cache(S, E, B)

def build_cache(S, E, B):
    for s in S:
        c.append([])
        for e in E:
            c[s].append([])
            for b in B:
                c[s][e].append([])

    

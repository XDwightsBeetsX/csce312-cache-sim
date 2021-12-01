import math

global cache, C, B, E, S, s, b, t

def configure_cache():
    print("configure the cache:")
    C = int(input("cache size: "))
    B = int(input("data block size: "))
    E = int(input("associativity: "))
    replacementPolicy = int(input("replacement policy: "))
    writeHit = int(input("write hit policy: "))
    writeMiss = int(input("write miss policy: "))
    print("cache successfully configured!")
    S = int(C/(B*E))
    s = math.log2(S)
    b = math.log2(B)
    t = int(m-(s+b))
    cache.build_cache(S, E, B)

def build_cache(S, E, B):
    for s in S:
        c.append([])
        for e in E:
            c[s].append([])
            for b in B:
                c[s][e].append([])

    

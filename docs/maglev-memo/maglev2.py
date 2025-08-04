#!/bin/usr/env python3
import farmhash
import xxhash
from socket import inet_aton
from struct import pack

M = 65537
node_names = ["0", "1", "2"]
N = len(node_names)

def h1(val):
  return farmhash.FarmHash64(str(val))

def h2(val):
  return xxhash.xxh64(str(val)).intdigest()


def gen_permutation():
  Permutaion = []
  for i in range(N):
    offset = h1(str(node_names[i])) % M
    skip = (h2(str(node_names[i])) % (M-1)) +1
    row = []
    for j in range(M):
      row.append((offset + j * skip) % M)
    Permutaion.append(row)
  return Permutaion


def populate(Permutation):
  next_ = [0]  * N
  entry = [-1] * M
  n = 0
  while True:
    for i in range(N):
      c = Permutation[i][next_[i]]
      while entry[c] >= 0:
        next_[i] += 1
        c = Permutation[i][next_[i]]
      entry[c] = i
      next_[i] += 1
      n += 1
      if n == M:
        return entry


def tuple_to_bytes(sip, dip, sport, dport, proto):
  return inet_aton(sip)+inet_aton(dip)+pack('!HHB',sport,dport,proto)


def lookup(Table, flow_identifier):
  idx = xxhash.xxh64(flow_identifier).intdigest() % len(Table)
  return Table[idx]


def main():
  P = gen_permutation()
  T = populate(P)
  print(T)
  print(lookup(T, tuple_to_bytes("10.0.0.1","10.1.0.1",44523,443,6)))
  print(lookup(T, tuple_to_bytes("10.0.0.1","192.1.0.1",44523,80,6)))

if __name__=="__main__":
    main()

# TODO: REFACTOR
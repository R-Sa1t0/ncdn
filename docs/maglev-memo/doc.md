## Google Maglev
 - Look Up Table (LUT)
   - M : LUT要素数。素数である必要がある。普通は65537
   - N : バックエンドの数。
   - i : バックエンドのID (クラスタ内で固有のもの)
   - `offset = h1(name[i]) mod M`
   - `skip   = h2(name[i]) mod (M-1) +1`

これらを求めた後に、
```
permutation[i][j] = (offset + j*skip) mod M
```

M = 4だったら 2と4 は互いに素ではない
M = 7 だったら1~7 は互いに素である


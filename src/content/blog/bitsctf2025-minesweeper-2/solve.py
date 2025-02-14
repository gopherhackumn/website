from itertools import count

from pwn import *
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve


directions = (-1, 0), (0, -1), (0, 1), (1, 0)

p = remote("chals.bitskrieg.in", 7005)

print(p.recvline())  # welcome to Minesweeper 2!
print(p.recvline())  #

try:
    for lvl in range(100):
        # Level 1: 3x4
        print(line := p.recvline())
        r, c = map(int, line.split(b": ")[1].split(b"x"))

        print(p.recvline())  # You have 65536 moves left!
        print(p.recvline())  #
        print(p.recvline())  # Here is your board:

        board = []
        data = []
        rows = []
        cols = []
        for i in range(r):
            print(line := p.recvline())  # 0 13  0  9
            board.extend(map(int, line.split()))
            for j in range(c):
                for dr, dc in directions:
                    nr = i + dr
                    nc = j + dc
                    if 0 <= nr < r and 0 <= nc < c:
                        data.append(1)
                        rows.append(i * c + j)
                        cols.append(nr * c + nc)

        print("Constructing matrices")
        A = csc_matrix((data, (rows, cols)), dtype=int)
        print("Constructed A")
        B = csc_matrix((board, (range(r * c), [0] * (r * c))), dtype=int)
        print("Constructed B")
        x = spsolve(A, B)
        print("Solved", x)

        print("Sending about", sum(board) // 4, "lines")
        cnt = 0
        for i in range(r * c):
            rr, cc = divmod(i, c)
            for _ in range(round(x[i])):
                p.sendline(bytes(f"{rr} {cc}", "utf-8"))
                cnt += 1

            if i % c == 0:
                p.recv(10 ** 9)
                print(cnt)
                time.sleep(0.5)
        print("Sent", cnt, "lines")

        print(p.recvuntil(b"You have cleared the level!\n"))
        print(p.recvline())  #
except Exception as e:
    print("Exception", e)
    print(cnt, "guesses used")
    for i in count():
        print(i, p.recvline())

# Flag: BITSCTF{D0_u_y34rn_f0R_th3_m1n3s?}

# Directory structure (generated by https://tree.nathanfriend.com/?s=(%27options!(%27fancy*~fullPath!false~trailingSlash*~rootDot*)~-(%27-%27challenge.bmp%5Cnfour.wav%5Cnsolve.py%27)~version!%271%27)*!true-source!%01-*):
# .
# ├── challenge.bmp
# ├── four.wav
# └── solve.py

with open("challenge.bmp", "rb") as challenge:
    f1 = challenge.read()

    with open("four.wav", "rb") as four:
        f2 = four.read()

        # Offset of 58 yields most 0's (same bits)
        for offset in range(100):
            s = [c1 ^ c2 for c1, c2 in zip(f1, f2[offset:])]
            print("Offset:", offset, "| 0's:", s.count(0))

        with open("flag.bmp", "wb") as flag:
            offset = 58
            for i in range(offset):
                flag.write(f1[i].to_bytes())
            for i in range(offset, len(f2)):
                flag.write((f1[i - offset] ^ f2[i]).to_bytes())
            for i in range(len(f2), len(f1)):
                flag.write(f1[i].to_bytes())

# Flag: TUCTF{wh0_gl33p3d_up_my_gl0rps}

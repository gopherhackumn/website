+++
title = "GopherHack Meeting 2024-09-25"
date = 2024-09-25
+++

# Last week: format string

Tools to have:

* Access to an x86-64 Linux machine
  * [CSELabs]: click the link and run `ssh <x500>@<machine>`
  * WSL, Virtual machine
* netcat

[CSELabs]: https://cse.umn.edu/cseit/classrooms-labs

We were working on a Format String problem from PicoCTF 2024.

```
nc gopherhack.easyctf.com 5013
```

The interesting part is that it does a `printf(buf)`, which allows you to put whatever string you want.

### One-liners from last week

To download a file, right click and copy paste the URL. Then, run:

```
wget -O <filename> <url>
```

To give yourself permission to run a binary, run:

```
chmod +x <file>
```

# This week's challenge: buffer overflow

Tools to have:

* Access to an x86-64 Linux machine
* Python
* [GDB](https://sourceware.org/gdb/)
* [pwntools](https://pwntools.com)
* [radare2](https://rada.re/n/radare2.html) (optional)
* [Cutter](https://cutter.re) (optional)

Access the challenge at our contest site: https://gopherhack.easyctf.com/

```
nc gopherhack.easyctf.com 5015
```

How can we change the value of `key`?

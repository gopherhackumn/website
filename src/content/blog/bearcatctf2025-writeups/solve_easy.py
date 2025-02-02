import angr                                                                                                                
import claripy                                                                                                             
                                                                                                                           
from angr.procedures.libc import memcpy, memcmp, strlen                                                                    
                                                                                                                           
                                                                                                                           
# Load the binary                                                                                                          
project = angr.Project("easy", auto_load_libs=True, main_opts={'base_addr':0x00}, use_sim_procedures = True)               
                                                                                                                           
stdin_input = claripy.BVS("stdin_input", 8 * 26)  # Symbolic string of 20 bytes                                            
                                                                                                                           
main = project.loader.find_symbol("main")                                                                                  
                                                                                                                           
# project.hook_symbol("strlen", strlen.strlen())                                                                           
# project.hook_symbol("memcpy", memcpy.memcpy())                                                                           
# project.hook_symbol("memcmp", memcmp.memcmp())                                                                           
                                                                                                                           
# Create an initial state, symbolically setting stdin to our symbolic input                                                
# state = project.factory.entry_state(stdin=stdin_input)                                                                   
flag_input = claripy.Concat(stdin_input, claripy.BVV(b"\n", 8))                                                            
                                                                                                                           
state = project.factory.entry_state(                                                                                       
            args=['./easy'],                                                                                               
            add_options={ angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY, angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS },   
            stdin=flag_input                                                                                               
           )                                                                                                               
                                                                                                                           
# Create a simulation manager                                                                                              
simgr = project.factory.simgr(state)                                                                                       
                                                                                                                           
def logg(st):                                                                                                              
    print(", ".join(hex(a.addr) for a in st.active))                                                                       
    pass                                                                                                                   
                                                                                                                           
simgr.run(step_func=logg)                                                                                                  
                                                                                                                           
# Explore the binary                                                                                                       
# simgr.explore(find=0x147b, avoid=0x148c, step_func=logg)                                                                 
                                                                                                                           
print(simgr)                                                                                                               
                                                                                                                           
for st in simgr.deadended:                                                                                                 
    if b"There it is" in st.posix.dumps(1):                                                                                
        print(st.solver.eval(flag_input, cast_to=bytes))                                                                   
    print(st.posix.dumps(1))                                                                                               
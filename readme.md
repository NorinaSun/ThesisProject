Dependencies

- os
- random
- csv
- numpy
- gurobipy

Setup Instructions

- install [gcc](https://gcc.gnu.org/install/download.html)
- install [porta](https://porta.zib.de/) follow instructions in INFO file
  - valid.c, porta.c, and inout.c reference 'cfree' which is not valid. Change them to 'free'.
  - Make sure you do the last path setting step, if it doesn't work try setting the path manually 
  ```
  PATH=/bin:/usr/bin:/usr/local/bin:/Users/...porta-1.4.1/gnu-make/bin:${PATH}
  or if downloading this repo in gnu-make/bin 
  PATH=/bin:/usr/bin:/usr/local/bin:/Users/...porta-1.4.1/gnu-make/bin:/ThesisProject${PATH}
- install gurobi and have a valid [gurobi license](https://www.gurobi.com/academia/academic-program-and-licenses)
  ```
 
 Run Instructions
 
- Execute main.py. Answer the prompts in console.

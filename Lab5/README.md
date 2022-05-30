# Descrierea formatului

## Format
Variables :
     
  variable1
  
  variable2
  
  '''
  
  variablek 
  
End


Terminals :

  terminal1
  
  terminal2
  
  ...
  
  terminalk
  
End


Productions :

variable_i -> variable_i    |    variable_j variable_k
    
 ...
    
End

Variabila de start apare in lista de variabile sub forma "variabila, S" sau "variabila, s".

Consideram epsilon egal cu #. Nu am considerat # ca terminal si nici ca variabila.

In fiecare productie variabilele apar cu spatiu intre ele. De asemenea, trebuie sa existe spatiu si intre variabile si "|".

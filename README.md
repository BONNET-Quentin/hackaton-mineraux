# hackaton-mineraux

# Bijection utilisée entre $[|1,n^3|]$ et $[|1,n|]\times[|1,n|]\times[|1,n|]$ :
$$f_n : [|0,n^3-1|] \to [|0,n-1|]\times[|0,n-1|]\times[|0,n-1|], k \mapsto (k//n^2, (k\%n^2)//n, (k\%n^2)\%n)$$

$$f_n^{-1} (x,y,z) = n^2*x + n*y + z$$
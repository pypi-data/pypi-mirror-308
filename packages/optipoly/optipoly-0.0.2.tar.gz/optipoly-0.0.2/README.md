# optipoly

`optipoly` is a non conventional optimizer dedicated to the optimization
of multi-variate polynomial cost functions on admissible hypercubes. It
leverages the extraordinarily fast computation of scalar polynomials by
the `scipy.interpolation.interp1d` method in oder to derive a robust to
local minima solution of the polynomial optimization problem.

Interested reader can refer to the citation provided 
for a complete description and comparison with some existing solvers.

Here, the main elements are explained briefly for an easy and quick use
of the solver.

## Installation

``` default
pip install optipoly
```

[Full description of the module is available](https://mazenalamir.github.io/optipoly/).

Here a very short presentation is given. 

## The problem addressed

Given a polynomial in several variables of the form:

$$
P(x)=\sum_{i=1}^{n_c}c_i\phi_i(x)\quad \text{where} \quad \phi_i(x):=\prod_{j=1}^n x_j^{p_ij}
$$

Assume that we want to find the minimum value of the polynomial over some hyper box defined by `xmin`and `xmax`, namely

$$
\min_{x} P(x) \quad \text{$\vert\quad x\in [x_\text{min}, x_\text{max}]\subset \mathbb R^n$}
$$

This is the kind of porblem `optipoly` is done for. 

> **Tip**
> 
> Using specific choice of the call inputs, `optipoly`can be used as well to find a maximum or to find a root of the polynomial.
>

[Full description of the module is available](https://mazenalamir.github.io/optipoly/).

## Example of use

Consider the polynomial in three variables defined by:

$$
P(x) = x_1x_3^2+2x_2^3
$$

An instance of the class `Pol` that represent this polynomial can be created via the following script:

```python 
from optipoly import Pol

# Define the matrix of powers and c.
 
powers = [[1, 0, 2], [0,3,0]] 
coefs = [1.0, 2.0]            

# Create an instance of the class.

pol = Pol(powers, coefs)      
```

The following script gives an example of a call that asks for the maximization of the polynomial defined earlier (see @eq-examplePx) then prints the results so obtained:

```python
nx = 3
x0 = np.zeros(nx)
ntrials = 6
ngrid = 1000
xmin = -1*np.ones(nx)
xmax = 2*np.ones(nx)

solution, cpu = pol.solve(x0=x0, 
                          xmin=xmin, 
                          xmax=xmax, 
                          ngrid=ngrid, 
                          Ntrials=ntrials, 
                          psi=lambda v:-v
                          )
                          
print(f'xopt = {solution.x}')
print(f'fopt = {solution.f}')
print(f'computation time = {solution.cpu}')

>> xopt = [-1.  2.  0.]
>> fopt = 16.0
>> computation time = 0.0046999454498291016
```

Changing the argument `psi`to `psi=lambda v:abs(v)` asks the solver to zero the polynomial and hence, leads to the following results:

```python
>> xopt = [-0.996997    0.58858859  0.63963964]
>> fopt = -9.305087356087371e-05
>> computation time = 0.003011941909790039
```

Finally, using the default definition leads to `solve` trying to find a minimum of the polynomial leading to:

```python 
>> xopt = [-1. -1.  2.]
>> fopt = -6.0
>> computation time = 0.005150318145751953
```

[Full description of the module is available](https://mazenalamir.github.io/optipoly/).

## Citing optipoly

``` bibtex
@misc{optipoly2024,
      title={optipoly: A Python package for boxed-constrained multi-variable polynomial cost functions optimization}, 
      author={Mazen Alamir},
      year={2024},
      eprint={5987757},
      archivePrefix={arXiv},
      primaryClass={eess.SY},
      url={https://arxiv.org/submit/5987757}, 
}
```


> **Tip**
>
> The above reference contains some comparison with alternative solver
> that underlines the performance of `optipoly` in terms of the achieved
> cost as well as in terms of the compuation time.

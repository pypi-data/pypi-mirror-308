import dataclasses as _dc
import numbers as _numbers
import types as _types

from ctypes import py_object, c_double, c_uint32, c_longlong
from ._ctypeslib import pydll as _pydll



_pydll.c_optimize_bracket.argtypes = [
					py_object, #function
					c_double, #a
					c_double, #b
					c_double, #growlimit
					c_uint32] #maxiter
_pydll.c_optimize_bracket.restype = py_object 


_pydll.c_optimize_golden.argtypes = [
					py_object, #function
					c_double, #xlow
					c_double, #xhigh
					c_double, #tol
					c_uint32] #maxiter
_pydll.c_optimize_golden.restype = py_object 


_pydll.c_optimize_parabolic.argtypes = [
					py_object, #function
					c_double, #xa
					c_double, #xb
					py_object, #xc
					c_double, #tol
					c_uint32] #maxiter
_pydll.c_optimize_parabolic.restype = py_object 


_pydll.c_optimize_brent.argtypes = [
					py_object, #function
					c_double, #xlow
					c_double, #xhigh
					c_longlong] #maxiter
_pydll.c_optimize_brent.restype = py_object 




#-----------------------------------------------------------


@_dc.dataclass
class BracketResult:
	a:float
	b:float
	c:float
	fa:float
	fb:float
	fc:float


def bracket(
	f:_types.FunctionType, 
	xa:_numbers.Real = 0.0, 
	xb:_numbers.Real = 1.0, 
	grow_limit=110,
	maxiter=1000)->BracketResult:
	"""
	Bracket the minimum of a function.
	Returns three points that bracket the minimum of the function.

	## Inputs:
	f: A unary function
	xa, xb: Initial guesses, local minimum need not be contained within this interval.
	grow_limit: Maximum grow limit.
	maxiter: Maximum number of iterations

	## References:
	- Press WH, Teukolsky SA, Vetterling WT, Flannery BP (2007). 
	  Numerical Recipes The Art of Scientific Computing. Cambridge Uni Press.
	"""
	assert isinstance(f, _types.FunctionType), "f must be function"
	assert isinstance(xa, _numbers.Real), "xa must be real number"
	assert isinstance(xb, _numbers.Real), "xb must be real number"
	assert isinstance(grow_limit, _numbers.Real), "grow_limit must be real number"
	assert isinstance(maxiter, int), "maxiter must be int"

	assert maxiter>0, "maxiter>0 expected"

	d:dict =_pydll.c_optimize_bracket(py_object(f), 
						c_double(xa), 
						c_double(xb),
						c_double(grow_limit),
						c_uint32(maxiter))
	
	return BracketResult(a=d["a"], b=d["b"], c=d["c"], fa=d["fa"], fb=d["fb"], fc=d["fc"])



#-------------------------------------------------------------------

@_dc.dataclass
class GoldenResult:
	xopt:float
	err: float
	iter: int


def golden(
	f:_types.FunctionType, 
	xlow:_numbers.Real, 
	xhigh:_numbers.Real, 
	tol=1E-6,
	maxiter=1000)->GoldenResult:
	"""
	Finds the *local* minimum using golden section method

	## Inputs:
	f: A unary function
	xlow, xhigh: Initial guesses, local minimum need to be contained within this interval.
	tol: tolerance.
	maxiter: Maximum number of iterations

	## References:
	- Chapra SC, Canale RP (2013). Numerical Methods for Engineers, 7th Ed. McGraw Hill Education.
	- Press WH, Teukolsky SA, Vetterling WT, Flannery BP (2007). 
	  Numerical Recipes The Art of Scientific Computing. Cambridge University Press.
	"""
	assert isinstance(f, _types.FunctionType), "f must be function"
	assert isinstance(xlow, _numbers.Real), "xlow must be real number"
	assert isinstance(xhigh, _numbers.Real), "xhigh must be real number"
	assert isinstance(tol, _numbers.Real), "tol must be real number"
	assert isinstance(maxiter, int), "maxiter must be int"

	assert maxiter>0, "maxiter>0 expected"

	xopt, err, iter =_pydll.c_optimize_golden(py_object(f), 
						c_double(xlow), 
						c_double(xhigh),
						c_double(tol),
						c_uint32(maxiter))
	
	return GoldenResult(xopt=xopt, err=err, iter=iter)




#-----------------------------------------------------------------

@_dc.dataclass
class BrentResult:
	xopt:float
	fval: float
	iter: int


def brent(
	f:_types.FunctionType, 
	xlow:_numbers.Real, 
	xhigh:_numbers.Real, 
	maxiter=500)->BrentResult:
	"""
	Finds the minimum using Brent's method

	## Inputs:
	f: A unary function
	xlow, xhigh: Initial guesses, local minimum need to be contained within this interval.
	maxiter: Maximum number of iterations

	## References
	- https://www.boost.org/doc/libs/1_82_0/libs/math/doc/html/math_toolkit/brent_minima.html
	"""
	assert isinstance(f, _types.FunctionType), "f must be function"
	assert isinstance(xlow, _numbers.Real), "xlow must be real number"
	assert isinstance(xhigh, _numbers.Real), "xhigh must be real number"
	assert isinstance(maxiter, int), "maxiter must be int"

	assert maxiter>0, "maxiter>0 expected"

	xopt, fxopt, iter =_pydll.c_optimize_brent(py_object(f), 
						c_double(xlow), 
						c_double(xhigh),
						c_longlong(maxiter))
	
	return BrentResult(xopt=xopt, fval=fxopt, iter=iter)



#----------------------------------------------------------

@_dc.dataclass
class ParabolicResult:
	xopt:float
	err: float
	iter: int


def parabolic(
	f:_types.FunctionType, 
	xa:_numbers.Real, 
	xb:_numbers.Real, 
	xc:None | _numbers.Real = None,
	tol=1E-6,
	maxiter=1000)->ParabolicResult:
	"""
	Finds the minimum using quadratic interpolation algorithm

	## Inputs:
	f: A unary function
	xa, xb, xc: initial guesses
	tol: tolerance.
	maxiter: Maximum number of iterations

	## References: 
	- Chapra SC, Canale RP (2013). Numerical Methods for Engineers, 7th Ed. McGraw Hill Education.
	- Cheney W, Kincaid D (2007). Numerical Mathematics and Computing, 6th Ed. Brooks Cole 
	"""
	assert isinstance(f, _types.FunctionType), "f must be function"
	assert isinstance(xa, _numbers.Real), "xa must be real"
	assert isinstance(xb, _numbers.Real), "xb must be real"
	assert isinstance(xc, _numbers.Real | None), "xc must be None or real"
	assert isinstance(tol, _numbers.Real), "tol must be real"
	assert isinstance(maxiter, int), "maxiter must be int"

	assert maxiter>0, "maxiter>0 expected"

	assert abs(xa-xb)>tol, "xa and xb must be different"
	if isinstance(xc, _numbers.Real):
		assert abs(xc-xb), "xa != xb != xc expected"

	xopt, err, iter =_pydll.c_optimize_parabolic(py_object(f), 
						c_double(xa), 
						c_double(xb),
						py_object(xc),
						c_double(tol),
						c_uint32(maxiter))
	
	return ParabolicResult(xopt=xopt, err=err, iter=iter)

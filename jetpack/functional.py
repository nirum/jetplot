import functools

def id(x): return x
def fst(x): return x[0]
def lst(x): return x[-1]

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

import inspect

def func_bodies_from_module(module):
    flist = inspect.getmembers(module, inspect.isfunction)
    bodies = {f[0]: getfunctionbody(f[1]) for f in flist}
    return bodies

def getfunctionbody(function):
    funclines = inspect.getsourcelines(function)[0]
    body =  "".join(funclines[1:])
    return body

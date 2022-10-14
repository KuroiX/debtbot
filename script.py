from inspect import signature


def func1(param: int):
    return 3


def func2(param2: str):
    return "boi"


test = func1
print(type(signature(test).parameters["param"]))

if "param2" in signature(func2).parameters:
    print("yey")

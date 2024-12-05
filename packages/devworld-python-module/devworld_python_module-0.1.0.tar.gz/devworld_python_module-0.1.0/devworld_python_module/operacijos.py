def suma(a, b):
    """Grazina suma"""
    return a + b

def skirtumas(a, b):
    """Grazina skirtuma"""
    return a - b

def daugyba(a, b):
    """Grazina daugyba"""
    return a * b

def dalyba(a, b):
    """Grazina dalyba, iskeliame errora jeigu daliname is 0"""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

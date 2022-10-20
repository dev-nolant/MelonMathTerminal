__DESCRIPTION__ = """Orbital Darkness Time\n\
Calculates how long the object will be in darkness. this is a positively extreme calculation.\n\
USAGE: calculate [apoapsis] [periapsis] [radius of object] [mass of the body to orbid] [optional: GravitationalParameter"""

from cmath import sqrt
import os
import time
from math import sqrt, asin


start_time = time.time()

"""[General director set]
Sets the working directory to the current directory \
that the __main__ file is being executed from
"""
os.chdir(os.path.dirname(os.path.abspath(__file__)))

defaultG = 6.674e-11


def calculate(Ap: float, Pe: float, R: float, M: float, G=defaultG):
    """_A general overview of the function 'calculate'. Will calculate based on algorithm below._

    Td = (2ab)/h(sin^-1(R/b)+(eR)/b)

    Args:
        Ap (_float_): _apoapsis of the crafts orbit from the surface of the body._
        Pe (_float_): _periapsis of the crafts orbit from the surface of the body._
        R (_float_): _radius of the body to orbit._
        M (_float_): _mass of the body to orbit._
        G (_float_): _defaultG is default Gravitational Parameter, can be overridden._
    """
    # PreRequisit compilation calculations
    Ra = float(Ap) + float(R)
    Rp = float(Pe) + float(R)
    semiMajorAxis = float(Ra+Rp)/2
    semiMinorAxis = sqrt(Ra*Rp)
    eccentricity = (Ra-Rp)/(Ra+Rp)
    semiLatusRectum = ((2 * Ra) * Rp)/Ra+Rp
    gravitationalParameter = float(G) * float(M)
    specificAngularMomentum = sqrt(semiLatusRectum * gravitationalParameter)

    # Algorithm breakdown - modular
    Part1 = ((2*semiMajorAxis) * semiMinorAxis)/specificAngularMomentum
    Part2 = float(R) / float(semiMinorAxis)
    Part3 = (float(eccentricity)*float(R))/semiMinorAxis
    Part4 = asin(Part2)
    Part5 = Part4 + Part3
    Td = (Part1 * Part5)*1000
    time_calculation = round(time.time() - start_time, 2)
    if time_calculation < 100:
        ending = "ms"
    else:
        ending = "secs"
        time_calculation = time_calculation/10
    print(
        f"Calculations finished\n\n---------LOG---------\nTime Taken: {time_calculation}{ending}\n")
    print(
        f"Total time spent in darkness based on parameters:\n\
-------------------------------------------------\n\
{Ap}: apoapsis of the crafts orbit from the surface of the body.\n\
{Pe}: periapsis of the crafts orbit from the surface of the body.\n\
{R}: radius of the body to orbit.\n\
{M}: mass of the body to orbit.\n\
{G}: defaultG is default, can be overridden.\n\
-------------------------------------------------\n\
{round(Td, 4)} total seconds in darkness\n\
----------------------------------------------\n\
Note: These calculations are based on the worst-case scenario meaning that\n\
      the time spent in darkness calculated here will be most-likely longer\n\
      than actually spent. + or - sin^-1")

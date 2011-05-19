#!/usrbin/python
""" Contains examples in list format and a function
to generate a random list.
"""

from random import randint, random
import numpy

BATMAN_LIST = [4.05 + 20.85j,   6.75 + 26.4j ,   6.45 + 18.15j,  9.3   +  9.9j ,
              15.75 +  8.4j ,  22.05 +  9.6j ,  27.9  + 16.35j,  27.45 + 25.35j,
              38.4  + 20.7j ,  47.25 + 14.25j,  53.25 +  6.45j,  55.95 -  2.85j,
              54    - 11.25j,  48.6  - 19.5j ,  42.6  - 24.15j,  35.4  - 27.45j,
              40.95 - 21.15j,  43.65 - 15.45j,  43.5  - 10.35j,  41.85 -  5.7j ,
              39    - 4.5j  ,  35.55 -  4.8j ,  31.95 -  9.45j,  29.1  - 16.2j ,
              29.25 - 10.95j,  28.35 -  7.35j,  25.5  -  5.55j,  21.45 -  5.1j ,
              14.85 - 9.15j ,   8.85 - 14.85j,   4.5  - 21.3j , -33.45j        ,
             - 4.5  - 21.3j , - 8.85 - 14.85j, -14.85 -  9.15j, -21.45 -  5.1j ,
             -25.5  -  5.55j, -28.35 -  7.35j, -29.25 - 10.95j, -29.1  - 16.2j ,
             -31.95 -  9.45j, -35.55 -  4.8j , -39    -  4.5j , -41.85 -  5.7j ,
             -43.5  - 10.35j, -43.65 - 15.45j, -40.95 - 21.15j, -35.4  - 27.45j,
             -42.6  - 24.15j, -48.6  - 19.5j , -54    - 11.25j, -55.95 -  2.85j,
             -53.25 +  6.45j, -47.25 + 14.25j, -38.4  + 20.7j , -27.45 + 25.35j,
             -27.9  + 16.35j, -22.05 +  9.6j , -15.75 +  8.4j , - 9.3  +  9.9j ,
             - 6.45 + 18.15j, - 6.75 + 26.4j , - 4.05 + 20.85j,  20.85j        ]

NIKE_LIST   = [10    + 4.2j ,  3.3 + 2.5j , -2.1 + 1.15j, -4.1 +  .4j,
               -6    +  .9j , -6.6 + 1.6j , -6.1 + 4.15j, -7.3 + 2.1j,
               -8.15 -  0.5j, -7.2 - 2.15j, -4.7 - 1.9j , -2.1 -  .9j,
                3.3  + 1.35j]

MICKEY_LIST = [1   +  9j  , - 3 + 8j  , -4   + 14.5j, -10.5 +16j,
             -15   + 10j  , -11 + 4.5j, -6.5 +  5.3j, - 8   - 3j,
               0.5 - 10j  ,  10 - 3j  ,  9.5 +  5.7j,  15   + 5j,
              16   + 13.5j,  10 + 16j ,  5   +  13j ,   5   + 8j]

PIZZA_LIST  = [-0.71 + 0.71j, -1         , -1j,  1         ,
                0.71 + 0.71j,  0.5 + 0.5j,  0 , -0.5 + 0.5j]
 
SQUARE_LIST = [1,  1 + 1j,  1j, -1 + 1j,
              -1, -1 - 1j, -1j,  1 - 1j]


def random_list():
    """
    Generates and outputs a random list ordered in a counterclockwise
    fashion about the origin.
    """
    N = randint(10, 101)
    lista = [ N * (random() - 0.5 + 1j * (random() - 0.5))
            for k in range(0,N)]
    lista_upper = []
    lista_lower = []
    for point in lista:
        if (numpy.imag(point) > 0):
            lista_upper.append(point)
        else:
            lista_lower.append(point)
    lista_upper.sort(key = lambda x: x.real)
    lista_lower.sort(key = lambda x: -x.real)
    lista = lista_upper + lista_lower
    return lista

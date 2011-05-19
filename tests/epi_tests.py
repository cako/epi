from nose.tools import *
from epi.epi_classes import Figura
from epi.epi_examples import *
from numpy import array

def test_figura():
    fig = Figura(BATMAN_LIST, "Batman")
    assert_equal(fig.title, "Batman")
    assert_equal(array(BATMAN_LIST).all(), fig.lista.all())

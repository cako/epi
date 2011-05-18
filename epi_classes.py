#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" __init__ script containing the Figura and TerminalMain class """

from __future__ import division
import numpy
import sympy
import pylab
import epi_examples

class Figura (object):
    """
    This class represents a figure. a figure is composed of a list that
    represents it's points on the plane, a name. Various methods can be
    called, such as one to plot the list and an orbit around the points,
    calculated using the trigonometric polynomial.
    For more information about the trignonometric polynomial, see:
    http://en.wikipedia.org/wiki/Trigonometric_interpolation_polynomial
    """
    def __init__(self, lista = [], title = ""):
        """ Initialize all of Figura's attributes. They include:
            o lista
            o coefs
            o sampled_f
            o size
            o title
        """
        self.lista = numpy.array(lista)
        self.size = len(lista)
        self.title = title
        self.step = 0.01
        self.coefs = []
        self.sampled_f = []
        if self.size != 0:
            self.coefs = self.get_coefs()
            self.sampled_f = self.get_sampled_f()
    
    def get_coefs(self):
        """
        Calculates the FFT of the lista and returns that.
        The result is stored in Figura.coefs.
        """
        if self.coefs == []:
            self.coefs = numpy.fft.fft(self.lista)
            self.coefs = [coef/self.size for coef in self.coefs] 
        return self.coefs

    def get_lista(self):
        """ Returns the lista. """
        return self.lista

    def put_lista(self, lista):
        """
        Defines Figura.lista according to it's argument,
        and then generates self.coefs and Figura.sampled_f.
        """
        self.lista = numpy.array(lista)
        self.size = len(lista)
        if self.size != 0:
            self.coefs = self.get_coefs()
            self.sampled_f = self.get_sampled_f()

    def put_title(self, title):
        """
        Defines self.title according to it's arguments.
        Prompts before overwriting the previous title.
        """
        if self.title != "":
            print "Do you want to overwrite the title '%s' (y/n)?" % self.title
            if(raw_input("> ") == 'y'):
                self.title = title
        else:
            self.title = title

    def symbol_f(self):
        """
        Generates a sympy object that represents the symbolic version of f,
        the trigonometric polynomial associated with the input points.
        For more information on how f is calculated, see:
        http://en.wikipedia.org/wiki/Trigonometric_interpolation_polynomial
        """
        N = self.size
        coefs = self.coefs
        z = sympy.Symbol("z")

        # k is mapped to the positive and negative powers of exp, respectively.
        # Note that some implementations of the FFT gives the order differently.
        # I had to use examples to figure out how this one worked.
        pos_terms = lambda k: sympy.exp( k * sympy.I * z ) * coefs[k]
        neg_terms = lambda k: sympy.exp( (k-N) * sympy.I * z) * coefs[k]

        # The first part of the function is the summation of the positive powers
        # of exp, and the last part is the summation of the negative powers.
        first = sympy.Add(*map(pos_terms, xrange(0, N//2 + 1)))
        last  = sympy.Add(*map(neg_terms, xrange(N//2 + 1, N)))

        # The function C^2 -> C^2 that graphs the orbit is finally scaled.
        symbol_f = sympy.Add(first, last)/N
        return symbol_f

    def calculate_f(self, z):
        """
        Auxiliary function that calculates f based on the FFT coeficients
        stored in Figura.coefs.
        """ 
        try:
            F = self.coefs[0]
        except IndexError:
            print 'Must first initialize the FFT coefficients with the method get_coefs().'
            print 'This is done automatically if Figura is instantiated with a nonempty first argument.'
            return None
        
        N = self.size
        coefs = self.coefs
        
        for k in xrange(1, N//2+1):
            #print k, coefs[k]
            F += numpy.exp( k * 1j * z ) * coefs[k]
        for k in xrange(N//2+1, N):
            #print k, coefs[k]
            F += numpy.exp( (k-N) * 1j * z) * coefs[k]
        return F

    def get_sampled_f(self):
        """
        Returns the list of f evaluated at a discretized version of the
        interval [0, 2pi].
        """
        samples = numpy.arange(0, 2*numpy.pi + self.step, self.step)
        return self.calculate_f(samples)

    def plot(self):
        """ Plots the orbit and Figura.lista as points. """
        if self.size == 0:
            print 'Warning, empty plot. Define the points with put_lista().' 
        fig = pylab.figure()
        myplots = fig.add_subplot(111, aspect='equal')
        myplots.plot( numpy.real(self.sampled_f), numpy.imag(self.sampled_f),
                        numpy.real(self.lista), numpy.imag(self.lista), 'ro')
        xbounds = myplots.get_xbound()
        ybounds = myplots.get_ybound()
        myplots.axis([xbounds[0], xbounds[1], ybounds[0]*1.1, ybounds[1]*1.5])
        myplots.legend((r'$f(z)$', 'Points'), 'upper center', shadow=True)
        myplots.set_title(self.title)
        pylab.show()

class TerminalMain (object):
    """ Comprises a runtime os the program through the terminal. """
    def __init__ (self):
        """ Initialize the TerminalMain class. """
        pass
    
    def input_from_terminal(self):
        """ Enter list manually. """
        formato = False
        while (formato == False):
            try:
                # Possible security problem. Must curcumvent using input.
                lista = input("> ")
                if type(lista) == type([]):
                    formato = True
                else:
                    print '\nWrong format for list, try again.'
            except:
                print '\nWrong format for list, try again.'
        return lista
    
    def run(self):
        """ Effectively runs the program through the terminal. """
        print """
Choose one of the options:\n
    (1) Enter your own points,\n
or choose one of the examples below:\n
    (2) Batman (64 points);
    (3) Nike (13 points);
    (4) Mickey (16 points);
    (5) Pizza Without a Slice (8 points);
    (6) Square (8 points);
    (7) Random points (number of points between 10 and 100).
Enter any key to exit.
"""
        choice = raw_input("> ")
        if choice == str(1):
            print """
Please input your coordinates in the following format:
[x_1 + y_1j, x_2 + y_2j, ... ,x_n + y_nj]
Where the Cartesian coordinates of the points are (x_i,y_i) for 1≤i≤n.
Note that the imaginary unit 1j, so the coordinate (1,1) would be written 1+1j,
but the coordinate (3,2) would be written 3+2j.\n
"""
            pts = self.input_from_terminal()
            title = raw_input('Figure title: ')
        elif choice == str(2):
            title = 'Batman'
            pts = epi_examples.BATMAN_LIST
        elif choice == str(3):
            title = 'Nike'
            pts = epi_examples.NIKE_LIST
        elif choice == str(4):
            title = 'Mickey'
            pts = epi_examples.MICKEY_LIST
        elif choice == str(5):
            title = 'Pizza without a slice'
            pts = epi_examples.PIZZA_LIST
        elif choice == str(6):
            title = 'Square'
            pts = epi_examples.SQUARE_LIST
        elif choice == str(7):
            title = 'Random'
            pts = epi_examples.random_list()
        else:
            exit(0)

        figura = Figura(pts, title)
        figura.plot()
        print "\nWould you like to display f(z) (y/n)? "
        if(raw_input("> ") == 'y'):
            print figura.symbol_f()
        
        print "\nWould you like calculate another orbit (y/n)?"
        if(raw_input("> ") == 'y'):
            return 0
        else:
            return -1

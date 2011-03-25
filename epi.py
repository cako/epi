#!/usr/bin/python
# -*- coding: UTF-8 -*-

#===============================================================================#
#                                                                               #
#   Copyright 2011 Carlos Alberto da Costa Filho                                #
#                                                                               #
#   This program is free software: you can redistribute it and/or modify        #
#   it under the terms of the GNU General Public License as published by        #
#   the Free Software Foundation, either version 3 of the License, or           #
#   (at your option) any later version.                                         #
#                                                                               #
#   This program is distributed in the hope that it will be useful,             #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#   GNU General Public License for more details.                                #
#                                                                               #
#   You should have received a copy of the GNU General Public License           #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                               #
#===============================================================================#
#                                                                               #
#         FILE:  epi.py                                                         #
#                                                                               #
#        USAGE:  ./epi.py                                                       #
#                python epi.py                                                  #
#                                                                               #
#  DESCRIPTION:  This is a little script I wrote when I was first learning      #
#                about Fourier series and transforms.                           #
#                                                                               #
#                It's purpose is to use the DFT in order to generate a curve    #
#                interpolates it's points in a smooth way.                      #
#                The user can enter the points to be interpolated manually or   #
#                choose from a list of examples. The program then calculates    #
#                the trigonometric polynomial using the values obtained from    #
#                the DFT. Finally, by plotting a parametric curve given by the  #
#                real and the imaginary parts of the polynomial, we can graph   #
#                the curve in 2D.                                               #
#                                                                               #
#                More information on the trigonometric interpolation polynomial #
#                can be found here:                                             #
#                http://en.wikipedia.org/wiki/Discrete_Fourier_transform#Trigonometric_interpolation_polynomial
#                                                                               #
#      OPTIONS:  None that I'm aware of!                                        #
#                                                                               #
# REQUIREMENTS:  python 2.6, numpy, sympy, matplotlib                           #
#         BUGS:  * When entering the list <C-c> does not quit the program       #
#                * Plot window not properly fit (might use matplotlib)          #
#        NOTES:  ---                                                            #
#       AUTHOR:  Carlos Alberto da Costa Filho, c.dacostaf (gmail)              #
#      VERSION:  0.1                                                            #
#      CREATED:  Thu Mar 24 22:12:07 BRT 2011                                   #
#     REVISION:  ---                                                            #
#===============================================================================#

from __future__ import division
from cmath import *
import numpy
from sympy import *
import matplotlib.pylab as plt

# Predefined examples
batman = [4.05+20.85j, 6.75+26.4j, 6.45+18.15j, 9.3+9.9j, 15.75+8.4j, 22.05+9.6j, 27.9+16.35j, 27.45+25.35j, 38.4+20.7j, 47.25+14.25j, 53.25+6.45j, 55.95-2.85j, 54-11.25j, 48.6-19.5j, 42.6-24.15j, 35.4-27.45j, 40.95-21.15j, 43.65-15.45j, 43.5-10.35j, 41.85-5.7j, 39-4.5j, 35.55-4.8j, 31.95-9.45j, 29.1-16.2j, 29.25-10.95j, 28.35-7.35j, 25.5-5.55j, 21.45-5.1j, 14.85-9.15j, 8.85-14.85j, 4.5-21.3j, -33.45j, -4.5-21.3j, -8.85-14.85j, -14.85-9.15j, -21.45-5.1j, -25.5-5.55j, -28.35-7.35j, -29.25-10.95j, -29.1-16.2j, -31.95-9.45j, -35.55-4.8j, -39-4.5j, -41.85-5.7j, -43.5-10.35j, -43.65-15.45j, -40.95-21.15j, -35.4-27.45j, -42.6-24.15j, -48.6-19.5j, -54-11.25j, -55.95-2.85j, -53.25+6.45j, -47.25+14.25j, -38.4+20.7j, -27.45+25.35j, -27.9+16.35j, -22.05+9.6j, -15.75+8.4j, -9.3+9.9j, -6.45+18.15j, -6.75+26.4j, -4.05+20.85j, 20.85j]
nike   = [10+4.2j,3.3+2.5j,-2.1+1.15j,-4.1+.4j,-6+.9j,-6.6+1.6j,-6.1+4.15j,-7.3+2.1j,-8.15-0.5j,-7.2-2.15j,-4.7-1.9j,-2.1-.9j,3.3+1.35j]
mickey = [1+9j,-3+8j,-4+14.5j,-10.5+16j,-15+10j,-11+4.5j,-6.5+5.3j,-8-3j,0.5-10j,10-3j,9.5+5.7j,15+5j,16+13.5j,10+16j,5+13j,5+8j]
pizza  = [-0.71+0.71j,-1,-1j,1,0.71+0.71j,0.5+0.5j,0,-0.5+0.5j] 

def enterlist():
    format = False
    while (format == False):
        try:
            lista = input()
            if type(lista) == type([]):
                format = True
            else:
                print '\nWrong format for list, try again.'
        except:
            print '\nWrong format for list, try again.'
    return lista

def plot(f,N,title): 
    z = Symbol("z")
    step = 0.05 #3.14/(20*log(N))
    sampl_f = map(lambda k: f.subs(z,k),numpy.arange(0,2*numpy.pi+step,step))
    plotpts = len(sampl_f)
    sampl_x = map(lambda k: re(sampl_f[k].expand(complex=True)),range(0,plotpts))
    sampl_y = map(lambda k: im(sampl_f[k].expand(complex=True)),range(0,plotpts))
    plt.title(title)
    plt.plot(sampl_x,sampl_y)
    print "Gerando imagem"
    plt.show()
    

def main():  
    print 'Choose one of the options:'
    print '\n    (1) Enter your own points,'
    print '\nor choose one of the examples below:'
    print '\n    (2) Batman (64 points);'
    print '    (3) Nike (13 points);'
    print '    (4) Mickey (16 points);'
    print '    (5) Pizza Without a Slice (8 points).'
    print '\nEnter any key to exit.'
    choice = raw_input()
    if choice == str(1):
        print '\nPlease input your coordinates in the following format:'
        print '     [x_1 + y_1j, x_2 + y_2j, ... ,x_n + y_nj]'
        print ' Where the Cartesian coordinates of the points are (x_i,y_i) for 1≤i≤n.'
        print ' Note that the imaginary unit 1j, so the coordinate (1,1) would be written 1+1j,'
        print ' but the coordinate (3,2) would be written 3+2j.'
        print '\nStandard mathematical notation follows that of the library cmath.'
        print ' Visit http://docs.python.org/library/cmath.htm for more information.'
        print ' Note that this feature is still experimental and may not work properly.\n'
        pts = enterlist()
        title = raw_input('Figure title: ')
    elif choice == str(2):
        title = 'Batman'
        pts = batman
    elif choice== str(3):
        title = 'Nike'
        pts = nike
    elif choice == str(4):
        title = 'Mickey'
        pts = mickey
    elif choice == str(5):
        title = 'Pizza without a slice'
        pts = pizza
    else:
        return 1
    N = len(pts)
    coefs = numpy.fft.fft(numpy.array(pts))
    z = Symbol("z")

    # The k is mapped to the positive and negative powers of exp, respectively.
    # Note that some implementations of the fft gives the order differently. I had to use examples to figure out how this one worked.
    pos_terms = lambda k: exp(k*I*z)*coefs[k]
    neg_terms = lambda k: exp((k-N)*I*z)*coefs[k]

    # The first part of the function is the summation of the positive powers of exp, and the last part is the summation of the negative powers.
    first = Add(*map(pos_terms, range(0,N//2 + 1)))
    last  = Add(*map(neg_terms, range(N//2 + 1,N)))
    #print first
    #print last
    #print ''

    # The function C^2 -> C^2 that graphs the orbit is finally scaled.
    f = Function("f")
    f = Add(first, last)/N
    #print f
    
    # Plot
    plot(f,N,title)


main()

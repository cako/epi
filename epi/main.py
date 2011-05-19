#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Main. Runs a terminal version of the program. """

import sys, os, random
from epi_classes import *

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    gui = True
except ImportError:
    gui = False

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Epi')

        self.create_menu()
        self.create_main_frame()
        #self.create_status_bar()

        #self.Figura = Figura(input_from_file('test'), 'test')
        self.Figura = Figura(epi_examples.BATMAN_LIST, 'Batman')
        #self.textbox.setText('1 2 3 4')
        self.on_draw()

    def open_file(self):
        file_choices = ""
        self.file_dialog = QFileDialog()
        filename = self.file_dialog.getOpenFileName(self,'Open file', '', file_choices)
        self.Figura = Figura(input_from_file(filename), "Test")
        self.connect(self.file_dialog, SIGNAL("fileSelected(QString)"), self.on_draw)

        #filename = unicode(QFileDialog.getOpenFileName(self, 
                        #'Open file', '', 
                        #file_choices))
        #self.connect(QFileDialog, SIGNAL("currentChanged(QString)"), self.on_draw)
        self.on_draw()

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"

        path = unicode(QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def on_about(self):
        msg = """ A demo of using PyQt with matplotlib:

         * Use the matplotlib navigation bar
         * Add values to the text box and press Enter (or click "Draw")
         * Show or hide the grid
         * Drag the slider to modify the width of the bars
         * Save the plot to a file using the File menu
         * Click on a bar to receive an informative message
        """
        QMessageBox.about(self, "About the demo", msg.strip())

    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points

        QMessageBox.information(self, "Click!", msg)

    def on_draw(self):
        """ Redraws the figure
        """
        #str = unicode(self.textbox.text())
        #self.data = map(int, str.split())

        #x = range(len(self.data))

        # clear the axes and redraw the plot anew
        #

        #if (self.slider.value() == 20):
            #self.Figura = Figura(input_from_file('test'), 'test')
        #elif (self.slider.value() == 1):
            #self.Figura = Figura(epi_examples.BATMAN_LIST, 'Batman')

        self.fig_plot.clear()
        self.fig_plot.grid(self.grid_cb.isChecked())

        #self.fig_plot.bar(
            #left=x, 
            #height=self.data, 
            #width=self.slider.value() / 100.0,
            #align='center', 
            #alpha=0.44,
            #picker=5)

        self.fig_plot.plot( numpy.real(self.Figura.sampled_f),
                            numpy.imag(self.Figura.sampled_f),
                            numpy.real(self.Figura.lista),
                            numpy.imag(self.Figura.lista), 
                            'ro')

        xbounds = self.fig_plot.get_xbound()
        ybounds = self.fig_plot.get_ybound()

        self.fig_plot.axis([xbounds[0], xbounds[1], ybounds[0]*1.1, ybounds[1]*1.5])
        self.fig_plot.legend((r'$f(z)$', 'Points'), 'upper center', shadow=True)
        self.fig_plot.set_title(self.Figura.title)
        self.canvas.draw()

    def create_main_frame(self):
        self.main_frame = QWidget()

        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        #self.fig_plot = self.fig.add_subplot(111)
        self.fig_plot = self.fig.add_subplot(111, aspect='equal')

        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.on_pick)

        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        # 
        #self.textbox = QLineEdit()
        #self.textbox.setMinimumWidth(200)
        #self.connect(self.textbox, SIGNAL('editingFinished ()'), self.on_draw)

        #self.draw_button = QPushButton("&Draw")
        #self.connect(self.draw_button, SIGNAL('clicked()'), self.on_draw)

        self.grid_cb = QCheckBox("Show &Grid")
        self.grid_cb.setChecked(False)
        self.connect(self.grid_cb, SIGNAL('stateChanged(int)'), self.on_draw)

        #slider_label = QLabel('Bar width (%):')
        #self.slider = QSlider(Qt.Horizontal)
        #self.slider.setRange(1, 100)
        #self.slider.setValue(20)
        #self.slider.setTracking(True)
        #self.slider.setTickPosition(QSlider.TicksBothSides)
        #self.connect(self.slider, SIGNAL('valueChanged(int)'), self.on_draw)

        #
        # Layout with box sizers
        # 
        hbox = QHBoxLayout()

        #for w in [  self.textbox, self.draw_button, self.grid_cb,
                    #slider_label, self.slider]:
            #hbox.addWidget(w)
            #hbox.setAlignment(w, Qt.AlignVCenter)

        hbox.addWidget(self.grid_cb)
        hbox.setAlignment(self.grid_cb, Qt.AlignVCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        vbox.addLayout(hbox)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    #def create_status_bar(self):
        #self.status_text = QLabel("This is a demo")
        #self.statusBar().addWidget(self.status_text, 1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot, 
            tip="Save the plot")

        open_file_action = self.create_action("&Open file",
            shortcut="Ctrl+O", slot = self.open_file,
            tip="Open a data file")

        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
            (open_file_action, load_file_action, None, quit_action))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
            shortcut='F1', slot=self.on_about,
            tip='About the demo')

        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

app = QApplication(sys.argv)
form = AppForm()
form.show()
app.exec_()

Figura

#try:
    #if (sys.argv[1] == '-t'):
        #gui = False
#except IndexError:
    #gui = False

#if (not gui):
    #run = 0
    #TMain = TerminalMain()
    #while (run == 0):
        #run = TMain.run()
#else:
    #print 'No GUI yet!'
    #app = QApplication(sys.argv)
    #form = AppForm()
    #form.show()
    #app.exec_()

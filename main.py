#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__   = 'GPL v3'
__copyright__ = '2019, soychicka'
__docformat__ = 'restructuredtext en'

if False:
    # This is here to keep my python error checker from complaining about
    # the builtin functions that will be defined by the plugin loading system
    # You do not need this code in your plugins
    get_icons = get_resources = None


import re
from PyQt5.Qt import (QAction, QInputDialog, QDialog, QVBoxLayout, QPushButton, QMessageBox, QLabel, QLineEdit, QComboBox,  QCompleter,  QMainWindow,  QWidget,  QTextEdit)
											
from css_parser.css import CSSRule

from calibre_plugins.spotlight_libre.config import prefs

from subprocess import Popen, PIPE, STDOUT
import re

class AboutWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.create_main_frame()       

    def create_main_frame(self):        
        page = QWidget()        

        self.button = QPushButton('OK', page)
        self.textWindow = QTextEdit()

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.textWindow)
        vbox1.addWidget(self.button)
        page.setLayout(vbox1)
        self.setCentralWidget(page)

        self.button.clicked.connect(self.clicked)

    def clicked(self):
        self.close()

class SpotlightLibreDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        # The current database shown in the GUI > class LibraryDatabase2 
        self.db = gui.current_db

        self.l = QVBoxLayout()
        self.setLayout(self.l)
        


        # Label
        self.labelText = QLabel('Use "and" and "or" for the search.')
        self.l.addWidget(self.labelText)

        # Title
        self.setWindowTitle('SpotlightLibre Full Text Search')
        self.setWindowIcon(icon)

        # Search window
        self.searchTextWindow = QComboBox()
        self.searchTextWindow.setEditable(True)
        self.l.addWidget(self.searchTextWindow)
        self.searchTextWindow.setFocus()
        self.searchTextWindow.setInsertPolicy(QComboBox.NoInsert)
        self.searchTextWindow.setDuplicatesEnabled(False)
        
        #Completer for the seach window
        self.completer = QCompleter()
        self.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
        self.searchTextWindow.setCompleter(self.completer)
        
        # output window
        self.outputWindow = QLabel()
        self.l.addWidget(self.outputWindow)
        
        # search button 1
        self.doSearchButton = QPushButton('Search and replace the filter', self)
        self.doSearchButton.clicked.connect(self.spotlightSearchNew)
        self.l.addWidget(self.doSearchButton)
        self.doSearchButton.setDefault(True)
                
        # search button 2
        self.doSearchButton = QPushButton('Search and add to filter', self)
        self.doSearchButton.clicked.connect(self.spotlightSearchAdd)
        self.l.addWidget(self.doSearchButton)
    

        # about button
        self.aboutButton = QPushButton('About', self)
        self.aboutButton.clicked.connect(self.about)
        self.l.addWidget(self.aboutButton)

        self.resize(self.sizeHint())
        #self.resize(500, self.height())
        

    def about(self):
        # Get the about text from a file inside the plugin zip file
        # The get_resources function is a builtin function defined for all your
        # plugin code. It loads files from the plugin zip file. It returns
        # the bytes from the specified file.
        
        text = get_resources('about.txt')
        #box = QMessageBox()
        #box.about(self, 'About the SpotlightLibre Full Text Search \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t',text.decode('utf-8'))
        #self.resize(600, self.height())
        
        self.box = AboutWindow()
        self.box.setWindowTitle("About the SpotlightLibre Full Text Search Plugin")
        self.box.textWindow.setText(text)
        self.box.textWindow.setReadOnly(True)
        self.box.resize(600, 500)
        self.box.show()
        



    def spotlightSearchNew(self):
        self.searchAdd = False
        self.spotlightSearch()
    
    def spotlightSearchAdd(self):
        self.searchAdd = True
        self.spotlightSearch()

    def spotlightSearch(self):
        self.searchText = str(self.searchTextWindow.currentText())# search text from the plugin gui
        self.searchTextWindow.insertItem(0, self.searchText)
        # self.cmd = 'mdfind -onlyin '+ prefs['pathToLibrary']+' '  # saved to allow for checkbox option later?

        print(self.db.library_path)
        self.cmd = 'mdfind -onlyin "'+self.db.library_path+'" '
								
        self.cmdString = self.cmd + '"'+self.searchText+'"'

        print(self.cmdString)

        self.p = Popen(self.cmdString,  shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.output = self.p.stdout.read()# output from the spotlight search
				
        print(self.output)
        self.found = ''
        self.found = re.findall(r" \((\d+)\)\/", self.output)# regex to find the calibre ids in the folder names
        
        
        self.wholeString = ''
        if len(self.found) == 0 :
            self.outputWindow.setText('no books found' + ' for ' + self.searchText)
        else :
            self.wholeString = '#cid:'
            for elem in self.found:
                self.wholeString += '=' + elem + ' or '
            self.wholeString = self.wholeString[:-4]
            self.outputWindow.setText(str(len(self.found)) + ' books found' + ' for ' + self.searchText)
        
        if self.searchAdd == True :
            self.oldFilter = self.gui.search.text()
            self.wholeString = self.oldFilter + ' and (' + self.wholeString + ')'
        
        self.searchTextWindow.clearEditText()
        self.gui.search.setEditText(self.wholeString) # set calibre search to the string found by spotlight
        self.gui.search.do_search()

    def config(self):
        self.do_user_config(parent=self)


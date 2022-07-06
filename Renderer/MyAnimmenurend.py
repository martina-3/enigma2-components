# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/MyAnimmenurend.py
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Components.Renderer.Renderer import Renderer
from Tools.Directories import fileExists
from Components.config import config
from enigma import ePixmap, eTimer, ePicLoad
import os


class MyAnimmenurend(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.path = '/usr/share/enigma2/HDLine/menu/'
        self.picon = ePicLoad()
        self.pixdelay = int(config.plugins.MyAnimmenu.animmenutime.value)
        self.pathanimicon = ''
        self.timermoveamenu = eTimer()
        self.controlTimer = eTimer()
        self.timermoveamenu.callback.append(self.timerEventnew)
        self.controlTimer.timeout.get().append(self.changed)

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what = None):
        if self.controlTimer.isActive():
            self.controlTimer.stop()
        name = ''
        if self.instance:
            name = self.path + self.source.text + '.png'
            if fileExists(name):
                if config.plugins.MyAnimmenu.animmenu.value:
                    self.pathanimicon = name
                    self.runanim()
                else:
                    self.instance.setPixmapFromFile(name)
            else:
                if config.plugins.MyAnimmenu.animmenu.value:
                    self.pathanimicon = '/usr/lib/enigma2/python/Plugins/Extensions/MyAnimmenu/noicon.png'
                    self.runanim()
                else:
                    self.instance.setPixmapFromFile('/usr/lib/enigma2/python/Plugins/Extensions/MyAnimmenu/noicon.png')
                if config.plugins.MyAnimmenu.animmenulog.value:
                    if len(self.source.text) > 1:
                        searchString = '%s.png' % self.source.text
                        log = '/tmp/MyAnimmenu'
                        if not fileExists(log):
                            f1 = open(log, 'w')
                            f1.write(searchString + '\n')
                            f1.close()
                        if fileExists(log):
                            f = open(log, 'r')
                            for line in f.readlines():
                                parts = line.strip()
                                if searchString not in parts:
                                    controlname = True
                                else:
                                    controlname = False

                            f.close()
                            if controlname == True:
                                out = open(log, 'a')
                                out.write(searchString + '\n')
                                out.close()
        else:
            self.controlTimer.start(50)

    def runanim(self):
        self.orgposmenu = 0
        self.sizemenu = self.instance.size()
        self.crocmenu = int(self.sizemenu.width()) / int(config.plugins.MyAnimmenu.animmenuspid.value)
        self.timermoveamenu.start(self.pixdelay, True)

    def timerEventnew(self):
        if self.orgposmenu < self.sizemenu.width():
            self.timermoveamenu.stop()
            self.orgposmenu += self.crocmenu
            self.picon.setPara((int(self.orgposmenu),
             int(self.sizemenu.height()),
             1,
             1,
             False,
             1,
             '#00000000'))
            self.picon.startDecode(self.pathanimicon, 0, 0, False)
            self.png = self.picon.getData()
            self.instance.setPixmap(self.png)
            self.timermoveamenu.start(self.pixdelay, True)
        else:
            self.timermoveamenu.stop()
            self.picon.setPara((int(self.sizemenu.width()),
             int(self.sizemenu.height()),
             1,
             1,
             False,
             1,
             '#00000000'))
            self.picon.startDecode(self.pathanimicon, 0, 0, False)
            self.png = self.picon.getData()
            self.instance.setPixmap(self.png)
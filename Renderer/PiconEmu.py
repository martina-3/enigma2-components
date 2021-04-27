# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/PiconEmu.py
from Renderer import Renderer
from enigma import ePixmap, ePicLoad, iServiceInformation
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.Converter.Poll import Poll

class PiconEmu(Renderer, Poll):

    def __init__(self):
        Poll.__init__(self)
        Renderer.__init__(self)
        self.nameCache = {}
        self.pngname = ''
        self.path = 'piconCam'

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

    def changed(self, what):
        self.poll_interval = 1000
        self.poll_enabled = True
        self.control = 0
        if self.instance:
            pngname = ''
            if what[0] != self.CHANGED_CLEAR:
                service = self.source.service
                if service:
                    info = service and service.info()
                    if info:
                        caids = info.getInfoObject(iServiceInformation.sCAIDs)
                        cfgfile = '/tmp/ecm.info'
                        text = 'Unknown'
                        if caids:
                            if fileExists(cfgfile):
                                text = self.findEmu(cfgfile)
                            else:
                                text = 'Unknown'
                        else:
                            text = 'Fta'
                    pngname = self.nameCache.get(text, '')
                    if pngname == '':
                        pngname = self.findPicon(text)
                        if pngname != '':
                            self.nameCache[text] = pngname
                if pngname == '':
                    pngname = self.nameCache.get('default', '')
                    if pngname == '':
                        pngname = self.findEmu('picon_default')
                        if pngname == '':
                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                            if fileExists(tmp):
                                pngname = tmp
                            else:
                                pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                        self.nameCache['default'] = pngname
                if self.pngname != pngname:
                    self.pngname = pngname
                    self.instance.setScale(1)
                    self.instance.setPixmapFromFile(pngname)

    def findEmu(self, cfgfile):
        emu = 'Unknown'
        if cfgfile:
            try:
                f = open(cfgfile, 'r')
                content = f.read()
                f.close()
            except:
                content = ''

            contentInfo = content.split('\n')
            for line in contentInfo:
                if '=====' in line:
                    self.control = 1
                if 'using' in line:
                    emu = 'CCCAM'
                elif 'source' in line and 'system:' not in line:
                    emu = 'MGCAMD'
                elif 'reader' in line or 'system:' in line:
                    if fileExists('/tmp/.ncam/ncam.version'):
                        emu = 'NCAM'
                    else:
                        emu = 'OSCAM'
                if 'reader' in line or 'system:' in line:
                    if fileExists('/tmp/.gcam/gcam.version'):
                        emu = 'GCAM'
                elif 'decode' in line:
                    emu = 'WICARDD'
                elif 'CAID' in line:
                    emu = 'CAMD3'

        return emu

    def findPicon(self, serviceName):
        if serviceName:
            pngname = self.path + serviceName + '.png'
            if fileExists(pngname):
                return pngname
        return ''
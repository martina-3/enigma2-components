# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Animmenuconv.py
from Components.Converter.Converter import Converter
from Components.Element import cached

class MyAnimmenuconv(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)

    def selChanged(self):
        self.downstream_elements.changed((self.CHANGED_ALL, 0))

    @cached
    def getText(self):
        cur = self.source.current
        if cur and len(cur) > 2:
            EntryID = cur[2]
            return EntryID
        return ''

    text = property(getText)

    def changed(self, what):
        if what[0] == self.CHANGED_DEFAULT:
            self.source.onSelectionChanged.append(self.selChanged)
        Converter.changed(self, what)
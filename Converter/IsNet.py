# IsNet Converter
# Copyright (c) 2boom 2014-22
# v.0.2-r2
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#Host:	8.8.8.8/8.8.4.4 (Google DNS)
#		9.9.9.9/149.112.112.112 (Quad9 DNS)
#		1.1.1.1/1.0.0.1 (Cloudflare DNS)
#OpenPort: 53/tcp
#Service: domain (DNS/TCP)
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.Poll import Poll
from Tools.Directories import fileExists
import socket

class IsNet(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if len(type.split(':')) >= 3:
			self.host = type.split(':')[0].strip()
			self.port = int(type.split(':')[1].strip())
			self.timeout = int(type.split(':')[-1].strip())
		else:
			self.host = '8.8.8.8'
			self.port = 53
			self.timeout = 1		
		if self.timeout > 3:
			self.timeout = 3
		self.poll_interval = 3000
		self.poll_enabled = True

	@cached
	def getBoolean(self):
		if self.ifUP():
			try:
				socket.setdefaulttimeout(1)
				socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
				return True
			except socket.error as ex:
				print(ex)
				return False
		return False
			
	boolean = property(getBoolean)
	
	def ifUP(self):
		devname = []
		devtype = ['et', 'wl', 'ra', 'pp']
		if fileExists('/proc/net/dev'):
			for line in open('/proc/net/dev'):
				for i in range(len(devtype)):
					if line.strip().startswith(devtype[i]):
						devname.append(line.split(':')[0].strip())
			for i in range(len(devname)):
				if fileExists('/sys/class/net/%s/operstate' % devname[i]):
					if 'up' in open('/sys/class/net/%s/operstate' % devname[i]).read():
						return True
		return False
	
	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)

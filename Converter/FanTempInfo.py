# FanTempInfo Converter
# Copyright (c) 2boom 2012-22
# v.0.6-r3
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
#
# 10.12.2018 code optimization mod by Sirius
# 05.01.2019 fix error AX HD 51 mod by Sirius
# 27.05.2022 py3 fix

from Components.Converter.Poll import Poll
from Components.Converter.Converter import Converter
from Components.Element import cached
import os

class FanTempInfo(Poll, Converter, object):
	FanInfo = 0
	TempInfo = 1
	TxtFanInfo = 2
	TxtTempInfo = 3

	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "FanInfo":
			self.type = self.FanInfo
		elif type == "TempInfo":
			self.type = self.TempInfo
		elif type == "TxtFanInfo":
			self.type = self.TxtFanInfo
		elif type == "TxtTempInfo":
			self.type = self.TxtTempInfo
		self.poll_interval = 5000
		self.poll_enabled = True

	@cached
	def getText(self):
		info = "N/A"
		if self.type == self.FanInfo or self.type == self.TxtFanInfo:
			try:
				if os.path.exists("/proc/stb/fp/fan_speed"):
					info = open("/proc/stb/fp/fan_speed").read().strip('\n')
				elif os.path.exists("/proc/stb/fp/fan_pwm"):
					info = open("/proc/stb/fp/fan_pwm").read().strip('\n')
			except:
				info = "N/A"
			if self.type == self.TxtFanInfo:
				info = "Fan: " + info
		elif self.type == self.TempInfo or self.type == self.TxtTempInfo:
			try:
				if os.path.exists("/proc/stb/sensors/temp0/value") and os.path.exists("/proc/stb/sensors/temp0/unit"):
					info = "%s%s%s" % (open("/proc/stb/sensors/temp0/value").read().strip('\n'), chr(176), open("/proc/stb/sensors/temp0/unit").read().strip('\n'))
				elif os.path.exists("/proc/stb/fp/temp_sensor_avs"):
					info = "%s%sC" % (open("/proc/stb/fp/temp_sensor_avs").read().strip('\n'), chr(176))
				elif os.path.exists("/proc/stb/fp/temp_sensor"):
					info = "%s%sC" % (open("/proc/stb/fp/temp_sensor").read().strip('\n'), chr(176))
				elif os.path.exists("/sys/devices/virtual/thermal/thermal_zone0/temp"):
					info = "%s%sC" % (open("/sys/devices/virtual/thermal/thermal_zone0/temp").read()[:2].strip('\n'), chr(176))
				elif os.path.exists('/proc/stb/power/avs'):
					info = "%s%sC" % (open("/proc/stb/power/avs").readline().replace('\n', ''), chr(176))
				elif os.path.exists("/proc/hisi/msp/pm_cpu"):
					#info = re.search('temperature = (\d+) degree', open("/proc/hisi/msp/pm_cpu").read()).group(1)
					info = "%s%sC" % (open("/proc/stb/power/avs").readline().replace('\n', ''), chr(176))
			except:
				pass
			if info.startswith('0'):
				info = "N/A"
			if self.type == self.TxtTempInfo:
				info = "Temp: " + info
		return info

	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
		elif not what[0] == self.CHANGED_SPECIFIC:
			Converter.changed(self, what)

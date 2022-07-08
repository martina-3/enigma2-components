# ServiceInfoEX
# Copyright (c) 2boom 2013-22
# v.1.5.6
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
# 26.11.2018 add terrestrial and cable type mod by Sirius
# 01.12.2018 fix video codec mod by Sirius
# 25.12.2018 add support for gamma values mod by Sirius
# 02.01.2022 fix vsize output in format string - 2boom
# 14.01.2022 fix fps data, fix combotype output (vsize & avtype), bit recode - 2boom
# 23.05.2022 pli 8.2 fix - 2boom
# 01.06.2022 add nongamma (NGM), bool sGamma add - 2boom
# 28.06.22 - py3 fps fix

from Components.Converter.Poll import Poll
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.config import config
from Components.Element import cached
from Tools.Directories import fileExists
from Screens.InfoBarGenerics import hasActiveSubservicesForCurrentChannel

if fileExists("/etc/issue"):
	image = ''
	for text in open("/etc/issue"):
		image += text
		if not 'open' in image:
			codec_data = {-1: ' ', 0: 'MPEG2', 1: 'MPEG4', 2: 'MPEG1', 3: 'MPEG4-II', 4: 'VC1', 5: 'VC1-SM', 6: 'HEVC', 7: ' '}
		else:
			codec_data = {-1: ' ', 0: 'MPEG2', 1: 'AVC', 2: 'H263', 3: 'VC1', 4: 'MPEG4-VC', 5: 'VC1-SM', 6: 'MPEG1', 7: 'HEVC', 8: 'VP8', 9: 'VP9', 10: 'XVID', 11: 'N/A 11', 12: 'N/A 12', 13: 'DIVX 3', 14: 'DIVX 4', 15: 'DIVX 5', 16: 'AVS', 17: 'N/A 17', 18: 'VP6', 19: 'N/A 19', 20: 'N/A 20', 21: 'SPARK'}

WIDESCREEN = [3, 4, 7, 8, 0xB, 0xC, 0xF, 0x10]

class ServiceInfoEX(Poll, Converter, object):
	apid = 0
	vpid = 1
	sid = 2
	onid = 3
	tsid = 4
	prcpid = 5
	pmtpid = 6
	txtpid = 7
	caids = 8
	xres = 9
	yres = 10
	gamma = 11
	atype = 12
	vtype = 13
	avtype = 14
	fps = 15
	tbps = 16
	vsize = 17
	ttype = 18
	format = 19
	XRES = 20
	YRES = 21
	IS_WIDESCREEN = 22
	HAS_TELETEXT = 23
	IS_MULTICHANNEL = 24
	IS_CRYPTED = 25
	SUBSERVICES_AVAILABLE = 26
	AUDIOTRACKS_AVAILABLE = 27
	SUBTITLES_AVAILABLE = 28
	EDITMODE = 29
	FRAMERATE = 30
	IS_FTA = 31
	HAS_HBBTV = 32
	IS_SATELLITE = 33
	IS_CABLE = 34
	IS_TERRESTRIAL = 35
	IS_STREAMTV = 36
	IS_SATELLITE_S = 37
	IS_SATELLITE_S2 = 38
	IS_CABLE_C = 39
	IS_CABLE_C2 = 40
	IS_TERRESTRIAL_T = 41
	IS_TERRESTRIAL_T2 = 42
	volume = 43
	volumedata = 44
	DMXstatus = 45
	IsRDS = 46
	IsNGM = 47
	IsHDR10 = 48
	IsHDR = 49
	IsHLG = 50
	IsSDR = 51
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "apid":
			self.type = self.apid
		elif type == "vpid":
			self.type = self.vpid
		elif type == "sid":
			self.type = self.sid
		elif type == "onid":
			self.type = self.onid
		elif type == "tsid":
			self.type = self.tsid
		elif type == "prcpid":
			self.type = self.prcpid
		elif type == "caids":
			self.type = self.caids
		elif type == "pmtpid":
			self.type = self.pmtpid
		elif type == "txtpid":
			self.type = self.txtpid
		elif type == "tsid":
			self.type = self.tsid
		elif type == "xres":
			self.type = self.xres
		elif type == "yres":
			self.type = self.yres
		elif type == "gamma":
			self.type = self.gamma
		elif type == "atype":
			self.type = self.atype
		elif type == "vtype":
			self.type = self.vtype
		elif type == "avtype":
			self.type = self.avtype
		elif type == "fps":
			self.type = self.fps
		elif type == "tbps":
			self.type = self.tbps
		elif type == "vsize":
			self.type = self.vsize
		elif type == "ttype":
			self.type = self.ttype
		elif type == "VideoWidth":
			self.type = self.XRES
		elif type == "VideoHeight":
			self.type = self.YRES
		elif type == "IsWidescreen":
			self.type = self.IS_WIDESCREEN
		elif type == "HasTelext":
			self.type = self.HAS_TELETEXT
		elif type == "IsMultichannel":
			self.type = self.IS_MULTICHANNEL
		elif type == "IsCrypted":
			self.type = self.IS_CRYPTED
		elif type == "IsFta":
			self.type = self.IS_FTA
		elif type == "HasHBBTV":
			self.type = self.HAS_HBBTV
		elif type == "SubservicesAvailable":
			self.type = self.SUBSERVICES_AVAILABLE
		elif type == "AudioTracksAvailable":
			self.type = self.AUDIOTRACKS_AVAILABLE
		elif type == "SubtitlesAvailable":
			self.type = self.SUBTITLES_AVAILABLE
		elif type == "Editmode":
			self.type = self.EDITMODE
		elif type == "Framerate":
			self.type = self.FRAMERATE
		elif type == "IsSatellite":
			self.type = self.IS_SATELLITE
		elif type == "IsSatelliteS":
			self.type = self.IS_SATELLITE_S
		elif type == "IsSatelliteS2":
			self.type = self.IS_SATELLITE_S2
		elif type == "IsCable":
			self.type = self.IS_CABLE
		elif type == "IsCableC":
			self.type = self.IS_CABLE_C
		elif type == "IsCableC2":
			self.type = self.IS_CABLE_C2
		elif type == "IsTerrestrial":
			self.type = self.IS_TERRESTRIAL
		elif type == "IsTerrestrialT":
			self.type = self.IS_TERRESTRIAL_T
		elif type == "IsTerrestrialT2":
			self.type = self.IS_TERRESTRIAL_T2
		elif type == "IsStreamTV":
			self.type = self.IS_STREAMTV
		elif type == "IsVolume":
			self.type = self.volume
		elif type == "DMXstatus":
			self.type = self.DMXstatus
		elif type == "IsVolumeData":
			self.type = self.volumedata
		elif type == "IsRDS":
			self.type = self.IsRDS
		elif type == "IsNGM":
			self.type = self.IsNGM
		elif type == "IsSDR":
			self.type = self.IsSDR
		elif type == "IsHDR":
			self.type = self.IsHDR
		elif type == "IsHDR10":
			self.type = self.IsHDR10
		elif type == "IsHLG":
			self.type = self.IsHLG
		else:
			self.type = self.format
			self.sfmt = type[:]
		self.poll_interval = 1000
		self.poll_enabled = True

	def getServiceInfoString2(self, info, what, convert = lambda x: "%d" % x):
		v = info.getInfo(what)
		if v == -3:
			t_objs = info.getInfoObject(what)
			if t_objs and (len(t_objs) > 0):
				ret_val=""
				for t_obj in t_objs:
					ret_val += "%.4X " % t_obj
				return ret_val[:-1]
			else:
				return ""
		return convert(v)

	def getServiceInfoString(self, info, what, convert = lambda x: "%d" % x):
		v = info.getInfo(what)
		if v == -1:
			return ""
		if v == -2:
			return info.getInfoString(what)
		return convert(v)

	@cached
	def getText(self):
		self.stream = { 'apid':" ", 'vpid':" ", 'sid':" ", 'onid':" ", 'tsid':" ", 'prcpid':" ", 'caids':"FTA", 'pmtpid':" ", 'txtpid':" ", 'xres':" ", 'yres':" ", 'gamma':" ", 'atype':" ", 'vtype':" ", 'avtype':" ", 'fps':" ", 'tbps':" ", 'vsize':" ",}
		streaminfo = ""
		array_caids = []
		service = self.source.service
		info = service and service.info()
		if info:
			apid = info.getInfo(iServiceInformation.sAudioPID)
			if apid < 0:
				apid = 0
			self.stream['apid'] = "%0.4X" % int(apid)
			vpid = info.getInfo(iServiceInformation.sVideoPID)
			if vpid < 0:
				vpid = 0
			self.stream['vpid'] = "%0.4X" % int(vpid)
			sidpid = info.getInfo(iServiceInformation.sSID)
			if sidpid < 0:
				sidpid = 0
			self.stream['sid'] = "%0.4X" % int(sidpid)
			onid = info.getInfo(iServiceInformation.sONID)
			if onid < 0:
				onid = 0
			self.stream['onid'] = "%0.4X" % int(onid)
			tsid = info.getInfo(iServiceInformation.sTSID)
			if tsid < 0:
				tsid = 0
			self.stream['tsid'] = "%0.4X" % int(tsid)
			pcrpid = info.getInfo(iServiceInformation.sPCRPID)
			if pcrpid < 0:
				pcrpid = 0
			self.stream['prcpid'] = "%0.4X" % int(pcrpid)
			self.stream['pmtpid'] = self.getServiceInfoString(info, iServiceInformation.sPMTPID)
			self.stream['txtpid'] = self.getServiceInfoString(info, iServiceInformation.sTXTPID)
			caidinfo = self.getServiceInfoString2(info, iServiceInformation.sCAIDs)
			for caid in caidinfo.split():
				array_caids.append(caid)
			self.stream['caids'] = ' '.join(str(x) for x in set(array_caids))
			self.stream['yres'] = self.getServiceInfoString(info, iServiceInformation.sVideoHeight) + ("i", "p", "")[info.getInfo(iServiceInformation.sProgressive)]
			self.stream['xres'] = self.getServiceInfoString(info, iServiceInformation.sVideoWidth)
			self.stream['gamma'] = ("SDR", "HDR", "HDR10", "HLG", "")[info.getInfo(iServiceInformation.sGamma)]
			audio = service.audioTracks()
			if audio:
				if audio.getCurrentTrack() > -1:
					self.stream['atype'] = str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription()).replace(" audio","").replace(" ","_")
			self.stream['vtype'] = codec_data[info.getInfo(iServiceInformation.sVideoType)]
			self.stream['avtype'] = self.stream['vtype'] + '/' + self.stream['atype']
			if self.stream['avtype'].strip() == '/':
				self.stream['avtype'] = ''
			elif self.stream['avtype'].strip().startswith('/'):
				self.stream['avtype'] = self.stream['atype']
			elif self.stream['avtype'].strip().endswith('/'):
				self.stream['avtype'] = self.stream['vtype']
			fps = (info.getInfo(iServiceInformation.sFrameRate) + 500) // 1000
			if not fps or fps == -1:
				try:
					fps = (int(open("/proc/stb/vmpeg/0/framerate", "r").read()) + 500) // 1000
				except:
					pass
			self.stream['fps'] = '%s' % str(fps)
			self.stream['tbps'] = self.getServiceInfoString(info, iServiceInformation.sTransferBPS, lambda x: "%d kB/s" % (x/1024))
			self.stream['vsize'] = '%sx%s' % (self.stream['xres'], self.stream['yres'])
			if len(self.stream['vsize'].strip()) == 1:
				self.stream['vsize'] = ''
			elif self.stream['vsize'].strip().startswith('0x'):
				self.stream['vsize'] = ''
			self.tpdata = info.getInfoObject(iServiceInformation.sTransponderData)
			if self.tpdata:
				self.stream['ttype'] = self.tpdata.get('tuner_type', '')
				if self.stream['ttype'] == 'DVB-S' and service.streamed() == None:
					if self.tpdata.get('system', 0) == 1:
						self.stream['ttype'] = 'DVB-S2'
				elif self.stream['ttype'] == 'DVB-C' and service.streamed() == None:
					if self.tpdata.get('system', 0) == 1:
						self.stream['ttype'] = 'DVB-C2'
				elif self.stream['ttype'] == 'DVB-T' and service.streamed() == None:
					if self.tpdata.get('system', 0) == 1:
						self.stream['ttype'] = 'DVB-T2'
			else:
				self.stream['ttype'] = 'IP-TV'
		else:
			return ""
		if self.type == self.apid:
			streaminfo = self.stream['apid']
		elif self.type == self.vpid:
			streaminfo = self.stream['vpid']
		elif self.type == self.sid:
			streaminfo = self.stream['sid']
		elif self.type == self.onid:
			streaminfo = self.stream['onid']
		elif self.type == self.tsid:
			streaminfo = self.stream['tsid']
		elif self.type == self.prcpid:
			streaminfo = self.stream['prcpid']
		elif self.type == self.caids:
			streaminfo = self.stream['caids']
		elif self.type == self.pmtpid:
			streaminfo = self.stream['pmtpid']
		elif self.type == self.txtpid:
			streaminfo = self.stream['txtpid']
		elif self.type == self.tsid:
			streaminfo = self.stream['tsid']
		elif self.type == self.xres:
			streaminfo = self.stream['xres']
		elif self.type == self.yres:
			streaminfo = self.stream['yres']
		elif self.type == self.gamma:
			streaminfo = self.stream['gamma']
		elif self.type == self.atype:
			streaminfo = self.stream['atype']
		elif self.type == self.vtype:
			streaminfo = self.stream['vtype']
		elif self.type == self.avtype:
			streaminfo = self.stream['avtype']
		elif self.type == self.fps:
			streaminfo = self.stream['fps']
		elif self.type == self.tbps:
			streaminfo = self.stream['tbps']
		elif self.type == self.ttype:
			streaminfo = self.stream['ttype']
		elif self.type == self.volume:
			streaminfo = _('Vol: %s') % config.audio.volume.value
		elif self.type == self.volumedata:
			streaminfo = '%s' % config.audio.volume.value
		elif self.type == self.vsize:
			streaminfo = self.stream['vsize']
		elif self.type == self.format:
			tmp = self.sfmt[:]
			for param in tmp.split():
				if param != '':
					if param[0] != '%':
						streaminfo += ' ' + param
					else:
						streaminfo += ' ' + self.stream[param.strip('%')].strip()
		return streaminfo
	text = property(getText)

	@cached
	def getValue(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return -1
		if self.type == self.XRES:
			return info.getInfo(iServiceInformation.sVideoWidth)
		if self.type == self.YRES:
			return info.getInfo(iServiceInformation.sVideoHeight)
		if self.type == self.FRAMERATE:
			return info.getInfo(iServiceInformation.sFrameRate)
		return -1
	value = property(getValue)

	@cached
	def getBoolean(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return False
		self.tpdata = info.getInfoObject(iServiceInformation.sTransponderData)
		if self.tpdata:
			type = self.tpdata.get('tuner_type', '')
		else:
			type = 'IP-TV'
		if self.type == self.HAS_TELETEXT:
			tpid = info.getInfo(iServiceInformation.sTXTPID)
			return tpid != -1
		elif self.type == self.IsRDS:
			if info.getInfo(iServiceInformation.sVideoHeight) > 0:
				return False
			else:
				return True

		elif self.type == self.IS_MULTICHANNEL:
			audio = service.audioTracks()
			if audio:
				if audio.getCurrentTrack() > -1:
					description = str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription())
					if "AC3" in description or "AC-3" in description or "DTS" in description or "THX" in description:
						return True
			return False
		elif self.type == self.IS_CRYPTED:
			return info.getInfo(iServiceInformation.sIsCrypted) == 1
		elif self.type == self.IS_FTA:
			return info.getInfo(iServiceInformation.sIsCrypted) == 0
		elif self.type == self.IsNGM:	
			if info.getInfo(iServiceInformation.sGamma) < 0:
				return True
			return False
		elif self.type == self.IsSDR:
			return info.getInfo(iServiceInformation.sGamma) == 0
		elif self.type == self.IsHDR:
			return info.getInfo(iServiceInformation.sGamma) == 1
		elif self.type == self.IsHDR10:
			return info.getInfo(iServiceInformation.sGamma) == 2
		elif self.type == self.IsHLG:
			return info.getInfo(iServiceInformation.sGamma) == 3
		elif self.type == self.IS_WIDESCREEN:
			return info.getInfo(iServiceInformation.sAspect) in WIDESCREEN
		elif self.type == self.SUBSERVICES_AVAILABLE:
			return hasActiveSubservicesForCurrentChannel(service)	
		elif self.type == self.HAS_HBBTV:
			return info.getInfoString(iServiceInformation.sHBBTVUrl) != ""
		elif self.type == self.AUDIOTRACKS_AVAILABLE:
			audio = service.audioTracks()
			if audio:
				n = audio.getNumberOfTracks()
				idx = 0
				while idx < n:
					i = audio.getTrackInfo(idx)
					description = i.getDescription()
					if description in ("AC3", "AC3+", "DTS", "DTS-HD", "AC-3"):
						if self.type == self.IS_MULTICHANNEL:
							return True
						elif self.type == self.IS_STEREO:
							return False
					idx += 1
				if self.type == self.IS_MULTICHANNEL:
					return False
				elif self.type == self.IS_STEREO:
					return True
			return False
		elif self.type == self.SUBTITLES_AVAILABLE:
			subtitle = service and service.subtitle()
			return bool(subtitle and subtitle.getSubtitleList())
		elif self.type == self.EDITMODE:
			return bool(hasattr(self.source, "editmode") and self.source.editmode)
		elif self.type == self.IS_SATELLITE:
			if type == 'DVB-S':
				return True
		elif self.type == self.IS_CABLE:
			if type == 'DVB-C':
				return True
		elif self.type == self.IS_TERRESTRIAL:
			if type == 'DVB-T':
				return True
		elif self.type == self.IS_STREAMTV:
			if service.streamed() != None:
				return True
		elif self.type == self.IS_SATELLITE_S:
			if type == 'DVB-S' and service.streamed() == None:
				if self.tpdata.get('system', 0) == 0:
					return True
		elif self.type == self.IS_SATELLITE_S2:
			if type == 'DVB-S' and service.streamed() == None:
				if self.tpdata.get('system', 0) == 1:
					return True
		elif self.type == self.IS_CABLE_C:
			if type == 'DVB-C' and service.streamed() == None:
				if self.tpdata.get('system', 0) == 0:
					return True
		elif self.type == self.IS_CABLE_C2:
			if type == 'DVB-C' and service.streamed() == None:
				if self.tpdata.get('system', 0) == 1:
					return True
		elif self.type == self.IS_TERRESTRIAL_T:
			if type == 'DVB-T' and service.streamed() == None:
				if self.tpdata.get('system', 0) == 0:
					return True
		elif self.type == self.IS_TERRESTRIAL_T2:
			if type == 'DVB-T' and service.streamed() == None:
				if self.tpdata.get('system', 0) == 1:
					return True
		elif self.type == self.DMXstatus:
			if config.av.downmix_ac3.value == True or config.av.downmix_ac3.value == "downmix":
				return True
			else:
				return False
		return False
	boolean = property(getBoolean)

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			if what[1] == iPlayableService.evVideoSizeChanged or what[1] == iPlayableService.evUpdatedInfo:
				Converter.changed(self, what)
		elif what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
			Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)

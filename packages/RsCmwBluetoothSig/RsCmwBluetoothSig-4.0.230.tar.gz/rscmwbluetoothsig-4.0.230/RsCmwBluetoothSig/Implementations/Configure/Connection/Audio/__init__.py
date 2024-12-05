from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioCls:
	"""Audio commands group definition. 41 total commands, 25 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("audio", core, parent)

	@property
	def bcount(self):
		"""bcount commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bcount'):
			from .Bcount import BcountCls
			self._bcount = BcountCls(self._core, self._cmd_group)
		return self._bcount

	@property
	def codec(self):
		"""codec commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_codec'):
			from .Codec import CodecCls
			self._codec = CodecCls(self._core, self._cmd_group)
		return self._codec

	@property
	def cdirection(self):
		"""cdirection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdirection'):
			from .Cdirection import CdirectionCls
			self._cdirection = CdirectionCls(self._core, self._cmd_group)
		return self._cdirection

	@property
	def sfrequency(self):
		"""sfrequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfrequency'):
			from .Sfrequency import SfrequencyCls
			self._sfrequency = SfrequencyCls(self._core, self._cmd_group)
		return self._sfrequency

	@property
	def cmode(self):
		"""cmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmode'):
			from .Cmode import CmodeCls
			self._cmode = CmodeCls(self._core, self._cmd_group)
		return self._cmode

	@property
	def fduration(self):
		"""fduration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fduration'):
			from .Fduration import FdurationCls
			self._fduration = FdurationCls(self._core, self._cmd_group)
		return self._fduration

	@property
	def iinterval(self):
		"""iinterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iinterval'):
			from .Iinterval import IintervalCls
			self._iinterval = IintervalCls(self._core, self._cmd_group)
		return self._iinterval

	@property
	def nsEvents(self):
		"""nsEvents commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsEvents'):
			from .NsEvents import NsEventsCls
			self._nsEvents = NsEventsCls(self._core, self._cmd_group)
		return self._nsEvents

	@property
	def sinterval(self):
		"""sinterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinterval'):
			from .Sinterval import SintervalCls
			self._sinterval = SintervalCls(self._core, self._cmd_group)
		return self._sinterval

	@property
	def sicp(self):
		"""sicp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sicp'):
			from .Sicp import SicpCls
			self._sicp = SicpCls(self._core, self._cmd_group)
		return self._sicp

	@property
	def sipc(self):
		"""sipc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sipc'):
			from .Sipc import SipcCls
			self._sipc = SipcCls(self._core, self._cmd_group)
		return self._sipc

	@property
	def ftcp(self):
		"""ftcp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ftcp'):
			from .Ftcp import FtcpCls
			self._ftcp = FtcpCls(self._core, self._cmd_group)
		return self._ftcp

	@property
	def ftpc(self):
		"""ftpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ftpc'):
			from .Ftpc import FtpcCls
			self._ftpc = FtpcCls(self._core, self._cmd_group)
		return self._ftpc

	@property
	def mscp(self):
		"""mscp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mscp'):
			from .Mscp import MscpCls
			self._mscp = MscpCls(self._core, self._cmd_group)
		return self._mscp

	@property
	def mspc(self):
		"""mspc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mspc'):
			from .Mspc import MspcCls
			self._mspc = MspcCls(self._core, self._cmd_group)
		return self._mspc

	@property
	def mpcp(self):
		"""mpcp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mpcp'):
			from .Mpcp import MpcpCls
			self._mpcp = MpcpCls(self._core, self._cmd_group)
		return self._mpcp

	@property
	def mppc(self):
		"""mppc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mppc'):
			from .Mppc import MppcCls
			self._mppc = MppcCls(self._core, self._cmd_group)
		return self._mppc

	@property
	def bncp(self):
		"""bncp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bncp'):
			from .Bncp import BncpCls
			self._bncp = BncpCls(self._core, self._cmd_group)
		return self._bncp

	@property
	def bnpc(self):
		"""bnpc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bnpc'):
			from .Bnpc import BnpcCls
			self._bnpc = BnpcCls(self._core, self._cmd_group)
		return self._bnpc

	@property
	def ominimum(self):
		"""ominimum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ominimum'):
			from .Ominimum import OminimumCls
			self._ominimum = OminimumCls(self._core, self._cmd_group)
		return self._ominimum

	@property
	def omaximum(self):
		"""omaximum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_omaximum'):
			from .Omaximum import OmaximumCls
			self._omaximum = OmaximumCls(self._core, self._cmd_group)
		return self._omaximum

	@property
	def cecOffset(self):
		"""cecOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cecOffset'):
			from .CecOffset import CecOffsetCls
			self._cecOffset = CecOffsetCls(self._core, self._cmd_group)
		return self._cecOffset

	@property
	def volControl(self):
		"""volControl commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_volControl'):
			from .VolControl import VolControlCls
			self._volControl = VolControlCls(self._core, self._cmd_group)
		return self._volControl

	@property
	def hfp(self):
		"""hfp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hfp'):
			from .Hfp import HfpCls
			self._hfp = HfpCls(self._core, self._cmd_group)
		return self._hfp

	@property
	def a2Dp(self):
		"""a2Dp commands group. 0 Sub-classes, 10 commands."""
		if not hasattr(self, '_a2Dp'):
			from .A2Dp import A2DpCls
			self._a2Dp = A2DpCls(self._core, self._cmd_group)
		return self._a2Dp

	# noinspection PyTypeChecker
	def get_sec_mode(self) -> enums.SecurityMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SECMode \n
		Snippet: value: enums.SecurityMode = driver.configure.connection.audio.get_sec_mode() \n
		Specifies security mode for audio tests. \n
			:return: security_mode: SEC2 | SEC3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SECMode?')
		return Conversions.str_to_scalar_enum(response, enums.SecurityMode)

	def set_sec_mode(self, security_mode: enums.SecurityMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SECMode \n
		Snippet: driver.configure.connection.audio.set_sec_mode(security_mode = enums.SecurityMode.SEC2) \n
		Specifies security mode for audio tests. \n
			:param security_mode: SEC2 | SEC3
		"""
		param = Conversions.enum_scalar_to_str(security_mode, enums.SecurityMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SECMode {param}')

	# noinspection PyTypeChecker
	def get_vlink(self) -> enums.VoiceLinkType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VLINk \n
		Snippet: value: enums.VoiceLinkType = driver.configure.connection.audio.get_vlink() \n
		No command help available \n
			:return: voice_link: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VLINk?')
		return Conversions.str_to_scalar_enum(response, enums.VoiceLinkType)

	def set_vlink(self, voice_link: enums.VoiceLinkType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VLINk \n
		Snippet: driver.configure.connection.audio.set_vlink(voice_link = enums.VoiceLinkType.ESCO) \n
		No command help available \n
			:param voice_link: No help available
		"""
		param = Conversions.enum_scalar_to_str(voice_link, enums.VoiceLinkType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:VLINk {param}')

	def get_pin_code(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:PINCode \n
		Snippet: value: str = driver.configure.connection.audio.get_pin_code() \n
		Specifies PIN code for audio profile tests. \n
			:return: pin_code: string
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:PINCode?')
		return trim_str_response(response)

	def set_pin_code(self, pin_code: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:PINCode \n
		Snippet: driver.configure.connection.audio.set_pin_code(pin_code = 'abc') \n
		Specifies PIN code for audio profile tests. \n
			:param pin_code: string
		"""
		param = Conversions.value_to_quoted_str(pin_code)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:PINCode {param}')

	def clone(self) -> 'AudioCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

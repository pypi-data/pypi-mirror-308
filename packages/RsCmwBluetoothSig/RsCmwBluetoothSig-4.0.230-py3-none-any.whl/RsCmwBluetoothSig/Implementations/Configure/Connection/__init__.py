from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectionCls:
	"""Connection commands group definition. 116 total commands, 24 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connection", core, parent)

	@property
	def audio(self):
		"""audio commands group. 25 Sub-classes, 3 commands."""
		if not hasattr(self, '_audio'):
			from .Audio import AudioCls
			self._audio = AudioCls(self._core, self._cmd_group)
		return self._audio

	@property
	def packets(self):
		"""packets commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_packets'):
			from .Packets import PacketsCls
			self._packets = PacketsCls(self._core, self._cmd_group)
		return self._packets

	@property
	def synWord(self):
		"""synWord commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synWord'):
			from .SynWord import SynWordCls
			self._synWord = SynWordCls(self._core, self._cmd_group)
		return self._synWord

	@property
	def cscheme(self):
		"""cscheme commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cscheme'):
			from .Cscheme import CschemeCls
			self._cscheme = CschemeCls(self._core, self._cmd_group)
		return self._cscheme

	@property
	def fec(self):
		"""fec commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fec'):
			from .Fec import FecCls
			self._fec = FecCls(self._core, self._cmd_group)
		return self._fec

	@property
	def phy(self):
		"""phy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_phy'):
			from .Phy import PhyCls
			self._phy = PhyCls(self._core, self._cmd_group)
		return self._phy

	@property
	def powerControl(self):
		"""powerControl commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_powerControl'):
			from .PowerControl import PowerControlCls
			self._powerControl = PowerControlCls(self._core, self._cmd_group)
		return self._powerControl

	@property
	def paging(self):
		"""paging commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_paging'):
			from .Paging import PagingCls
			self._paging = PagingCls(self._core, self._cmd_group)
		return self._paging

	@property
	def bdAddress(self):
		"""bdAddress commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bdAddress'):
			from .BdAddress import BdAddressCls
			self._bdAddress = BdAddressCls(self._core, self._cmd_group)
		return self._bdAddress

	@property
	def inquiry(self):
		"""inquiry commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_inquiry'):
			from .Inquiry import InquiryCls
			self._inquiry = InquiryCls(self._core, self._cmd_group)
		return self._inquiry

	@property
	def eutCharacter(self):
		"""eutCharacter commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_eutCharacter'):
			from .EutCharacter import EutCharacterCls
			self._eutCharacter = EutCharacterCls(self._core, self._cmd_group)
		return self._eutCharacter

	@property
	def wfcMap(self):
		"""wfcMap commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_wfcMap'):
			from .WfcMap import WfcMapCls
			self._wfcMap = WfcMapCls(self._core, self._cmd_group)
		return self._wfcMap

	@property
	def slatency(self):
		"""slatency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_slatency'):
			from .Slatency import SlatencyCls
			self._slatency = SlatencyCls(self._core, self._cmd_group)
		return self._slatency

	@property
	def rencryption(self):
		"""rencryption commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rencryption'):
			from .Rencryption import RencryptionCls
			self._rencryption = RencryptionCls(self._core, self._cmd_group)
		return self._rencryption

	@property
	def iencryption(self):
		"""iencryption commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iencryption'):
			from .Iencryption import IencryptionCls
			self._iencryption = IencryptionCls(self._core, self._cmd_group)
		return self._iencryption

	@property
	def cmw(self):
		"""cmw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmw'):
			from .Cmw import CmwCls
			self._cmw = CmwCls(self._core, self._cmd_group)
		return self._cmw

	@property
	def address(self):
		"""address commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_address'):
			from .Address import AddressCls
			self._address = AddressCls(self._core, self._cmd_group)
		return self._address

	@property
	def raddress(self):
		"""raddress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_raddress'):
			from .Raddress import RaddressCls
			self._raddress = RaddressCls(self._core, self._cmd_group)
		return self._raddress

	@property
	def svTimeout(self):
		"""svTimeout commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_svTimeout'):
			from .SvTimeout import SvTimeoutCls
			self._svTimeout = SvTimeoutCls(self._core, self._cmd_group)
		return self._svTimeout

	@property
	def interval(self):
		"""interval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interval'):
			from .Interval import IntervalCls
			self._interval = IntervalCls(self._core, self._cmd_group)
		return self._interval

	@property
	def sinterval(self):
		"""sinterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinterval'):
			from .Sinterval import SintervalCls
			self._sinterval = SintervalCls(self._core, self._cmd_group)
		return self._sinterval

	@property
	def ainterval(self):
		"""ainterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ainterval'):
			from .Ainterval import AintervalCls
			self._ainterval = AintervalCls(self._core, self._cmd_group)
		return self._ainterval

	@property
	def swindow(self):
		"""swindow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swindow'):
			from .Swindow import SwindowCls
			self._swindow = SwindowCls(self._core, self._cmd_group)
		return self._swindow

	@property
	def pperiod(self):
		"""pperiod commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pperiod'):
			from .Pperiod import PperiodCls
			self._pperiod = PperiodCls(self._core, self._cmd_group)
		return self._pperiod

	# noinspection PyTypeChecker
	def get_btype(self) -> enums.BurstType:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BTYPe \n
		Snippet: value: enums.BurstType = driver.configure.connection.get_btype() \n
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- BR/EDR in test mode
			- LE in direct test mode \n
			:return: burst_type: BR | EDR | LE BR: 'Basic Rate' EDR: 'Enhanced Data Rate' LE: 'Low Energy'
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BurstType)

	def set_btype(self, burst_type: enums.BurstType) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BTYPe \n
		Snippet: driver.configure.connection.set_btype(burst_type = enums.BurstType.BR) \n
			INTRO_CMD_HELP: Defines the Bluetooth burst type. The command is relevant for: \n
			- BR/EDR in test mode
			- LE in direct test mode \n
			:param burst_type: BR | EDR | LE BR: 'Basic Rate' EDR: 'Enhanced Data Rate' LE: 'Low Energy'
		"""
		param = Conversions.enum_scalar_to_str(burst_type, enums.BurstType)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:BTYPe {param}')

	def get_delay(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:DELay \n
		Snippet: value: bool = driver.configure.connection.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:DELay?')
		return Conversions.str_to_bool(response)

	def set_delay(self, delay: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:DELay \n
		Snippet: driver.configure.connection.set_delay(delay = False) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.bool_to_str(delay)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:DELay {param}')

	def get_whitening(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WHITening \n
		Snippet: value: bool = driver.configure.connection.get_whitening() \n
		Sets whether the EUT has to transmit ACL packets scrambled with a particular data sequence in a loopback mode. \n
			:return: whitening: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WHITening?')
		return Conversions.str_to_bool(response)

	def set_whitening(self, whitening: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WHITening \n
		Snippet: driver.configure.connection.set_whitening(whitening = False) \n
		Sets whether the EUT has to transmit ACL packets scrambled with a particular data sequence in a loopback mode. \n
			:param whitening: OFF | ON
		"""
		param = Conversions.bool_to_str(whitening)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:WHITening {param}')

	def clone(self) -> 'ConnectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConnectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

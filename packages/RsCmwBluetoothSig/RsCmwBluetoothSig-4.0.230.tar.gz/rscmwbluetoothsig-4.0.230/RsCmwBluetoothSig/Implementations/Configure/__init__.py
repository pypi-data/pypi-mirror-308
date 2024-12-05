from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConfigureCls:
	"""Configure commands group definition. 425 total commands, 12 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("configure", core, parent)

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import DelayCls
			self._delay = DelayCls(self._core, self._cmd_group)
		return self._delay

	@property
	def connection(self):
		"""connection commands group. 24 Sub-classes, 3 commands."""
		if not hasattr(self, '_connection'):
			from .Connection import ConnectionCls
			self._connection = ConnectionCls(self._core, self._cmd_group)
		return self._connection

	@property
	def utpMode(self):
		"""utpMode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_utpMode'):
			from .UtpMode import UtpModeCls
			self._utpMode = UtpModeCls(self._core, self._cmd_group)
		return self._utpMode

	@property
	def audio(self):
		"""audio commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_audio'):
			from .Audio import AudioCls
			self._audio = AudioCls(self._core, self._cmd_group)
		return self._audio

	@property
	def lowEnergy(self):
		"""lowEnergy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lowEnergy'):
			from .LowEnergy import LowEnergyCls
			self._lowEnergy = LowEnergyCls(self._core, self._cmd_group)
		return self._lowEnergy

	@property
	def usbSettings(self):
		"""usbSettings commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbSettings'):
			from .UsbSettings import UsbSettingsCls
			self._usbSettings = UsbSettingsCls(self._core, self._cmd_group)
		return self._usbSettings

	@property
	def comSettings(self):
		"""comSettings commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_comSettings'):
			from .ComSettings import ComSettingsCls
			self._comSettings = ComSettingsCls(self._core, self._cmd_group)
		return self._comSettings

	@property
	def hwInterface(self):
		"""hwInterface commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hwInterface'):
			from .HwInterface import HwInterfaceCls
			self._hwInterface = HwInterfaceCls(self._core, self._cmd_group)
		return self._hwInterface

	@property
	def debug(self):
		"""debug commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_debug'):
			from .Debug import DebugCls
			self._debug = DebugCls(self._core, self._cmd_group)
		return self._debug

	@property
	def tconnection(self):
		"""tconnection commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tconnection'):
			from .Tconnection import TconnectionCls
			self._tconnection = TconnectionCls(self._core, self._cmd_group)
		return self._tconnection

	@property
	def rfSettings(self):
		"""rfSettings commands group. 10 Sub-classes, 8 commands."""
		if not hasattr(self, '_rfSettings'):
			from .RfSettings import RfSettingsCls
			self._rfSettings = RfSettingsCls(self._core, self._cmd_group)
		return self._rfSettings

	@property
	def rxQuality(self):
		"""rxQuality commands group. 10 Sub-classes, 4 commands."""
		if not hasattr(self, '_rxQuality'):
			from .RxQuality import RxQualityCls
			self._rxQuality = RxQualityCls(self._core, self._cmd_group)
		return self._rxQuality

	# noinspection PyTypeChecker
	def get_op_mode(self) -> enums.OperatingMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:OPMode \n
		Snippet: value: enums.OperatingMode = driver.configure.get_op_mode() \n
		Specifies the operating mode of R&S CMW. \n
			:return: operating_mode: CNTest | RFTest | ECMode | PROFiles | AUDio | UTPMode CNTest: connection test for BR/EDR or LE (OTA) RFTest: test mode for BR/EDR or direct test for LE ECMode: echo mode for BR/EDR or LE PROFiles: profiles for BR/EDR AUDio: audio mode for BR/EDR or LE
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:OPMode?')
		return Conversions.str_to_scalar_enum(response, enums.OperatingMode)

	def set_op_mode(self, operating_mode: enums.OperatingMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:OPMode \n
		Snippet: driver.configure.set_op_mode(operating_mode = enums.OperatingMode.AUDio) \n
		Specifies the operating mode of R&S CMW. \n
			:param operating_mode: CNTest | RFTest | ECMode | PROFiles | AUDio | UTPMode CNTest: connection test for BR/EDR or LE (OTA) RFTest: test mode for BR/EDR or direct test for LE ECMode: echo mode for BR/EDR or LE PROFiles: profiles for BR/EDR AUDio: audio mode for BR/EDR or LE
		"""
		param = Conversions.enum_scalar_to_str(operating_mode, enums.OperatingMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:OPMode {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.TestMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TMODe \n
		Snippet: value: enums.TestMode = driver.configure.get_tmode() \n
		Selects the test mode that the EUT enters in a test mode connection. \n
			:return: test_mode: LOOPback | TXTest LOOPback: BR/EDR loopback test mode TXTest: BR/EDR transmitter test mode
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TestMode)

	def set_tmode(self, test_mode: enums.TestMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TMODe \n
		Snippet: driver.configure.set_tmode(test_mode = enums.TestMode.LOOPback) \n
		Selects the test mode that the EUT enters in a test mode connection. \n
			:param test_mode: LOOPback | TXTest LOOPback: BR/EDR loopback test mode TXTest: BR/EDR transmitter test mode
		"""
		param = Conversions.enum_scalar_to_str(test_mode, enums.TestMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TMODe {param}')

	# noinspection PyTypeChecker
	def get_cprotocol(self) -> enums.CommProtocol:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CPRotocol \n
		Snippet: value: enums.CommProtocol = driver.configure.get_cprotocol() \n
		Specifies the communication protocol for direct test mode. \n
			:return: comm_protocol: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CPRotocol?')
		return Conversions.str_to_scalar_enum(response, enums.CommProtocol)

	def set_cprotocol(self, comm_protocol: enums.CommProtocol) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CPRotocol \n
		Snippet: driver.configure.set_cprotocol(comm_protocol = enums.CommProtocol.HCI) \n
		Specifies the communication protocol for direct test mode. \n
			:param comm_protocol: HCI | TWO HCI or two-wire UART interface
		"""
		param = Conversions.enum_scalar_to_str(comm_protocol, enums.CommProtocol)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CPRotocol {param}')

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.SignalingStandard:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:STANdard \n
		Snippet: value: enums.SignalingStandard = driver.configure.get_standard() \n
		Selects classic (BR/EDR) or low energy (LE) bursts. \n
			:return: sig_std: CLASsic | LESignaling
		"""
		response = self._core.io.query_str_with_opc('CONFigure:BLUetooth:SIGNaling<Instance>:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.SignalingStandard)

	def set_standard(self, sig_std: enums.SignalingStandard) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:STANdard \n
		Snippet: driver.configure.set_standard(sig_std = enums.SignalingStandard.CLASsic) \n
		Selects classic (BR/EDR) or low energy (LE) bursts. \n
			:param sig_std: CLASsic | LESignaling
		"""
		param = Conversions.enum_scalar_to_str(sig_std, enums.SignalingStandard)
		self._core.io.write_with_opc(f'CONFigure:BLUetooth:SIGNaling<Instance>:STANdard {param}')

	def clone(self) -> 'ConfigureCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConfigureCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

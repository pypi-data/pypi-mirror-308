from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StopBitsCls:
	"""StopBits commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stopBits", core, parent)

	def set(self, stop_bits: enums.StopBits, commSettings=repcap.CommSettings.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:STOPbits \n
		Snippet: driver.configure.comSettings.stopBits.set(stop_bits = enums.StopBits.S1, commSettings = repcap.CommSettings.Default) \n
		Specifies the transmission parameters of serial connection. \n
			:param stop_bits: S1 | S2 Number of bits used for stop indication
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
		"""
		param = Conversions.enum_scalar_to_str(stop_bits, enums.StopBits)
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:STOPbits {param}')

	# noinspection PyTypeChecker
	def get(self, commSettings=repcap.CommSettings.Default) -> enums.StopBits:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:STOPbits \n
		Snippet: value: enums.StopBits = driver.configure.comSettings.stopBits.get(commSettings = repcap.CommSettings.Default) \n
		Specifies the transmission parameters of serial connection. \n
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
			:return: stop_bits: S1 | S2 Number of bits used for stop indication"""
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:STOPbits?')
		return Conversions.str_to_scalar_enum(response, enums.StopBits)

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ComPortCls:
	"""ComPort commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("comPort", core, parent)

	def set(self, no: int, commSettings=repcap.CommSettings.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:COMPort \n
		Snippet: driver.configure.comSettings.comPort.set(no = 1, commSettings = repcap.CommSettings.Default) \n
		Specifies the virtual COM port to be used for USB connection with USB to RS232 adapter. \n
			:param no: 1..2 1: HW interface for LE tests 2: HW interface for BR / EDR tests
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
		"""
		param = Conversions.decimal_value_to_str(no)
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:COMPort {param}')

	def get(self, commSettings=repcap.CommSettings.Default) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:COMPort \n
		Snippet: value: int = driver.configure.comSettings.comPort.get(commSettings = repcap.CommSettings.Default) \n
		Specifies the virtual COM port to be used for USB connection with USB to RS232 adapter. \n
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
			:return: no: 1..2 1: HW interface for LE tests 2: HW interface for BR / EDR tests"""
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:COMPort?')
		return Conversions.str_to_int(response)

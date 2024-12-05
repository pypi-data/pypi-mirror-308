from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BaudRateCls:
	"""BaudRate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("baudRate", core, parent)

	def set(self, baud_rate: enums.BaudRate, commSettings=repcap.CommSettings.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:BAUDrate \n
		Snippet: driver.configure.comSettings.baudRate.set(baud_rate = enums.BaudRate.B110, commSettings = repcap.CommSettings.Default) \n
		Specifies the transmission parameters of serial connection. \n
			:param baud_rate: B110 | B300 | B600 | B12K | B24K | B48K | B96K | B14K | B19K | B28K | B38K | B57K | B115k | B234k | B460k | B500k | B576k | B921k | B1M | B1M5 | B2M | B3M | B3M5 | B4M Data transmission rate in symbol: 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 2000000, 3000000, 3500000, 4000000
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
		"""
		param = Conversions.enum_scalar_to_str(baud_rate, enums.BaudRate)
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:BAUDrate {param}')

	# noinspection PyTypeChecker
	def get(self, commSettings=repcap.CommSettings.Default) -> enums.BaudRate:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:BAUDrate \n
		Snippet: value: enums.BaudRate = driver.configure.comSettings.baudRate.get(commSettings = repcap.CommSettings.Default) \n
		Specifies the transmission parameters of serial connection. \n
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
			:return: baud_rate: B110 | B300 | B600 | B12K | B24K | B48K | B96K | B14K | B19K | B28K | B38K | B57K | B115k | B234k | B460k | B500k | B576k | B921k | B1M | B1M5 | B2M | B3M | B3M5 | B4M Data transmission rate in symbol: 110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 2000000, 3000000, 3500000, 4000000"""
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:BAUDrate?')
		return Conversions.str_to_scalar_enum(response, enums.BaudRate)

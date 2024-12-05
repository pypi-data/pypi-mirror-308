from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DbitsCls:
	"""Dbits commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dbits", core, parent)

	def set(self, data_bits: enums.DataBits, commSettings=repcap.CommSettings.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:DBITs \n
		Snippet: driver.configure.comSettings.dbits.set(data_bits = enums.DataBits.D7, commSettings = repcap.CommSettings.Default) \n
		No command help available \n
			:param data_bits: No help available
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
		"""
		param = Conversions.enum_scalar_to_str(data_bits, enums.DataBits)
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:DBITs {param}')

	# noinspection PyTypeChecker
	def get(self, commSettings=repcap.CommSettings.Default) -> enums.DataBits:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:DBITs \n
		Snippet: value: enums.DataBits = driver.configure.comSettings.dbits.get(commSettings = repcap.CommSettings.Default) \n
		No command help available \n
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
			:return: data_bits: No help available"""
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:DBITs?')
		return Conversions.str_to_scalar_enum(response, enums.DataBits)

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ParityCls:
	"""Parity commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("parity", core, parent)

	def set(self, parity: enums.Parity, commSettings=repcap.CommSettings.Default) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:PARity \n
		Snippet: driver.configure.comSettings.parity.set(parity = enums.Parity.EVEN, commSettings = repcap.CommSettings.Default) \n
		Specifies the transmission parameters of serial connection. \n
			:param parity: NONE | ODD | EVEN Number of parity bits
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
		"""
		param = Conversions.enum_scalar_to_str(parity, enums.Parity)
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:PARity {param}')

	# noinspection PyTypeChecker
	def get(self, commSettings=repcap.CommSettings.Default) -> enums.Parity:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings<nr>:PARity \n
		Snippet: value: enums.Parity = driver.configure.comSettings.parity.get(commSettings = repcap.CommSettings.Default) \n
		Specifies the transmission parameters of serial connection. \n
			:param commSettings: optional repeated capability selector. Default value: Hw1 (settable in the interface 'ComSettings')
			:return: parity: NONE | ODD | EVEN Number of parity bits"""
		commSettings_cmd_val = self._cmd_group.get_repcap_cmd_value(commSettings, repcap.CommSettings)
		response = self._core.io.query_str(f'CONFigure:BLUetooth:SIGNaling<Instance>:COMSettings{commSettings_cmd_val}:PARity?')
		return Conversions.str_to_scalar_enum(response, enums.Parity)

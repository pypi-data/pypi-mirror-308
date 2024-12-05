from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def get_state(self) -> bool:
		"""SCPI: SOURce:BLUetooth:SIGNaling<Instance>:STATe \n
		Snippet: value: bool = driver.source.get_state() \n
		Sets/gets the main state of the 'Bluetooth Signaling' application. Signaling actions such as inquiry or paging are
		initiated using the method RsCmwBluetoothSig.Call.Connection.Action.value command. \n
			:return: main_state: ON | OFF | 1 | 0 When turned ON, the R&S CMW switches to standby state (see method RsCmwBluetoothSig.Connection.State.fetch)
		"""
		response = self._core.io.query_str_with_opc('SOURce:BLUetooth:SIGNaling<Instance>:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, main_state: bool) -> None:
		"""SCPI: SOURce:BLUetooth:SIGNaling<Instance>:STATe \n
		Snippet: driver.source.set_state(main_state = False) \n
		Sets/gets the main state of the 'Bluetooth Signaling' application. Signaling actions such as inquiry or paging are
		initiated using the method RsCmwBluetoothSig.Call.Connection.Action.value command. \n
			:param main_state: ON | OFF | 1 | 0 When turned ON, the R&S CMW switches to standby state (see method RsCmwBluetoothSig.Connection.State.fetch)
		"""
		param = Conversions.bool_to_str(main_state)
		self._core.io.write_with_opc(f'SOURce:BLUetooth:SIGNaling<Instance>:STATe {param}')

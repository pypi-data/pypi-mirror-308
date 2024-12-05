from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_2_m(self) -> int:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:EPLength:LENergy:LE2M \n
		Snippet: value: int = driver.diagnostic.connection.packets.epLength.lowEnergy.get_le_2_m() \n
		No command help available \n
			:return: payload_length: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:EPLength:LENergy:LE2M?')
		return Conversions.str_to_int(response)

	def set_le_2_m(self, payload_length: int) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:EPLength:LENergy:LE2M \n
		Snippet: driver.diagnostic.connection.packets.epLength.lowEnergy.set_le_2_m(payload_length = 1) \n
		No command help available \n
			:param payload_length: No help available
		"""
		param = Conversions.decimal_value_to_str(payload_length)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:CONNection:PACKets:EPLength:LENergy:LE2M {param}')

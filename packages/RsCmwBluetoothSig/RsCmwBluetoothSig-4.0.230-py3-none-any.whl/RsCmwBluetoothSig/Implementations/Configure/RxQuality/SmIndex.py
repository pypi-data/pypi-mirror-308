from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SmIndexCls:
	"""SmIndex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("smIndex", core, parent)

	def get_low_energy(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SMINdex:LENergy \n
		Snippet: value: bool = driver.configure.rxQuality.smIndex.get_low_energy() \n
		Selects the standard or stable modulation index. \n
			:return: mod_index_type: OFF | ON OFF: standard modulation index is used ON: stable modulation index is used
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SMINdex:LENergy?')
		return Conversions.str_to_bool(response)

	def set_low_energy(self, mod_index_type: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SMINdex:LENergy \n
		Snippet: driver.configure.rxQuality.smIndex.set_low_energy(mod_index_type = False) \n
		Selects the standard or stable modulation index. \n
			:param mod_index_type: OFF | ON OFF: standard modulation index is used ON: stable modulation index is used
		"""
		param = Conversions.bool_to_str(mod_index_type)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SMINdex:LENergy {param}')

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> float or bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:LENergy[:LE1M] \n
		Snippet: value: float or bool = driver.configure.rfSettings.dtx.sing.mindex.lowEnergy.get_le_1_m() \n
		No command help available \n
			:return: mod_index: (float or boolean) No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:LENergy:LE1M?')
		return Conversions.str_to_float_or_bool(response)

	def set_le_1_m(self, mod_index: float or bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:LENergy[:LE1M] \n
		Snippet: driver.configure.rfSettings.dtx.sing.mindex.lowEnergy.set_le_1_m(mod_index = 1.0) \n
		No command help available \n
			:param mod_index: (float or boolean) No help available
		"""
		param = Conversions.decimal_or_bool_value_to_str(mod_index)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:SING:MINDex:LENergy:LE1M {param}')

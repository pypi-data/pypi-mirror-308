from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> List[float or bool]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:LENergy[:LE1M] \n
		Snippet: value: List[float or bool] = driver.configure.rfSettings.dtx.stab.mindex.lowEnergy.get_le_1_m() \n
		No command help available \n
			:return: mod_index: (float or boolean items) No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX:STAB:MINDex:LENergy:LE1M?')
		return Conversions.str_to_float_or_bool_list(response)

from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CteCls:
	"""Cte commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cte", core, parent)

	def get_low_energy(self) -> List[int]:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AIDoverride:CTE:LENergy \n
		Snippet: value: List[int] = driver.configure.rfSettings.aidOverride.cte.get_low_energy() \n
		No command help available \n
			:return: antenna_id: No help available
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AIDoverride:CTE:LENergy?')
		return response

	def set_low_energy(self, antenna_id: List[int]) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AIDoverride:CTE:LENergy \n
		Snippet: driver.configure.rfSettings.aidOverride.cte.set_low_energy(antenna_id = [1, 2, 3]) \n
		No command help available \n
			:param antenna_id: No help available
		"""
		param = Conversions.list_to_csv_str(antenna_id)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:AIDoverride:CTE:LENergy {param}')

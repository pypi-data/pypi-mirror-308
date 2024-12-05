from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RxQualityCls:
	"""RxQuality commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rxQuality", core, parent)

	def set_per_show(self, per_show: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:RXQuality:PERShow \n
		Snippet: driver.diagnostic.rxQuality.set_per_show(per_show = False) \n
		No command help available \n
			:param per_show: No help available
		"""
		param = Conversions.bool_to_str(per_show)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:RXQuality:PERShow {param}')

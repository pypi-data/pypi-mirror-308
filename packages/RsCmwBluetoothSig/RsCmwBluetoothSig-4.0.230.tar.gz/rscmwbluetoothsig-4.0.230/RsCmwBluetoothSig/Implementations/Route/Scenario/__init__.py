from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScenarioCls:
	"""Scenario commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scenario", core, parent)

	@property
	def otRx(self):
		"""otRx commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_otRx'):
			from .OtRx import OtRxCls
			self._otRx = OtRxCls(self._core, self._cmd_group)
		return self._otRx

	# noinspection PyTypeChecker
	def get_state(self) -> enums.ConnectionState:
		"""SCPI: ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:STATe \n
		Snippet: value: enums.ConnectionState = driver.route.scenario.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('ROUTe:BLUetooth:SIGNaling<Instance>:SCENario:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.ConnectionState)

	def clone(self) -> 'ScenarioCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScenarioCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

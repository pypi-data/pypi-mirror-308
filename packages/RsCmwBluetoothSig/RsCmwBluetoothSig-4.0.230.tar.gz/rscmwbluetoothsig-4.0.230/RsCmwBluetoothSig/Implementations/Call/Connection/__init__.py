from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ConnectionCls:
	"""Connection commands group definition. 4 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("connection", core, parent)

	@property
	def check(self):
		"""check commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_check'):
			from .Check import CheckCls
			self._check = CheckCls(self._core, self._cmd_group)
		return self._check

	@property
	def action(self):
		"""action commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_action'):
			from .Action import ActionCls
			self._action = ActionCls(self._core, self._cmd_group)
		return self._action

	def get_aconnect(self) -> bool:
		"""SCPI: CALL:BLUetooth:SIGNaling<instance>:CONNection:ACONnect \n
		Snippet: value: bool = driver.call.connection.get_aconnect() \n
		No command help available \n
			:return: auto_ranging: No help available
		"""
		response = self._core.io.query_str('CALL:BLUetooth:SIGNaling<Instance>:CONNection:ACONnect?')
		return Conversions.str_to_bool(response)

	def set_aconnect(self, auto_ranging: bool) -> None:
		"""SCPI: CALL:BLUetooth:SIGNaling<instance>:CONNection:ACONnect \n
		Snippet: driver.call.connection.set_aconnect(auto_ranging = False) \n
		No command help available \n
			:param auto_ranging: No help available
		"""
		param = Conversions.bool_to_str(auto_ranging)
		self._core.io.write(f'CALL:BLUetooth:SIGNaling<Instance>:CONNection:ACONnect {param}')

	def clone(self) -> 'ConnectionCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ConnectionCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

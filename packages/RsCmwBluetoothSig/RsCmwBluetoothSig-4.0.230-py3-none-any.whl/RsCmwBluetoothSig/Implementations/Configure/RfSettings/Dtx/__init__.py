from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DtxCls:
	"""Dtx commands group definition. 129 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dtx", core, parent)

	@property
	def stab(self):
		"""stab commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_stab'):
			from .Stab import StabCls
			self._stab = StabCls(self._core, self._cmd_group)
		return self._stab

	@property
	def sing(self):
		"""sing commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sing'):
			from .Sing import SingCls
			self._sing = SingCls(self._core, self._cmd_group)
		return self._sing

	@property
	def modFrequency(self):
		"""modFrequency commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_modFrequency'):
			from .ModFrequency import ModFrequencyCls
			self._modFrequency = ModFrequencyCls(self._core, self._cmd_group)
		return self._modFrequency

	@property
	def mode(self):
		"""mode commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_mode'):
			from .Mode import ModeCls
			self._mode = ModeCls(self._core, self._cmd_group)
		return self._mode

	@property
	def mindex(self):
		"""mindex commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mindex'):
			from .Mindex import MindexCls
			self._mindex = MindexCls(self._core, self._cmd_group)
		return self._mindex

	def get_value(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX \n
		Snippet: value: bool = driver.configure.rfSettings.dtx.get_value() \n
		Enables/disables the dirty transmitter. \n
			:return: dtx_state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX?')
		return Conversions.str_to_bool(response)

	def set_value(self, dtx_state: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX \n
		Snippet: driver.configure.rfSettings.dtx.set_value(dtx_state = False) \n
		Enables/disables the dirty transmitter. \n
			:param dtx_state: OFF | ON
		"""
		param = Conversions.bool_to_str(dtx_state)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RFSettings:DTX {param}')

	def clone(self) -> 'DtxCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DtxCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

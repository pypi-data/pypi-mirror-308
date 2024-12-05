from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InquiryCls:
	"""Inquiry commands group definition. 8 total commands, 5 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inquiry", core, parent)

	@property
	def ptargets(self):
		"""ptargets commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptargets'):
			from .Ptargets import PtargetsCls
			self._ptargets = PtargetsCls(self._core, self._cmd_group)
		return self._ptargets

	@property
	def noResponses(self):
		"""noResponses commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_noResponses'):
			from .NoResponses import NoResponsesCls
			self._noResponses = NoResponsesCls(self._core, self._cmd_group)
		return self._noResponses

	@property
	def sinterval(self):
		"""sinterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinterval'):
			from .Sinterval import SintervalCls
			self._sinterval = SintervalCls(self._core, self._cmd_group)
		return self._sinterval

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Duration import DurationCls
			self._duration = DurationCls(self._core, self._cmd_group)
		return self._duration

	@property
	def swindow(self):
		"""swindow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swindow'):
			from .Swindow import SwindowCls
			self._swindow = SwindowCls(self._core, self._cmd_group)
		return self._swindow

	def get_ilength(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:ILENgth \n
		Snippet: value: int = driver.configure.connection.inquiry.get_ilength() \n
		Sets/gets the Inquiry_Length parameter, i.e. the total duration of the inquiry mode. \n
			:return: inquiry_length: numeric The inquiry length in units of 1.28 s Range: 1 to 24, Unit: 1.28 s
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:ILENgth?')
		return Conversions.str_to_int(response)

	def set_ilength(self, inquiry_length: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:ILENgth \n
		Snippet: driver.configure.connection.inquiry.set_ilength(inquiry_length = 1) \n
		Sets/gets the Inquiry_Length parameter, i.e. the total duration of the inquiry mode. \n
			:param inquiry_length: numeric The inquiry length in units of 1.28 s Range: 1 to 24, Unit: 1.28 s
		"""
		param = Conversions.decimal_value_to_str(inquiry_length)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:ILENgth {param}')

	def clone(self) -> 'InquiryCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InquiryCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

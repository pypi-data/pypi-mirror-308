from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PagingCls:
	"""Paging commands group definition. 5 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("paging", core, parent)

	@property
	def timeout(self):
		"""timeout commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_timeout'):
			from .Timeout import TimeoutCls
			self._timeout = TimeoutCls(self._core, self._cmd_group)
		return self._timeout

	@property
	def ptarget(self):
		"""ptarget commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ptarget'):
			from .Ptarget import PtargetCls
			self._ptarget = PtargetCls(self._core, self._cmd_group)
		return self._ptarget

	# noinspection PyTypeChecker
	def get_psr_mode(self) -> enums.PsrMode:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PSRMode \n
		Snippet: value: enums.PsrMode = driver.configure.connection.paging.get_psr_mode() \n
		Sets/gets the page scan repetition mode to be used for the default device (see method RsCmwBluetoothSig.Configure.
		Connection.BdAddress.eut) . \n
			:return: psr_mode: R0 | R1 | R2 Paging mode R0, R1, R2. Select the value according to the page scan repetition mode of the default device.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PSRMode?')
		return Conversions.str_to_scalar_enum(response, enums.PsrMode)

	def set_psr_mode(self, psr_mode: enums.PsrMode) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PSRMode \n
		Snippet: driver.configure.connection.paging.set_psr_mode(psr_mode = enums.PsrMode.R0) \n
		Sets/gets the page scan repetition mode to be used for the default device (see method RsCmwBluetoothSig.Configure.
		Connection.BdAddress.eut) . \n
			:param psr_mode: R0 | R1 | R2 Paging mode R0, R1, R2. Select the value according to the page scan repetition mode of the default device.
		"""
		param = Conversions.enum_scalar_to_str(psr_mode, enums.PsrMode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:PSRMode {param}')

	def clone(self) -> 'PagingCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PagingCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

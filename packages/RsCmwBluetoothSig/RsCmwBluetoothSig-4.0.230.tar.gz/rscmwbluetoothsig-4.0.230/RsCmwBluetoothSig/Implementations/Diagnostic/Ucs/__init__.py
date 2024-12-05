from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UcsCls:
	"""Ucs commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ucs", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	# noinspection PyTypeChecker
	def get_state(self) -> enums.LeDiagState:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:STATe \n
		Snippet: value: enums.LeDiagState = driver.diagnostic.ucs.get_state() \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.LeDiagState)

	def get_mode(self) -> bool:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:MODE \n
		Snippet: value: bool = driver.diagnostic.ucs.get_mode() \n
		No command help available \n
			:return: ucs_mode: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, ucs_mode: bool) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:MODE \n
		Snippet: driver.diagnostic.ucs.set_mode(ucs_mode = False) \n
		No command help available \n
			:param ucs_mode: No help available
		"""
		param = Conversions.bool_to_str(ucs_mode)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:MODE {param}')

	# noinspection PyTypeChecker
	def get_test_vector(self) -> enums.TestVector:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:TESTvector \n
		Snippet: value: enums.TestVector = driver.diagnostic.ucs.get_test_vector() \n
		No command help available \n
			:return: test_vector: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:TESTvector?')
		return Conversions.str_to_scalar_enum(response, enums.TestVector)

	def set_test_vector(self, test_vector: enums.TestVector) -> None:
		"""SCPI: DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:TESTvector \n
		Snippet: driver.diagnostic.ucs.set_test_vector(test_vector = enums.TestVector.INITstack) \n
		No command help available \n
			:param test_vector: No help available
		"""
		param = Conversions.enum_scalar_to_str(test_vector, enums.TestVector)
		self._core.io.write(f'DIAGnostic:BLUetooth:SIGNaling<Instance>:UCS:TESTvector {param}')

	def clone(self) -> 'UcsCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UcsCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

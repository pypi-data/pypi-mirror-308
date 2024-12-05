from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CheckCls:
	"""Check commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("check", core, parent)

	# noinspection PyTypeChecker
	def get_low_energy(self) -> enums.ConTestResult:
		"""SCPI: CALL:BLUetooth:SIGNaling<Instance>:CONNection:CHECk:LENergy \n
		Snippet: value: enums.ConTestResult = driver.call.connection.check.get_low_energy() \n
		Checks the LE connection via USB. \n
			:return: con_test_result: PASS | FAIL | TOUT | NRUN Result: passed, failed, timeout, not running
		"""
		response = self._core.io.query_str('CALL:BLUetooth:SIGNaling<Instance>:CONNection:CHECk:LENergy?')
		return Conversions.str_to_scalar_enum(response, enums.ConTestResult)

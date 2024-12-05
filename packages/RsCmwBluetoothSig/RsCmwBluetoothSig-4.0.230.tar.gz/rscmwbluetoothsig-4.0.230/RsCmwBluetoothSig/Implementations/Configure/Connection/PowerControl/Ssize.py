from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SsizeCls:
	"""Ssize commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ssize", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:SSIZe:LESignaling \n
		Snippet: value: int = driver.configure.connection.powerControl.ssize.get_le_signaling() \n
		Sets the step size for increasing / decreasing the DUT's TX power. See also method RsCmwBluetoothSig.Configure.Connection.
		PowerControl.Step.Action.leSignaling. \n
			:return: stepsize: numeric Range: 0 dB to 8 dB
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:SSIZe:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, stepsize: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:SSIZe:LESignaling \n
		Snippet: driver.configure.connection.powerControl.ssize.set_le_signaling(stepsize = 1) \n
		Sets the step size for increasing / decreasing the DUT's TX power. See also method RsCmwBluetoothSig.Configure.Connection.
		PowerControl.Step.Action.leSignaling. \n
			:param stepsize: numeric Range: 0 dB to 8 dB
		"""
		param = Conversions.decimal_value_to_str(stepsize)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:SSIZe:LESignaling {param}')

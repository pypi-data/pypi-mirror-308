from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ActionCls:
	"""Action commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("action", core, parent)

	def set_le_signaling(self, pcontrol: enums.PowerControl) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion:LESignaling \n
		Snippet: driver.configure.connection.powerControl.step.action.set_le_signaling(pcontrol = enums.PowerControl.DOWN) \n
		Sends a command to the DUT to increase/decrease power by the defined step size. See also method RsCmwBluetoothSig.
		Configure.Connection.PowerControl.Ssize.leSignaling. \n
			:param pcontrol: UP | DOWN | MAX One step up, one step down, command to maximum DUT TX power
		"""
		param = Conversions.enum_scalar_to_str(pcontrol, enums.PowerControl)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion:LESignaling {param}')

	def set_value(self, pcontrol: enums.PowerControl) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion \n
		Snippet: driver.configure.connection.powerControl.step.action.set_value(pcontrol = enums.PowerControl.DOWN) \n
		Sends a command to the EUT to increase/decrease power. \n
			:param pcontrol: UP | DOWN | MAX One step up, one step down, command to maximum EUT power
		"""
		param = Conversions.enum_scalar_to_str(pcontrol, enums.PowerControl)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PCONtrol:STEP:ACTion {param}')

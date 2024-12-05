from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PperiodCls:
	"""Pperiod commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pperiod", core, parent)

	def get_minimum(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PPERiod:MINimum \n
		Snippet: value: bool = driver.configure.connection.pperiod.get_minimum() \n
		Enables a minimum poll period. To prevent the simultaneous transmission from central and peripheral device, the minimum
		poll period for an x-DHn packet type (n = 1, 3, 5) is automatically set to n+1 slots. \n
			:return: poll_period_min: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PPERiod:MINimum?')
		return Conversions.str_to_bool(response)

	def set_minimum(self, poll_period_min: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PPERiod:MINimum \n
		Snippet: driver.configure.connection.pperiod.set_minimum(poll_period_min = False) \n
		Enables a minimum poll period. To prevent the simultaneous transmission from central and peripheral device, the minimum
		poll period for an x-DHn packet type (n = 1, 3, 5) is automatically set to n+1 slots. \n
			:param poll_period_min: OFF | ON
		"""
		param = Conversions.bool_to_str(poll_period_min)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PPERiod:MINimum {param}')

	def get_value(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PPERiod \n
		Snippet: value: int = driver.configure.connection.pperiod.get_value() \n
		Defines how often the R&S CMW transmitts a poll packet. If the set poll period is too small for the selected packet type
		(for x-DH1, x-DH3, or x-DH5) , it is automatically changed to 2, 4, or 6 slots. X = 1, 2, 3. \n
			:return: poll_period: numeric Range: x-DH1: 1 to 127, x-DH3: 2 to 127, x-DH5: 3 to 127 , Unit: Unit corresponds to two slots
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PPERiod?')
		return Conversions.str_to_int(response)

	def set_value(self, poll_period: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PPERiod \n
		Snippet: driver.configure.connection.pperiod.set_value(poll_period = 1) \n
		Defines how often the R&S CMW transmitts a poll packet. If the set poll period is too small for the selected packet type
		(for x-DH1, x-DH3, or x-DH5) , it is automatically changed to 2, 4, or 6 slots. X = 1, 2, 3. \n
			:param poll_period: numeric Range: x-DH1: 1 to 127, x-DH3: 2 to 127, x-DH5: 3 to 127 , Unit: Unit corresponds to two slots
		"""
		param = Conversions.decimal_value_to_str(poll_period)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PPERiod {param}')

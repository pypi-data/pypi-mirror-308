from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NoResponsesCls:
	"""NoResponses commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("noResponses", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:NOResponses:LESignaling \n
		Snippet: value: int = driver.configure.connection.inquiry.noResponses.get_le_signaling() \n
		Specifies the maximum number of responses recorded during an inquiry. \n
			:return: number_responses: numeric Range: 1 to 100
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:NOResponses:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, number_responses: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:NOResponses:LESignaling \n
		Snippet: driver.configure.connection.inquiry.noResponses.set_le_signaling(number_responses = 1) \n
		Specifies the maximum number of responses recorded during an inquiry. \n
			:param number_responses: numeric Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(number_responses)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:NOResponses:LESignaling {param}')

	def get_value(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:NOResponses \n
		Snippet: value: int = driver.configure.connection.inquiry.noResponses.get_value() \n
		Sets/gets the maximum number of responses recorded during an inquiry. \n
			:return: number_responses: numeric The maximum number of responses, where 0 means 'unlimited'. Range: 0 to 12
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:NOResponses?')
		return Conversions.str_to_int(response)

	def set_value(self, number_responses: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:NOResponses \n
		Snippet: driver.configure.connection.inquiry.noResponses.set_value(number_responses = 1) \n
		Sets/gets the maximum number of responses recorded during an inquiry. \n
			:param number_responses: numeric The maximum number of responses, where 0 means 'unlimited'. Range: 0 to 12
		"""
		param = Conversions.decimal_value_to_str(number_responses)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:NOResponses {param}')

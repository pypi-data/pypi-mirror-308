from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SynWordCls:
	"""SynWord commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("synWord", core, parent)

	def get_low_energy(self) -> str:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SYNWord:LENergy \n
		Snippet: value: str = driver.configure.connection.synWord.get_low_energy() \n
		Specifies the synchronization word used for LE connection. \n
			:return: synch_word: hex Range: #H0 to #HFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SYNWord:LENergy?')
		return trim_str_response(response)

	def set_low_energy(self, synch_word: str) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SYNWord:LENergy \n
		Snippet: driver.configure.connection.synWord.set_low_energy(synch_word = rawAbc) \n
		Specifies the synchronization word used for LE connection. \n
			:param synch_word: hex Range: #H0 to #HFFFFFFFF
		"""
		param = Conversions.value_to_str(synch_word)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SYNWord:LENergy {param}')

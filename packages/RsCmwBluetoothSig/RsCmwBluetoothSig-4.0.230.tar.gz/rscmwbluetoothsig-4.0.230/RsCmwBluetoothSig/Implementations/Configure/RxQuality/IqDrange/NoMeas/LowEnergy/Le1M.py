from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le1MCls:
	"""Le1M commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le1M", core, parent)

	def get_a_0_reference(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A0Reference \n
		Snippet: value: int = driver.configure.rxQuality.iqDrange.noMeas.lowEnergy.le1M.get_a_0_reference() \n
		Defines the number of measurements per measurement cycle for the specified antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		antenna (...:A1NReference) , and optional third and fourth antennas are available. \n
			:return: no_of_meas: numeric Range: 0 to 30E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A0Reference?')
		return Conversions.str_to_int(response)

	def set_a_0_reference(self, no_of_meas: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A0Reference \n
		Snippet: driver.configure.rxQuality.iqDrange.noMeas.lowEnergy.le1M.set_a_0_reference(no_of_meas = 1) \n
		Defines the number of measurements per measurement cycle for the specified antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		antenna (...:A1NReference) , and optional third and fourth antennas are available. \n
			:param no_of_meas: numeric Range: 0 to 30E+3
		"""
		param = Conversions.decimal_value_to_str(no_of_meas)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A0Reference {param}')

	def get_a_1_nreference(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A1NReference \n
		Snippet: value: int = driver.configure.rxQuality.iqDrange.noMeas.lowEnergy.le1M.get_a_1_nreference() \n
		Defines the number of measurements per measurement cycle for the specified antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		antenna (...:A1NReference) , and optional third and fourth antennas are available. \n
			:return: no_of_meas: numeric Range: 0 to 30E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A1NReference?')
		return Conversions.str_to_int(response)

	def set_a_1_nreference(self, no_of_meas: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A1NReference \n
		Snippet: driver.configure.rxQuality.iqDrange.noMeas.lowEnergy.le1M.set_a_1_nreference(no_of_meas = 1) \n
		Defines the number of measurements per measurement cycle for the specified antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		antenna (...:A1NReference) , and optional third and fourth antennas are available. \n
			:param no_of_meas: numeric Range: 0 to 30E+3
		"""
		param = Conversions.decimal_value_to_str(no_of_meas)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A1NReference {param}')

	def get_a_2_nreference(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A2NReference \n
		Snippet: value: int = driver.configure.rxQuality.iqDrange.noMeas.lowEnergy.le1M.get_a_2_nreference() \n
		Defines the number of measurements per measurement cycle for the specified antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		antenna (...:A1NReference) , and optional third and fourth antennas are available. \n
			:return: no_of_meas: numeric Range: 0 to 30E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A2NReference?')
		return Conversions.str_to_int(response)

	def set_a_2_nreference(self, no_of_meas: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A2NReference \n
		Snippet: driver.configure.rxQuality.iqDrange.noMeas.lowEnergy.le1M.set_a_2_nreference(no_of_meas = 1) \n
		Defines the number of measurements per measurement cycle for the specified antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		antenna (...:A1NReference) , and optional third and fourth antennas are available. \n
			:param no_of_meas: numeric Range: 0 to 30E+3
		"""
		param = Conversions.decimal_value_to_str(no_of_meas)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A2NReference {param}')

	def get_a_3_nreference(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A3NReference \n
		Snippet: value: int = driver.configure.rxQuality.iqDrange.noMeas.lowEnergy.le1M.get_a_3_nreference() \n
		Defines the number of measurements per measurement cycle for the specified antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		antenna (...:A1NReference) , and optional third and fourth antennas are available. \n
			:return: no_of_meas: numeric Range: 0 to 30E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A3NReference?')
		return Conversions.str_to_int(response)

	def set_a_3_nreference(self, no_of_meas: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A3NReference \n
		Snippet: driver.configure.rxQuality.iqDrange.noMeas.lowEnergy.le1M.set_a_3_nreference(no_of_meas = 1) \n
		Defines the number of measurements per measurement cycle for the specified antenna. Commands for uncoded LE 1M PHY (..
		:LE1M..) and LE 2M PHY (..:LE2M..) are available. Commands for reference antenna (...:A0Reference) , mandatory second
		antenna (...:A1NReference) , and optional third and fourth antennas are available. \n
			:param no_of_meas: numeric Range: 0 to 30E+3
		"""
		param = Conversions.decimal_value_to_str(no_of_meas)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQDRange:NOMeas:LENergy:LE1M:A3NReference {param}')

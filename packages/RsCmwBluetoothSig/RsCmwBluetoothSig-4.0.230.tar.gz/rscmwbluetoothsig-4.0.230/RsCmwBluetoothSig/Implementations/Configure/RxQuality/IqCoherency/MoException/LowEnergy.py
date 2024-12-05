from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:MOEXception:LENergy:LE1M \n
		Snippet: value: bool = driver.configure.rxQuality.iqCoherency.moException.lowEnergy.get_le_1_m() \n
		Specifies whether measurement results that the R&S CMW identifies as faulty or inaccurate are rejected. Commands for
		uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: meas_on_exception: OFF | ON OFF: Faulty results are rejected ON: Results are never rejected
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:MOEXception:LENergy:LE1M?')
		return Conversions.str_to_bool(response)

	def set_le_1_m(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:MOEXception:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.iqCoherency.moException.lowEnergy.set_le_1_m(meas_on_exception = False) \n
		Specifies whether measurement results that the R&S CMW identifies as faulty or inaccurate are rejected. Commands for
		uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param meas_on_exception: OFF | ON OFF: Faulty results are rejected ON: Results are never rejected
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:MOEXception:LENergy:LE1M {param}')

	def get_le_2_m(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:MOEXception:LENergy:LE2M \n
		Snippet: value: bool = driver.configure.rxQuality.iqCoherency.moException.lowEnergy.get_le_2_m() \n
		Specifies whether measurement results that the R&S CMW identifies as faulty or inaccurate are rejected. Commands for
		uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:return: meas_on_exception: OFF | ON OFF: Faulty results are rejected ON: Results are never rejected
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:MOEXception:LENergy:LE2M?')
		return Conversions.str_to_bool(response)

	def set_le_2_m(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:MOEXception:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.iqCoherency.moException.lowEnergy.set_le_2_m(meas_on_exception = False) \n
		Specifies whether measurement results that the R&S CMW identifies as faulty or inaccurate are rejected. Commands for
		uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..) are available. \n
			:param meas_on_exception: OFF | ON OFF: Faulty results are rejected ON: Results are never rejected
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:IQCoherency:MOEXception:LENergy:LE2M {param}')

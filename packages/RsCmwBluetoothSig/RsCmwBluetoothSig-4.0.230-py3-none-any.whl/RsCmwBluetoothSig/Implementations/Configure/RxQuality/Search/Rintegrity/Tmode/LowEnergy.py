from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LE1M \n
		Snippet: value: bool = driver.configure.rxQuality.search.rintegrity.tmode.lowEnergy.get_le_1_m() \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW. Commands for uncoded LE 1M PHY (..:LE1M..
		) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LE1M?')
		return Conversions.str_to_bool(response)

	def set_le_1_m(self, report_integrity: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.search.rintegrity.tmode.lowEnergy.set_le_1_m(report_integrity = False) \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW. Commands for uncoded LE 1M PHY (..:LE1M..
		) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		param = Conversions.bool_to_str(report_integrity)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LE1M {param}')

	def get_le_2_m(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LE2M \n
		Snippet: value: bool = driver.configure.rxQuality.search.rintegrity.tmode.lowEnergy.get_le_2_m() \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW. Commands for uncoded LE 1M PHY (..:LE1M..
		) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LE2M?')
		return Conversions.str_to_bool(response)

	def set_le_2_m(self, report_integrity: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.search.rintegrity.tmode.lowEnergy.set_le_2_m(report_integrity = False) \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW. Commands for uncoded LE 1M PHY (..:LE1M..
		) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		param = Conversions.bool_to_str(report_integrity)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LE2M {param}')

	def get_lrange(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LRANge \n
		Snippet: value: bool = driver.configure.rxQuality.search.rintegrity.tmode.lowEnergy.get_lrange() \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW. Commands for uncoded LE 1M PHY (..:LE1M..
		) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:return: report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LRANge?')
		return Conversions.str_to_bool(response)

	def set_lrange(self, report_integrity: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LRANge \n
		Snippet: driver.configure.rxQuality.search.rintegrity.tmode.lowEnergy.set_lrange(report_integrity = False) \n
		Sets the ratio of the test packets with correct CRC transmitted by the R&S CMW. Commands for uncoded LE 1M PHY (..:LE1M..
		) , LE 2M PHY (..:LE2M..) , and LE coded PHY (..:LRANge..) are available. \n
			:param report_integrity: OFF | ON OFF: 100% of packets generated with correct CRC ON: 50% of packets generated with correct CRC
		"""
		param = Conversions.bool_to_str(report_integrity)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:SEARch:RINTegrity:TMODe:LENergy:LRANge {param}')

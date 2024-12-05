from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Le2MCls:
	"""Le2M commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("le2M", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.CtePacketType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:LENergy:LE2M:TYPE \n
		Snippet: value: enums.CtePacketType = driver.configure.inputSignal.cte.lowEnergy.le2M.get_type_py() \n
		Specifies the CTE slot type for LE with CTE. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..
		) are available. \n
			:return: cte_type: AOAus | AOD1us | AOD2us | AOA2us | AOA1us AOD1us, AOD2us: CTE type angle of departure, 1 us or 2 us slot AOAus, AOA2us: CTE type angle of arrival, 2 us slot AOA1us: CTE type angle of arrival, 1 us slot
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:LENergy:LE2M:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.CtePacketType)

	def set_type_py(self, cte_type: enums.CtePacketType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:LENergy:LE2M:TYPE \n
		Snippet: driver.configure.inputSignal.cte.lowEnergy.le2M.set_type_py(cte_type = enums.CtePacketType.AOA1us) \n
		Specifies the CTE slot type for LE with CTE. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..
		) are available. \n
			:param cte_type: AOAus | AOD1us | AOD2us | AOA2us | AOA1us AOD1us, AOD2us: CTE type angle of departure, 1 us or 2 us slot AOAus, AOA2us: CTE type angle of arrival, 2 us slot AOA1us: CTE type angle of arrival, 1 us slot
		"""
		param = Conversions.enum_scalar_to_str(cte_type, enums.CtePacketType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:LENergy:LE2M:TYPE {param}')

	def get_units(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:LENergy:LE2M:UNITs \n
		Snippet: value: int = driver.configure.inputSignal.cte.lowEnergy.le2M.get_units() \n
		Specifies the number of CTE units for LE with CTE. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..
		) are available. \n
			:return: cte_units: numeric Range: 2 to 20
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:LENergy:LE2M:UNITs?')
		return Conversions.str_to_int(response)

	def set_units(self, cte_units: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:LENergy:LE2M:UNITs \n
		Snippet: driver.configure.inputSignal.cte.lowEnergy.le2M.set_units(cte_units = 1) \n
		Specifies the number of CTE units for LE with CTE. Commands for uncoded LE 1M PHY (..:LE1M..) and LE 2M PHY (..:LE2M..
		) are available. \n
			:param cte_units: numeric Range: 2 to 20
		"""
		param = Conversions.decimal_value_to_str(cte_units)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:LENergy:LE2M:UNITs {param}')

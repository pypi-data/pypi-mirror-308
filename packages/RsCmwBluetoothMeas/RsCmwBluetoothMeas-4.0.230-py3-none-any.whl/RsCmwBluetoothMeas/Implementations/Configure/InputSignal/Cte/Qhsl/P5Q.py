from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class P5QCls:
	"""P5Q commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("p5Q", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.CtePacketType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:QHSL:P5Q:TYPE \n
		Snippet: value: enums.CtePacketType = driver.configure.inputSignal.cte.qhsl.p5Q.get_type_py() \n
		No command help available \n
			:return: cte_type: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:QHSL:P5Q:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.CtePacketType)

	def set_type_py(self, cte_type: enums.CtePacketType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:QHSL:P5Q:TYPE \n
		Snippet: driver.configure.inputSignal.cte.qhsl.p5Q.set_type_py(cte_type = enums.CtePacketType.AOA1us) \n
		No command help available \n
			:param cte_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(cte_type, enums.CtePacketType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:QHSL:P5Q:TYPE {param}')

	def get_units(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:QHSL:P5Q:UNITs \n
		Snippet: value: int = driver.configure.inputSignal.cte.qhsl.p5Q.get_units() \n
		No command help available \n
			:return: cte_units: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:QHSL:P5Q:UNITs?')
		return Conversions.str_to_int(response)

	def set_units(self, cte_units: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:QHSL:P5Q:UNITs \n
		Snippet: driver.configure.inputSignal.cte.qhsl.p5Q.set_units(cte_units = 1) \n
		No command help available \n
			:param cte_units: No help available
		"""
		param = Conversions.decimal_value_to_str(cte_units)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:ISIGnal:CTE:QHSL:P5Q:UNITs {param}')

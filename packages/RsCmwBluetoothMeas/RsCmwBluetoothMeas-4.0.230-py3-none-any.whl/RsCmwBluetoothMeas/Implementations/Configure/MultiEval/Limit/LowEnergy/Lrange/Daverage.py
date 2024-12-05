from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DaverageCls:
	"""Daverage commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("daverage", core, parent)

	def set(self, freq_dev_f_1_lower: float, freq_dev_f_1_upper: float, freq_dev_f_1_enable: List[bool]) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DAVerage \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.lrange.daverage.set(freq_dev_f_1_lower = 1.0, freq_dev_f_1_upper = 1.0, freq_dev_f_1_enable = [True, False, True]) \n
		Defines the lower and upper deltaf1 frequency deviation limits for LE coded PHY. The mnemonics DAVerage, DMINimum,
		DMAXimum distinguish average, minimum and maximum frequency deviations. \n
			:param freq_dev_f_1_lower: numeric Range: 0 Hz to 500 kHz, Unit: Hz
			:param freq_dev_f_1_upper: numeric Range: 0 Hz to 500 kHz, Unit: Hz
			:param freq_dev_f_1_enable: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('freq_dev_f_1_lower', freq_dev_f_1_lower, DataType.Float), ArgSingle('freq_dev_f_1_upper', freq_dev_f_1_upper, DataType.Float), ArgSingle('freq_dev_f_1_enable', freq_dev_f_1_enable, DataType.BooleanList, None, False, False, 4))
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DAVerage {param}'.rstrip())

	# noinspection PyTypeChecker
	class DaverageStruct(StructBase):
		"""Response structure. Fields: \n
			- Freq_Dev_F_1_Lower: float: numeric Range: 0 Hz to 500 kHz, Unit: Hz
			- Freq_Dev_F_1_Upper: float: numeric Range: 0 Hz to 500 kHz, Unit: Hz
			- Freq_Dev_F_1_Enable: List[bool]: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq_Dev_F_1_Lower'),
			ArgStruct.scalar_float('Freq_Dev_F_1_Upper'),
			ArgStruct('Freq_Dev_F_1_Enable', DataType.BooleanList, None, False, False, 4)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq_Dev_F_1_Lower: float = None
			self.Freq_Dev_F_1_Upper: float = None
			self.Freq_Dev_F_1_Enable: List[bool] = None

	def get(self) -> DaverageStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DAVerage \n
		Snippet: value: DaverageStruct = driver.configure.multiEval.limit.lowEnergy.lrange.daverage.get() \n
		Defines the lower and upper deltaf1 frequency deviation limits for LE coded PHY. The mnemonics DAVerage, DMINimum,
		DMAXimum distinguish average, minimum and maximum frequency deviations. \n
			:return: structure: for return value, see the help for DaverageStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:LRANge:DAVerage?', self.__class__.DaverageStruct())

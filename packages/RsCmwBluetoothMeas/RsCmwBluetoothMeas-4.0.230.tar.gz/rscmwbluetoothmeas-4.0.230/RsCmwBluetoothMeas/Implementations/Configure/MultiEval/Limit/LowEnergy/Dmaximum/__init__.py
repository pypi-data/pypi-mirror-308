from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DmaximumCls:
	"""Dmaximum commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmaximum", core, parent)

	@property
	def df2S(self):
		"""df2S commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_df2S'):
			from .Df2S import Df2SCls
			self._df2S = Df2SCls(self._core, self._cmd_group)
		return self._df2S

	def set(self, freq_dev_f_1_lower: float, freq_dev_f_1_upper: float, freq_dev_f_1_enable: List[bool]) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum \n
		Snippet: driver.configure.multiEval.limit.lowEnergy.dmaximum.set(freq_dev_f_1_lower = 1.0, freq_dev_f_1_upper = 1.0, freq_dev_f_1_enable = [True, False, True]) \n
		Defines the lower and upper deltaf1 frequency deviation limits for LE 1M PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:param freq_dev_f_1_lower: numeric Range: 0 Hz to 500 kHz, Unit: Hz
			:param freq_dev_f_1_upper: numeric Range: 0 Hz to 500 kHz, Unit: Hz
			:param freq_dev_f_1_enable: OFF | ON Disable or enable limits for current, average, maximum, and minimum results (4 values)
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('freq_dev_f_1_lower', freq_dev_f_1_lower, DataType.Float), ArgSingle('freq_dev_f_1_upper', freq_dev_f_1_upper, DataType.Float), ArgSingle('freq_dev_f_1_enable', freq_dev_f_1_enable, DataType.BooleanList, None, False, False, 4))
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum {param}'.rstrip())

	# noinspection PyTypeChecker
	class DmaximumStruct(StructBase):
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

	def get(self) -> DmaximumStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum \n
		Snippet: value: DmaximumStruct = driver.configure.multiEval.limit.lowEnergy.dmaximum.get() \n
		Defines the lower and upper deltaf1 frequency deviation limits for LE 1M PHY. The mnemonics DAVerage, DMINimum, DMAXimum
		distinguish average, minimum and maximum frequency deviations. \n
			:return: structure: for return value, see the help for DmaximumStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:LENergy:DMAXimum?', self.__class__.DmaximumStruct())

	def clone(self) -> 'DmaximumCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DmaximumCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

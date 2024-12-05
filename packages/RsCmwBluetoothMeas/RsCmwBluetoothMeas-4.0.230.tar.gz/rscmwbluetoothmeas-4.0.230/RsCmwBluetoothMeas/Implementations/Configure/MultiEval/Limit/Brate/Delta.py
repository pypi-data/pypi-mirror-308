from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeltaCls:
	"""Delta commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delta", core, parent)

	def set(self, delta_f_2_p_99_p_9: float, delta_f_2_p_99_enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DELTa \n
		Snippet: driver.configure.multiEval.limit.brate.delta.set(delta_f_2_p_99_p_9 = 1.0, delta_f_2_p_99_enable = False) \n
		It defines the lower limit for the frequency deviation deltaf2 that must be exceeded by 99.9% of the measured bits. \n
			:param delta_f_2_p_99_p_9: numeric Range: 100 kHz to 200 kHz, Unit: Hz
			:param delta_f_2_p_99_enable: OFF | ON
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('delta_f_2_p_99_p_9', delta_f_2_p_99_p_9, DataType.Float), ArgSingle('delta_f_2_p_99_enable', delta_f_2_p_99_enable, DataType.Boolean))
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DELTa {param}'.rstrip())

	# noinspection PyTypeChecker
	class DeltaStruct(StructBase):
		"""Response structure. Fields: \n
			- Delta_F_2_P_99_P_9: float: numeric Range: 100 kHz to 200 kHz, Unit: Hz
			- Delta_F_2_P_99_Enable: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_float('Delta_F_2_P_99_P_9'),
			ArgStruct.scalar_bool('Delta_F_2_P_99_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Delta_F_2_P_99_P_9: float = None
			self.Delta_F_2_P_99_Enable: bool = None

	def get(self) -> DeltaStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DELTa \n
		Snippet: value: DeltaStruct = driver.configure.multiEval.limit.brate.delta.get() \n
		It defines the lower limit for the frequency deviation deltaf2 that must be exceeded by 99.9% of the measured bits. \n
			:return: structure: for return value, see the help for DeltaStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:DELTa?', self.__class__.DeltaStruct())

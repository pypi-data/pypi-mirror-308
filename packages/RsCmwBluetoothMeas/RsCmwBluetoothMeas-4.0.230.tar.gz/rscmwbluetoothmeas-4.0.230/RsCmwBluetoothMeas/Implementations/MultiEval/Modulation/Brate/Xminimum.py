from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class XminimumCls:
	"""Xminimum commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("xminimum", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float or bool: float Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#Modulation CMDLINKRESOLVED]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Delta_F_299_P_9: float or bool: float Frequency deviation value deltaf2 above which 99.9% of all measured deltaf2 values occur Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Accuracy: float or bool: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Drift: float or bool: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Max_Drift: float or bool: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz/50 us
			- Freq_Dev_Avg_F_1: float or bool: No parameter help available
			- Freq_Dev_Min_F_1: float or bool: No parameter help available
			- Freq_Dev_Max_F_1: float or bool: No parameter help available
			- Freq_Dev_Avg_F_2: float or bool: No parameter help available
			- Freq_Dev_Min_F_2: float or bool: No parameter help available
			- Freq_Dev_Max_F_2: float or bool: No parameter help available
			- Nominal_Power: float or bool: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Mod_Ratio: enums.ResultStatus2: float Modulation ratio deltaf2 avg / deltaf1 avg Range: 0 to 1"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Out_Of_Tol'),
			ArgStruct.scalar_float_ext('Delta_F_299_P_9'),
			ArgStruct.scalar_float_ext('Freq_Accuracy'),
			ArgStruct.scalar_float_ext('Freq_Drift'),
			ArgStruct.scalar_float_ext('Max_Drift'),
			ArgStruct.scalar_float_ext('Freq_Dev_Avg_F_1'),
			ArgStruct.scalar_float_ext('Freq_Dev_Min_F_1'),
			ArgStruct.scalar_float_ext('Freq_Dev_Max_F_1'),
			ArgStruct.scalar_float_ext('Freq_Dev_Avg_F_2'),
			ArgStruct.scalar_float_ext('Freq_Dev_Min_F_2'),
			ArgStruct.scalar_float_ext('Freq_Dev_Max_F_2'),
			ArgStruct.scalar_float_ext('Nominal_Power'),
			ArgStruct.scalar_enum('Mod_Ratio', enums.ResultStatus2)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float or bool = None
			self.Delta_F_299_P_9: float or bool = None
			self.Freq_Accuracy: float or bool = None
			self.Freq_Drift: float or bool = None
			self.Max_Drift: float or bool = None
			self.Freq_Dev_Avg_F_1: float or bool = None
			self.Freq_Dev_Min_F_1: float or bool = None
			self.Freq_Dev_Max_F_1: float or bool = None
			self.Freq_Dev_Avg_F_2: float or bool = None
			self.Freq_Dev_Min_F_2: float or bool = None
			self.Freq_Dev_Max_F_2: float or bool = None
			self.Nominal_Power: float or bool = None
			self.Mod_Ratio: enums.ResultStatus2 = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:BRATe:XMINimum \n
		Snippet: value: CalculateStruct = driver.multiEval.modulation.brate.xminimum.calculate() \n
		Returns the current, average, absolute min (xmin) , absolute max (xmax) , and max modulation results for BR packets. The
		values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:BRATe:XMINimum?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Out_Of_Tol: float: float Out of tolerance result, i.e. the percentage of measurement intervals of the statistic count ([CMDLINKRESOLVED Configure.MultiEval.Scount#Modulation CMDLINKRESOLVED]) exceeding the specified limits. Range: 0 % to 100 %, Unit: %
			- Delta_F_299_P_9: float: float Frequency deviation value deltaf2 above which 99.9% of all measured deltaf2 values occur Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Accuracy: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Freq_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz
			- Max_Drift: float: float Range: -0.99999 MHz to 0.99999 MHz, Unit: Hz/50 us
			- Freq_Dev_Avg_F_1: float: No parameter help available
			- Freq_Dev_Min_F_1: float: No parameter help available
			- Freq_Dev_Max_F_1: float: No parameter help available
			- Freq_Dev_Avg_F_2: float: No parameter help available
			- Freq_Dev_Min_F_2: float: No parameter help available
			- Freq_Dev_Max_F_2: float: No parameter help available
			- Nominal_Power: float: float Average power during the carrier-on state Range: -99.99 dBm to 99.99 dBm, Unit: dBm
			- Mod_Ratio: float: float Modulation ratio deltaf2 avg / deltaf1 avg Range: 0 to 1"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Out_Of_Tol'),
			ArgStruct.scalar_float('Delta_F_299_P_9'),
			ArgStruct.scalar_float('Freq_Accuracy'),
			ArgStruct.scalar_float('Freq_Drift'),
			ArgStruct.scalar_float('Max_Drift'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_1'),
			ArgStruct.scalar_float('Freq_Dev_Avg_F_2'),
			ArgStruct.scalar_float('Freq_Dev_Min_F_2'),
			ArgStruct.scalar_float('Freq_Dev_Max_F_2'),
			ArgStruct.scalar_float('Nominal_Power'),
			ArgStruct.scalar_float('Mod_Ratio')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Out_Of_Tol: float = None
			self.Delta_F_299_P_9: float = None
			self.Freq_Accuracy: float = None
			self.Freq_Drift: float = None
			self.Max_Drift: float = None
			self.Freq_Dev_Avg_F_1: float = None
			self.Freq_Dev_Min_F_1: float = None
			self.Freq_Dev_Max_F_1: float = None
			self.Freq_Dev_Avg_F_2: float = None
			self.Freq_Dev_Min_F_2: float = None
			self.Freq_Dev_Max_F_2: float = None
			self.Nominal_Power: float = None
			self.Mod_Ratio: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:BRATe:XMINimum \n
		Snippet: value: ResultData = driver.multiEval.modulation.brate.xminimum.fetch() \n
		Returns the current, average, absolute min (xmin) , absolute max (xmax) , and max modulation results for BR packets. The
		values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:BRATe:XMINimum?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:BRATe:XMINimum \n
		Snippet: value: ResultData = driver.multiEval.modulation.brate.xminimum.read() \n
		Returns the current, average, absolute min (xmin) , absolute max (xmax) , and max modulation results for BR packets. The
		values described below are returned by FETCh and READ commands. CALCulate commands return limit check results instead,
		one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:MEValuation:MODulation:BRATe:XMINimum?', self.__class__.ResultData())

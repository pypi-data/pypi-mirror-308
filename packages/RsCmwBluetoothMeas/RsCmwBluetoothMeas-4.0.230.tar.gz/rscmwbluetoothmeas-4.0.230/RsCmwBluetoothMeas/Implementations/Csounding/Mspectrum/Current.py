from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CurrentCls:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Peak_Emission: float: float Peak power within the CS signal Range: -128 dBm to 50 dBm
			- Fl: float: float The smallest frequency at which the transmit power drops the configured threshold value below the peak power. Range: -1.5 MHz to 0 MHz
			- Fh: float: float The highest frequency at which the transmit power drops the configured threshold value below the peak power. Range: 0 MHz to 1.5 MHz
			- Fl_Minus_Fh: float: float The difference | fL - fH | Range: 0 MHz to 3 MHz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Peak_Emission'),
			ArgStruct.scalar_float('Fl'),
			ArgStruct.scalar_float('Fh'),
			ArgStruct.scalar_float('Fl_Minus_Fh')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Peak_Emission: float = None
			self.Fl: float = None
			self.Fh: float = None
			self.Fl_Minus_Fh: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:BLUetooth:MEASurement<Instance>:CSOunding:MSPectrum:CURRent \n
		Snippet: value: ResultData = driver.csounding.mspectrum.current.read() \n
		Returns the modulation spectrum results The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:BLUetooth:MEASurement<Instance>:CSOunding:MSPectrum:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:BLUetooth:MEASurement<Instance>:CSOunding:MSPectrum:CURRent \n
		Snippet: value: ResultData = driver.csounding.mspectrum.current.fetch() \n
		Returns the modulation spectrum results The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:BLUetooth:MEASurement<Instance>:CSOunding:MSPectrum:CURRent?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: decimal 'Reliability indicator'
			- Peak_Emission: float or bool: float Peak power within the CS signal Range: -128 dBm to 50 dBm
			- Fl: float or bool: float The smallest frequency at which the transmit power drops the configured threshold value below the peak power. Range: -1.5 MHz to 0 MHz
			- Fh: float or bool: float The highest frequency at which the transmit power drops the configured threshold value below the peak power. Range: 0 MHz to 1.5 MHz
			- Fl_Minus_Fh: float or bool: float The difference | fL - fH | Range: 0 MHz to 3 MHz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float_ext('Peak_Emission'),
			ArgStruct.scalar_float_ext('Fl'),
			ArgStruct.scalar_float_ext('Fh'),
			ArgStruct.scalar_float_ext('Fl_Minus_Fh')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Peak_Emission: float or bool = None
			self.Fl: float or bool = None
			self.Fh: float or bool = None
			self.Fl_Minus_Fh: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:MSPectrum:CURRent \n
		Snippet: value: CalculateStruct = driver.csounding.mspectrum.current.calculate() \n
		Returns the modulation spectrum results The values described below are returned by FETCh and READ commands. CALCulate
		commands return limit check results instead, one value for each result listed below. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:BLUetooth:MEASurement<Instance>:CSOunding:MSPectrum:CURRent?', self.__class__.CalculateStruct())

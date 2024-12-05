from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AllCls:
	"""All commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("all", core, parent)

	def set(self, stable_phase: bool, step_frequency: bool, power_vs_time: bool, pv_antenna: bool, mod_spectrum: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult[:ALL] \n
		Snippet: driver.configure.csounding.result.all.set(stable_phase = False, step_frequency = False, power_vs_time = False, pv_antenna = False, mod_spectrum = False) \n
		Enables or disables the evaluation of results in the channel sounding measurements. This command combines all other
		CONFigure:BLUetooth:MEAS<i>:CSOunding:RESult... commands. Tip: Use READ...? queries to retrieve results for disabled
		views. \n
			:param stable_phase: OFF | ON Stable phase measurement ON: Evaluate the results. OFF: Do not evaluate results.
			:param step_frequency: OFF | ON Step frequency evaluation
			:param power_vs_time: OFF | ON Power vs time
			:param pv_antenna: OFF | ON Power vs antenna path
			:param mod_spectrum: OFF | ON Modulation spectrum results
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('stable_phase', stable_phase, DataType.Boolean), ArgSingle('step_frequency', step_frequency, DataType.Boolean), ArgSingle('power_vs_time', power_vs_time, DataType.Boolean), ArgSingle('pv_antenna', pv_antenna, DataType.Boolean), ArgSingle('mod_spectrum', mod_spectrum, DataType.Boolean))
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:ALL {param}'.rstrip())

	# noinspection PyTypeChecker
	class AllStruct(StructBase):
		"""Response structure. Fields: \n
			- Stable_Phase: bool: OFF | ON Stable phase measurement ON: Evaluate the results. OFF: Do not evaluate results.
			- Step_Frequency: bool: OFF | ON Step frequency evaluation
			- Power_Vs_Time: bool: OFF | ON Power vs time
			- Pv_Antenna: bool: OFF | ON Power vs antenna path
			- Mod_Spectrum: bool: OFF | ON Modulation spectrum results"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Stable_Phase'),
			ArgStruct.scalar_bool('Step_Frequency'),
			ArgStruct.scalar_bool('Power_Vs_Time'),
			ArgStruct.scalar_bool('Pv_Antenna'),
			ArgStruct.scalar_bool('Mod_Spectrum')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Stable_Phase: bool = None
			self.Step_Frequency: bool = None
			self.Power_Vs_Time: bool = None
			self.Pv_Antenna: bool = None
			self.Mod_Spectrum: bool = None

	def get(self) -> AllStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult[:ALL] \n
		Snippet: value: AllStruct = driver.configure.csounding.result.all.get() \n
		Enables or disables the evaluation of results in the channel sounding measurements. This command combines all other
		CONFigure:BLUetooth:MEAS<i>:CSOunding:RESult... commands. Tip: Use READ...? queries to retrieve results for disabled
		views. \n
			:return: structure: for return value, see the help for AllStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:RESult:ALL?', self.__class__.AllStruct())

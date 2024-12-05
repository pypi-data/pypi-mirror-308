from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MratioCls:
	"""Mratio commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mratio", core, parent)

	def set(self, mod_ratio: float, mod_ratio_enabled: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:MRATio \n
		Snippet: driver.configure.multiEval.limit.brate.mratio.set(mod_ratio = 1.0, mod_ratio_enabled = False) \n
		Specifies the modulation ratio limit deltaf2 avg / deltaf1 avg for BR bursts. \n
			:param mod_ratio: numeric Range: 0 to 2
			:param mod_ratio_enabled: OFF | ON Disable/enable limit checking
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('mod_ratio', mod_ratio, DataType.Float), ArgSingle('mod_ratio_enabled', mod_ratio_enabled, DataType.Boolean))
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:MRATio {param}'.rstrip())

	# noinspection PyTypeChecker
	class MratioStruct(StructBase):
		"""Response structure. Fields: \n
			- Mod_Ratio: float: numeric Range: 0 to 2
			- Mod_Ratio_Enabled: bool: OFF | ON Disable/enable limit checking"""
		__meta_args_list = [
			ArgStruct.scalar_float('Mod_Ratio'),
			ArgStruct.scalar_bool('Mod_Ratio_Enabled')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mod_Ratio: float = None
			self.Mod_Ratio_Enabled: bool = None

	def get(self) -> MratioStruct:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:MRATio \n
		Snippet: value: MratioStruct = driver.configure.multiEval.limit.brate.mratio.get() \n
		Specifies the modulation ratio limit deltaf2 avg / deltaf1 avg for BR bursts. \n
			:return: structure: for return value, see the help for MratioStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:BLUetooth:MEASurement<Instance>:MEValuation:LIMit:BRATe:MRATio?', self.__class__.MratioStruct())

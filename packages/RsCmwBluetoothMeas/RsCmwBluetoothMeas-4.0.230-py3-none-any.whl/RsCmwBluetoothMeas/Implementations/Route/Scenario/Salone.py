from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SaloneCls:
	"""Salone commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("salone", core, parent)

	def set(self, rx_connector: enums.RfConnector, rf_converter: enums.RxConverter) -> None:
		"""SCPI: ROUTe:BLUetooth:MEASurement<Instance>:SCENario:SALone \n
		Snippet: driver.route.scenario.salone.set(rx_connector = enums.RfConnector.I11I, rf_converter = enums.RxConverter.IRX1) \n
		Activates the standalone scenario and selects the RF input path for the measured RF signal. For possible connector and
		converter values, see 'Values for RF path selection'. \n
			:param rx_connector: RF connector for the input path
			:param rf_converter: RX module for the input path
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('rx_connector', rx_connector, DataType.Enum, enums.RfConnector), ArgSingle('rf_converter', rf_converter, DataType.Enum, enums.RxConverter))
		self._core.io.write(f'ROUTe:BLUetooth:MEASurement<Instance>:SCENario:SALone {param}'.rstrip())

	# noinspection PyTypeChecker
	class SaloneStruct(StructBase):
		"""Response structure. Fields: \n
			- Rx_Connector: enums.RfConnector: RF connector for the input path
			- Rf_Converter: enums.RxConverter: RX module for the input path"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Rx_Connector', enums.RfConnector),
			ArgStruct.scalar_enum('Rf_Converter', enums.RxConverter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rx_Connector: enums.RfConnector = None
			self.Rf_Converter: enums.RxConverter = None

	def get(self) -> SaloneStruct:
		"""SCPI: ROUTe:BLUetooth:MEASurement<Instance>:SCENario:SALone \n
		Snippet: value: SaloneStruct = driver.route.scenario.salone.get() \n
		Activates the standalone scenario and selects the RF input path for the measured RF signal. For possible connector and
		converter values, see 'Values for RF path selection'. \n
			:return: structure: for return value, see the help for SaloneStruct structure arguments."""
		return self._core.io.query_struct(f'ROUTe:BLUetooth:MEASurement<Instance>:SCENario:SALone?', self.__class__.SaloneStruct())

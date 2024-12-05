from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputSignalCls:
	"""InputSignal commands group definition. 23 total commands, 2 Subgroups, 18 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("inputSignal", core, parent)

	@property
	def plength(self):
		"""plength commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_plength'):
			from .Plength import PlengthCls
			self._plength = PlengthCls(self._core, self._cmd_group)
		return self._plength

	@property
	def mmode(self):
		"""mmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mmode'):
			from .Mmode import MmodeCls
			self._mmode = MmodeCls(self._core, self._cmd_group)
		return self._mmode

	# noinspection PyTypeChecker
	def get_tcase(self) -> enums.TestCase:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TCASe \n
		Snippet: value: enums.TestCase = driver.configure.csounding.inputSignal.get_tcase() \n
		No command help available \n
			:return: test_case: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TCASe?')
		return Conversions.str_to_scalar_enum(response, enums.TestCase)

	def set_tcase(self, test_case: enums.TestCase) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TCASe \n
		Snippet: driver.configure.csounding.inputSignal.set_tcase(test_case = enums.TestCase.FV_M0phy1) \n
		No command help available \n
			:param test_case: No help available
		"""
		param = Conversions.enum_scalar_to_str(test_case, enums.TestCase)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TCASe {param}')

	# noinspection PyTypeChecker
	def get_tswitch(self) -> enums.Tswitch:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TSWitch \n
		Snippet: value: enums.Tswitch = driver.configure.csounding.inputSignal.get_tswitch() \n
		Specifies the time duration in us for the antenna switch. \n
			:return: tswitch: T0 | T1 | T2 | T4 | T10
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TSWitch?')
		return Conversions.str_to_scalar_enum(response, enums.Tswitch)

	def set_tswitch(self, tswitch: enums.Tswitch) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TSWitch \n
		Snippet: driver.configure.csounding.inputSignal.set_tswitch(tswitch = enums.Tswitch.T0) \n
		Specifies the time duration in us for the antenna switch. \n
			:param tswitch: T0 | T1 | T2 | T4 | T10
		"""
		param = Conversions.enum_scalar_to_str(tswitch, enums.Tswitch)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TSWitch {param}')

	# noinspection PyTypeChecker
	def get_tp_meas(self) -> enums.TpMeasurement:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TPMeas \n
		Snippet: value: enums.TpMeasurement = driver.configure.csounding.inputSignal.get_tp_meas() \n
		Specifies the phase measurement period (T_PM) in us. \n
			:return: tp_measurement: T10 | T20 | T40 | T652
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TPMeas?')
		return Conversions.str_to_scalar_enum(response, enums.TpMeasurement)

	def set_tp_meas(self, tp_measurement: enums.TpMeasurement) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TPMeas \n
		Snippet: driver.configure.csounding.inputSignal.set_tp_meas(tp_measurement = enums.TpMeasurement.T10) \n
		Specifies the phase measurement period (T_PM) in us. \n
			:param tp_measurement: T10 | T20 | T40 | T652
		"""
		param = Conversions.enum_scalar_to_str(tp_measurement, enums.TpMeasurement)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TPMeas {param}')

	# noinspection PyTypeChecker
	def get_tip_2(self) -> enums.Tip:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TIP2 \n
		Snippet: value: enums.Tip = driver.configure.csounding.inputSignal.get_tip_2() \n
		Specifies the interlude period (T_IP2) in us for main mode. \n
			:return: tip_second: T10 | T20 | T30 | T40 | T50 | T60 | T80 | T145
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TIP2?')
		return Conversions.str_to_scalar_enum(response, enums.Tip)

	def set_tip_2(self, tip_second: enums.Tip) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TIP2 \n
		Snippet: driver.configure.csounding.inputSignal.set_tip_2(tip_second = enums.Tip.T10) \n
		Specifies the interlude period (T_IP2) in us for main mode. \n
			:param tip_second: T10 | T20 | T30 | T40 | T50 | T60 | T80 | T145
		"""
		param = Conversions.enum_scalar_to_str(tip_second, enums.Tip)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TIP2 {param}')

	# noinspection PyTypeChecker
	def get_tip_1(self) -> enums.Tip:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TIP1 \n
		Snippet: value: enums.Tip = driver.configure.csounding.inputSignal.get_tip_1() \n
		Specifies the interlude period (T_IP1) in us for mode 0. \n
			:return: tip_one: T10 | T20 | T30 | T40 | T50 | T60 | T80 | T145
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TIP1?')
		return Conversions.str_to_scalar_enum(response, enums.Tip)

	def set_tip_1(self, tip_one: enums.Tip) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TIP1 \n
		Snippet: driver.configure.csounding.inputSignal.set_tip_1(tip_one = enums.Tip.T10) \n
		Specifies the interlude period (T_IP1) in us for mode 0. \n
			:param tip_one: T10 | T20 | T30 | T40 | T50 | T60 | T80 | T145
		"""
		param = Conversions.enum_scalar_to_str(tip_one, enums.Tip)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TIP1 {param}')

	# noinspection PyTypeChecker
	def get_tfc_selection(self) -> enums.TfcSelection:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TFCSelection \n
		Snippet: value: enums.TfcSelection = driver.configure.csounding.inputSignal.get_tfc_selection() \n
		Specifies the frequency hopping duration (T_FCS) in us. \n
			:return: tfc_selection: T15 | T20 | T30 | T40 | T50 | T60 | T80 | T100 | T120 | T150
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TFCSelection?')
		return Conversions.str_to_scalar_enum(response, enums.TfcSelection)

	def set_tfc_selection(self, tfc_selection: enums.TfcSelection) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TFCSelection \n
		Snippet: driver.configure.csounding.inputSignal.set_tfc_selection(tfc_selection = enums.TfcSelection.T100) \n
		Specifies the frequency hopping duration (T_FCS) in us. \n
			:param tfc_selection: T15 | T20 | T30 | T40 | T50 | T60 | T80 | T100 | T120 | T150
		"""
		param = Conversions.enum_scalar_to_str(tfc_selection, enums.TfcSelection)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TFCSelection {param}')

	def get_rt_exention(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:RTEXention \n
		Snippet: value: bool = driver.configure.csounding.inputSignal.get_rt_exention() \n
		Enables or disables the reflector tone extension. \n
			:return: rt_extention: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:RTEXention?')
		return Conversions.str_to_bool(response)

	def set_rt_exention(self, rt_extention: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:RTEXention \n
		Snippet: driver.configure.csounding.inputSignal.set_rt_exention(rt_extention = False) \n
		Enables or disables the reflector tone extension. \n
			:param rt_extention: OFF | ON
		"""
		param = Conversions.bool_to_str(rt_extention)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:RTEXention {param}')

	def get_it_exention(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:ITEXention \n
		Snippet: value: bool = driver.configure.csounding.inputSignal.get_it_exention() \n
		Enables or disables the initiator tone extension. \n
			:return: it_extention: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:ITEXention?')
		return Conversions.str_to_bool(response)

	def set_it_exention(self, it_extention: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:ITEXention \n
		Snippet: driver.configure.csounding.inputSignal.set_it_exention(it_extention = False) \n
		Enables or disables the initiator tone extension. \n
			:param it_extention: OFF | ON
		"""
		param = Conversions.bool_to_str(it_extention)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:ITEXention {param}')

	# noinspection PyTypeChecker
	def get_na_path(self) -> enums.Nantenna:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NAPath \n
		Snippet: value: enums.Nantenna = driver.configure.csounding.inputSignal.get_na_path() \n
		Sets the number of antenna paths. \n
			:return: nantenna: A1 | A2 | A3 | A4 Ax: x denoted the number of antenna paths to be measured.
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NAPath?')
		return Conversions.str_to_scalar_enum(response, enums.Nantenna)

	def set_na_path(self, nantenna: enums.Nantenna) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NAPath \n
		Snippet: driver.configure.csounding.inputSignal.set_na_path(nantenna = enums.Nantenna.A1) \n
		Sets the number of antenna paths. \n
			:param nantenna: A1 | A2 | A3 | A4 Ax: x denoted the number of antenna paths to be measured.
		"""
		param = Conversions.enum_scalar_to_str(nantenna, enums.Nantenna)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NAPath {param}')

	def get_penabled(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PENabled \n
		Snippet: value: bool = driver.configure.csounding.inputSignal.get_penabled() \n
		No command help available \n
			:return: payload_enabled: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PENabled?')
		return Conversions.str_to_bool(response)

	def set_penabled(self, payload_enabled: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PENabled \n
		Snippet: driver.configure.csounding.inputSignal.set_penabled(payload_enabled = False) \n
		No command help available \n
			:param payload_enabled: OFF | ON
		"""
		param = Conversions.bool_to_str(payload_enabled)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PENabled {param}')

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.LePatternType:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PATTern \n
		Snippet: value: enums.LePatternType = driver.configure.csounding.inputSignal.get_pattern() \n
		Sets the pattern type. The setting is relevant for main mode 1 and 3. \n
			:return: pattern: P11 | P44 | PRBS9 | SOUNding | RANDom P11: e.g., 10101010 P44: e.g., 11110000 PRBS9: pseudo random binary sequence of nine bits SOUN: sounding sequence RAND: random sequence
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.LePatternType)

	def set_pattern(self, pattern: enums.LePatternType) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PATTern \n
		Snippet: driver.configure.csounding.inputSignal.set_pattern(pattern = enums.LePatternType.P11) \n
		Sets the pattern type. The setting is relevant for main mode 1 and 3. \n
			:param pattern: P11 | P44 | PRBS9 | SOUNding | RANDom P11: e.g., 10101010 P44: e.g., 11110000 PRBS9: pseudo random binary sequence of nine bits SOUN: sounding sequence RAND: random sequence
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.LePatternType)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PATTern {param}')

	def get_nmm_steps(self) -> int:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NMMSteps \n
		Snippet: value: int = driver.configure.csounding.inputSignal.get_nmm_steps() \n
		Sets the number of steps within the CS subevent for the main mode. \n
			:return: nmm_steps: numeric
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NMMSteps?')
		return Conversions.str_to_int(response)

	def set_nmm_steps(self, nmm_steps: int) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NMMSteps \n
		Snippet: driver.configure.csounding.inputSignal.set_nmm_steps(nmm_steps = 1) \n
		Sets the number of steps within the CS subevent for the main mode. \n
			:param nmm_steps: numeric
		"""
		param = Conversions.decimal_value_to_str(nmm_steps)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NMMSteps {param}')

	# noinspection PyTypeChecker
	def get_nmz_steps(self) -> enums.NmzSteps:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NMZSteps \n
		Snippet: value: enums.NmzSteps = driver.configure.csounding.inputSignal.get_nmz_steps() \n
		Sets the number of mode zero steps within the CS subevent. \n
			:return: nmz_steps: Z1 | Z2 | Z3 No. of mode 0 steps
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NMZSteps?')
		return Conversions.str_to_scalar_enum(response, enums.NmzSteps)

	def set_nmz_steps(self, nmz_steps: enums.NmzSteps) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NMZSteps \n
		Snippet: driver.configure.csounding.inputSignal.set_nmz_steps(nmz_steps = enums.NmzSteps.Z1) \n
		Sets the number of mode zero steps within the CS subevent. \n
			:param nmz_steps: Z1 | Z2 | Z3 No. of mode 0 steps
		"""
		param = Conversions.enum_scalar_to_str(nmz_steps, enums.NmzSteps)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:NMZSteps {param}')

	def get_ra_address(self) -> str:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:RAADdress \n
		Snippet: value: str = driver.configure.csounding.inputSignal.get_ra_address() \n
		Specifies the reflector access address. \n
			:return: ra_address: hex Range: #H0 to #HFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:RAADdress?')
		return trim_str_response(response)

	def set_ra_address(self, ra_address: str) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:RAADdress \n
		Snippet: driver.configure.csounding.inputSignal.set_ra_address(ra_address = rawAbc) \n
		Specifies the reflector access address. \n
			:param ra_address: hex Range: #H0 to #HFFFFFFFF
		"""
		param = Conversions.value_to_str(ra_address)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:RAADdress {param}')

	def get_ia_address(self) -> str:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:IAADdress \n
		Snippet: value: str = driver.configure.csounding.inputSignal.get_ia_address() \n
		Specifies the initiator access address. \n
			:return: ia_address: hex Range: #H0 to #HFFFFFFFF
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:IAADdress?')
		return trim_str_response(response)

	def set_ia_address(self, ia_address: str) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:IAADdress \n
		Snippet: driver.configure.csounding.inputSignal.set_ia_address(ia_address = rawAbc) \n
		Specifies the initiator access address. \n
			:param ia_address: hex Range: #H0 to #HFFFFFFFF
		"""
		param = Conversions.value_to_str(ia_address)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:IAADdress {param}')

	def get_tx_enable(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TXENable \n
		Snippet: value: bool = driver.configure.csounding.inputSignal.get_tx_enable() \n
		Activates or deactivates the CS procedure at the R&S CMW. In the initiator role, the R&S CMW initiates the CS procedure
		and transmits CS signals to the reflector. In the reflector role, the R&S CMW reflects the CS signals back to the
		initiator. \n
			:return: tester_tx_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TXENable?')
		return Conversions.str_to_bool(response)

	def set_tx_enable(self, tester_tx_enable: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TXENable \n
		Snippet: driver.configure.csounding.inputSignal.set_tx_enable(tester_tx_enable = False) \n
		Activates or deactivates the CS procedure at the R&S CMW. In the initiator role, the R&S CMW initiates the CS procedure
		and transmits CS signals to the reflector. In the reflector role, the R&S CMW reflects the CS signals back to the
		initiator. \n
			:param tester_tx_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(tester_tx_enable)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:TXENable {param}')

	# noinspection PyTypeChecker
	def get_role(self) -> enums.Role:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:ROLE \n
		Snippet: value: enums.Role = driver.configure.csounding.inputSignal.get_role() \n
		Sets the role of DUT for the channel sounding procedure. The R&S CMW gets the other role. \n
			:return: role: INITiator | REFLector
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:ROLE?')
		return Conversions.str_to_scalar_enum(response, enums.Role)

	def set_role(self, role: enums.Role) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:ROLE \n
		Snippet: driver.configure.csounding.inputSignal.set_role(role = enums.Role.INITiator) \n
		Sets the role of DUT for the channel sounding procedure. The R&S CMW gets the other role. \n
			:param role: INITiator | REFLector
		"""
		param = Conversions.enum_scalar_to_str(role, enums.Role)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:ROLE {param}')

	# noinspection PyTypeChecker
	def get_phy(self) -> enums.Phy:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PHY \n
		Snippet: value: enums.Phy = driver.configure.csounding.inputSignal.get_phy() \n
		Specifies the physical layer of LE connections. \n
			:return: phy: LE1M | LE2M LE1M: LE 1 Msymbol/s uncoded PHY LE2M: LE 2 Msymbol/s uncoded PHY
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PHY?')
		return Conversions.str_to_scalar_enum(response, enums.Phy)

	def set_phy(self, phy: enums.Phy) -> None:
		"""SCPI: CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PHY \n
		Snippet: driver.configure.csounding.inputSignal.set_phy(phy = enums.Phy.LE1M) \n
		Specifies the physical layer of LE connections. \n
			:param phy: LE1M | LE2M LE1M: LE 1 Msymbol/s uncoded PHY LE2M: LE 2 Msymbol/s uncoded PHY
		"""
		param = Conversions.enum_scalar_to_str(phy, enums.Phy)
		self._core.io.write(f'CONFigure:BLUetooth:MEASurement<Instance>:CSOunding:ISIGnal:PHY {param}')

	def clone(self) -> 'InputSignalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = InputSignalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group

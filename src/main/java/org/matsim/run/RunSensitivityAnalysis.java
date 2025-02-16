package org.matsim.run;


import com.google.inject.Key;
import com.google.inject.name.Names;
import org.matsim.analysis.QsimTimingModule;
import org.matsim.analysis.personMoney.PersonMoneyEventsAnalysisModule;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.TransportMode;
import org.matsim.api.core.v01.network.Link;
import org.matsim.application.MATSimApplication;
import org.matsim.application.options.SampleOptions;
import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.config.groups.ReplanningConfigGroup;
import org.matsim.core.config.groups.ScoringConfigGroup;
import org.matsim.core.config.groups.VspExperimentalConfigGroup;
import org.matsim.core.controler.AbstractModule;
import org.matsim.core.controler.Controler;
import org.matsim.core.controler.OutputDirectoryHierarchy;
import org.matsim.core.events.EventsUtils;
import org.matsim.core.replanning.strategies.DefaultPlanStrategiesModule;
import org.matsim.core.router.costcalculators.OnlyTimeDependentTravelDisutilityFactory;
import org.matsim.core.router.costcalculators.TravelDisutilityFactory;
import org.matsim.core.router.util.TravelTime;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.core.scoring.functions.ScoringParametersForPerson;
import org.matsim.run.scoring.AdvancedScoringConfigGroup;
import org.matsim.run.scoring.AdvancedScoringModule;
import org.matsim.simwrapper.SimWrapperConfigGroup;
import org.matsim.simwrapper.SimWrapperModule;
import org.matsim.vehicles.VehicleType;
import org.matsim.contrib.bicycle.BicycleConfigGroup;
import org.matsim.contrib.bicycle.BicycleLinkSpeedCalculator;
import org.matsim.contrib.bicycle.BicycleLinkSpeedCalculatorDefaultImpl;
import org.matsim.contrib.bicycle.BicycleTravelTime;
import org.matsim.contrib.emissions.utils.EmissionsConfigGroup;
import org.matsim.contrib.vsp.scoring.RideScoringParamsFromCarParams;

import picocli.CommandLine;
import playground.vsp.scoring.IncomeDependentUtilityOfMoneyPersonScoringParameters;

import java.io.File;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

@CommandLine.Command(header = ":: Open Berlin Scenario ::", version = OpenBerlinScenario.VERSION, mixinStandardHelpOptions = true)
public class RunSensitivityAnalysis extends MATSimApplication {

	// General configuration
	public static final int iterNum = 400;
	public static final String VERSION = "6.4";
	public static final String CRS = "EPSG:25832";
	public static final String configFile = "input/v6.4/berlin-v6.4.config.xml";
	public static final double sampleSize = 0.03;

	// Sensitivity Analysis configuration
	public static final List<Double> microSpeeds = List.of(50.0); //List.of(50.0, 70.0, 90.0, 120.0);
	public static final List<Double> microPCEs = List.of(0.5); //List.of(0.5, 0.6, 0.7);
	public static final List<String> planFiles = List.of(
//		"berlin-v6.4-3pct-plans-micro20pct.xml.gz",
//		"berlin-v6.4-3pct-plans-micro40pct.xml.gz",
//		"berlin-v6.4-3pct-plans-micro60pct.xml.gz",
//		"berlin-v6.4-3pct-plans-micro80pct.xml.gz",
//		"berlin-v6.4-3pct-plans-micro100pct.xml.gz"
		"berlin-v6.4-3pct-plans-micro00pct.xml.gz"
	);

	// emission input files
	public static final String emissionConfigFile = "input/v6.4/emission-average/config_emission.xml";
    public static final String HBEFA_FILE_COLD_AVERAGE = "csv-data/cold_avr_2020_WTT_zero.csv";
    public static final String HBEFA_FILE_WARM_AVERAGE = "csv-data/EFA_HOT_Vehcat_hot_avr_WTT_all_road_type.csv";


	public RunSensitivityAnalysis() {
		super(String.format("input/v%s/berlin-v%s.config.xml", VERSION, VERSION));
	}

	public static void main(String[] args) {
		for (String planFile : planFiles) {
			for (double microSpeed : microSpeeds) {
				for (double microPCE : microPCEs) {

					// Generate folderName dynamically
					String folderName = String.format("micro%spct-sp%.0f-pce%.1f-iter%d",extractPercentage(planFile), microSpeed, microPCE, iterNum);

					System.out.printf("Running simulation for folderName = %s%n", folderName);

					// matsim simulation
					try {
						RunSensitivityAnalysis instance = new RunSensitivityAnalysis();
						Config config = instance.prepareConfig(ConfigUtils.loadConfig(configFile), folderName, planFile);
						Scenario scenario = ScenarioUtils.loadScenario(config);
						instance.prepareScenario(scenario, microSpeed, microPCE);
						Controler controler = new Controler(scenario);
						instance.prepareControler(controler);
						controler.run();
					} catch (Exception e) {
						e.printStackTrace();
					}

					System.out.printf("Running emission analysis for folderName = %s%n", folderName);

					// emission analysis
					try {
						Config emissionConfig = ConfigUtils.loadConfig(emissionConfigFile);
						File rootPath = RunBerlinEmission.createOutputFolder("./output/" + folderName); // Use the dynamically generated folder name
						RunBerlinEmission.prepareConfig(emissionConfig, rootPath, HBEFA_FILE_WARM_AVERAGE, HBEFA_FILE_COLD_AVERAGE);

						Scenario emissionScenario = ScenarioUtils.loadScenario(emissionConfig);
                        RunBerlinEmission.prepareScenario(emissionScenario);


						EventsManager eventsManager = EventsUtils.createEventsManager();
						RunBerlinEmission.initializeEmissionModule(emissionConfig, emissionScenario, eventsManager);

						RunBerlinEmission.processEvents(emissionConfig, eventsManager, "./output/" + folderName + "/output_events.xml.gz");
						RunBerlinEmission.writeOutputs(emissionConfig, emissionScenario, rootPath);

						System.out.printf("Emission analysis completed for folderName = %s%n", folderName);
					} catch (Exception e) {
						e.printStackTrace();
					}


				}
			}
		}
	}


	private static String extractPercentage(String planFile) {
		String percentage = planFile.replaceAll(".*-micro(\\d+)pct.*", "$1");
		return String.format("%03d", Integer.parseInt(percentage));
	}

	protected Config prepareConfig(Config config, String folderName, String planFile) {

        SimWrapperConfigGroup sw = ConfigUtils.addOrGetModule(config, SimWrapperConfigGroup.class);

		config.controller().setOutputDirectory("./output/" + folderName);
		System.out.println(config.controller().getOutputDirectory());
		config.controller().setOverwriteFileSetting( OutputDirectoryHierarchy.OverwriteFileSetting.deleteDirectoryIfExists );

		config.controller().setLastIteration(iterNum);
		config.plans().setInputFile(planFile);

		{
			System.out.println("Sample size: " + sampleSize);
			config.qsim().setFlowCapFactor(sampleSize);
			config.qsim().setStorageCapFactor(sampleSize);

			// Counts can be scaled with sample size
			config.counts().setCountsScaleFactor(sampleSize);
			sw.sampleSize = sampleSize;

			// to resolve the congestion issue of transit vehicles that occurs due to downscaling the sample size
			// Refer to https://github.com/matsim-org/matsim-code-examples/issues/395 for more details
			config.qsim().setPcuThresholdForFlowCapacityEasing( 0.1 );
		}

        config.qsim().setUsingTravelTimeCheckInTeleportation(true);

        // overwrite ride scoring params with values derived from car
		RideScoringParamsFromCarParams.setRideScoringParamsBasedOnCarParams(config.scoring(), 1.0);
		Activities.addScoringParams(config, true);

		// Required for all calibration strategies
		for (String subpopulation : List.of("person", "freight", "goodsTraffic", "commercialPersonTraffic", "commercialPersonTraffic_service")) {
			config.replanning().addStrategySettings(
				new ReplanningConfigGroup.StrategySettings()
					.setStrategyName(DefaultPlanStrategiesModule.DefaultSelector.ChangeExpBeta)
					.setWeight(1.0)
					.setSubpopulation(subpopulation)
			);

			config.replanning().addStrategySettings(
				new ReplanningConfigGroup.StrategySettings()
					.setStrategyName(DefaultPlanStrategiesModule.DefaultStrategy.ReRoute)
					.setWeight(0.15)
					.setSubpopulation(subpopulation)
			);
		}

		config.replanning().addStrategySettings(
			new ReplanningConfigGroup.StrategySettings()
				.setStrategyName(DefaultPlanStrategiesModule.DefaultStrategy.TimeAllocationMutator)
				.setWeight(0.15)
				.setSubpopulation("person")
		);

		config.replanning().addStrategySettings(
			new ReplanningConfigGroup.StrategySettings()
				.setStrategyName(DefaultPlanStrategiesModule.DefaultStrategy.SubtourModeChoice)
				.setWeight(0.15)
				.setSubpopulation("person")
		);


		// Bicycle config must be present
		ConfigUtils.addOrGetModule(config, BicycleConfigGroup.class);

		// scoring for microcar
		{
			ScoringConfigGroup.ModeParams params = new ScoringConfigGroup.ModeParams("microcar");
			params.setConstant(-0.60);
			params.setDailyMonetaryConstant(-3.0);
			params.setDailyUtilityConstant(0.0);
			params.setMarginalUtilityOfDistance(0.0);
			params.setMarginalUtilityOfTraveling(0.0);
			params.setMonetaryDistanceRate(-2.39E-5);
			params.setMode("microcar");

			config.scoring().addModeParams(params);
		}

		return config;
	}

    //////
	protected void prepareScenario(Scenario scenario, double microSpeed, double microPCE) {

		// Add microcar mode to all the links where car mode is allowed
		for (Link link : scenario.getNetwork().getLinks().values()) {
			Set<String> allowedModes = new HashSet<>(link.getAllowedModes());
			if (allowedModes.contains("car")) {
				allowedModes.add("microcar");
			}
			link.setAllowedModes(allowedModes);
		}

		// Add PCE and Max. speed of microcar to the vehicle file based on values defined in this Java file
		for (VehicleType vehicleType : scenario.getVehicles().getVehicleTypes().values()) {
			Id<VehicleType> vehicleTypeId = vehicleType.getId();
			if (Objects.equals(vehicleTypeId.toString(), "microcar")) {
				vehicleType.setMaximumVelocity(microSpeed / 3.6); // Apply microSpeed
				vehicleType.setPcuEquivalents(microPCE);          // Apply microPCE
			}
		}

		// Adjust the PCE of transit vehicles (public transportation) along with the sample size
		// Please refer to https://github.com/matsim-org/matsim-code-examples/issues/395 for the reason
		for (VehicleType vehicleType : scenario.getTransitVehicles().getVehicleTypes().values()) {
			double originalVehiclePce = vehicleType.getPcuEquivalents();
			vehicleType.setPcuEquivalents(originalVehiclePce * sampleSize);
		}

	}

	@Override
	protected void prepareControler(Controler controler) {

		controler.addOverridingModule(new SimWrapperModule());

		controler.addOverridingModule(new TravelTimeBinding());

		controler.addOverridingModule(new QsimTimingModule());

		// AdvancedScoring is specific to matsim-berlin!
		if (ConfigUtils.hasModule(controler.getConfig(), AdvancedScoringConfigGroup.class)) {
			controler.addOverridingModule(new AdvancedScoringModule());
			controler.getConfig().scoring().setExplainScores(true);
		} else {
			// if the above config group is not present we still need income dependent scoring
			// this implementation also allows for person specific asc
			controler.addOverridingModule(new AbstractModule() {
				@Override
				public void install() {
					bind(ScoringParametersForPerson.class).to(IncomeDependentUtilityOfMoneyPersonScoringParameters.class).asEagerSingleton();
				}
			});
		}
		controler.addOverridingModule(new PersonMoneyEventsAnalysisModule());
	}

	/**
	 * Add travel time bindings for ride and freight modes, which are not actually network modes.
	 */
	public static final class TravelTimeBinding extends AbstractModule {

		private final boolean carOnly;

		public TravelTimeBinding() {
			this.carOnly = false;
		}

		public TravelTimeBinding(boolean carOnly) {
			this.carOnly = carOnly;
		}

		@Override
		public void install() {
			addTravelTimeBinding(TransportMode.ride).to(networkTravelTime());
			addTravelDisutilityFactoryBinding(TransportMode.ride).to(carTravelDisutilityFactoryKey());

			if (!carOnly) {
				addTravelTimeBinding("freight").to(Key.get(TravelTime.class, Names.named(TransportMode.truck)));
				addTravelDisutilityFactoryBinding("freight").to(Key.get(TravelDisutilityFactory.class, Names.named(TransportMode.truck)));


				bind(BicycleLinkSpeedCalculator.class).to(BicycleLinkSpeedCalculatorDefaultImpl.class);

				// Bike should use free speed travel time
				addTravelTimeBinding(TransportMode.bike).to(BicycleTravelTime.class);
				addTravelDisutilityFactoryBinding(TransportMode.bike).to(OnlyTimeDependentTravelDisutilityFactory.class);
			}
		}
	}

}



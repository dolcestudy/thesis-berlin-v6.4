package org.matsim.run;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.matsim.analysis.EmissionDataProcessor;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.network.Link;
import org.matsim.contrib.emissions.EmissionModule;
import org.matsim.contrib.emissions.EmissionUtils;
import org.matsim.contrib.emissions.HbefaRoadTypeMapping;
import org.matsim.contrib.emissions.HbefaVehicleCategory;
import org.matsim.contrib.emissions.OsmHbefaMapping;
import org.matsim.contrib.emissions.utils.EmissionsConfigGroup;
import org.matsim.core.api.experimental.events.EventsManager;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.controler.AbstractModule;
import org.matsim.core.controler.Injector;
import org.matsim.core.controler.OutputDirectoryHierarchy;
import org.matsim.core.events.EventsUtils;
import org.matsim.core.events.algorithms.EventWriterXML;
import org.matsim.core.network.NetworkUtils;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.vehicles.EngineInformation;
import org.matsim.vehicles.MatsimVehicleWriter;
import org.matsim.vehicles.VehicleType;
import org.matsim.vehicles.VehicleUtils;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.IOException;
import java.util.*;

/**
 * This class runs the Berlin emission simulation in MATSim.
 * It loads the necessary configurations, processes emission data,
 * and generates output files including vehicle emissions and Excel summaries.
 */
public final class RunBerlinEmission {
	public static final String HBEFA_FILE_COLD_AVERAGE = "csv-data/cold_avr_2020_WTT_zero.csv";
	public static final String HBEFA_FILE_WARM_AVERAGE = "csv-data/EFA_HOT_Vehcat_hot_avr_WTT_all_road_type.csv";

	private static final Logger log = LogManager.getLogger(RunBerlinEmission.class);
	private static final String folderName = "micro100pct-sp60-pce0.5-DMC-2.5-MDR-0.24-iter0";
	private static final String basePath = "./output/" + folderName;
	private static final String eventsFile = basePath + "/output_events.xml.gz";
	private static final String emissionEventOutputFileName = "output_event_emission.xml.gz";

	/**
	 * Private constructor to prevent instantiation.
	 */
	private RunBerlinEmission() {
		throw new UnsupportedOperationException("Utility class");
	}

	/**
	 * Main method that runs the MATSim emission analysis.
	 *
	 * @param args Command-line arguments.
	 */
	public static void main(String[] args) {
		Config config = ConfigUtils.loadConfig("input/v6.4/emission-average/config_emission.xml");
		File rootPath = createOutputFolder(basePath);
		prepareConfig(config, rootPath, HBEFA_FILE_WARM_AVERAGE, HBEFA_FILE_COLD_AVERAGE);
		Scenario scenario = ScenarioUtils.loadScenario(config);

		prepareScenario(scenario);
		// the two lines below are original prepareScenario for emission analysis
		// but the prepareScenario for emission analysis is already provided by MATSim contrib
		// setupHbefaRoadTypes(scenario);
		// setupVehicleAttributes(scenario);


		EventsManager eventsManager = EventsUtils.createEventsManager();
		initializeEmissionModule(config, scenario, eventsManager);

		processEvents(config, eventsManager, eventsFile);
		writeOutputs(config, scenario, rootPath);
	}



	/**
	 * Loads the configuration for the emission simulation.
	 *
	 * @param args The command-line arguments containing the configuration file path.
	 * @return The loaded MATSim configuration object.
	 */
	public static Config loadConfig(String[] args) {
		Config config;
		if (args == null || args.length == 0 || args[0] == null) {
			config = ConfigUtils.loadConfig("xxx");
		} else {
			config = ConfigUtils.loadConfig(args);
		}
		return config;
	}

	/**
	 * Creates an output folder for emission analysis.
	 *
	 * @param basePath The base path where the folder should be created.
	 * @return The created folder as a File object.
	 */
	public static File createOutputFolder(String basePath) {
		File folder = new File(basePath + "/emission-analysis");
		if (!folder.exists() && folder.mkdir()) {
			log.info("A new folder was created: " + folder.getPath());
		} else if (folder.exists()) {
			log.info("The folder already exists.");
		} else {
			log.error("Failed to create a new folder.");
		}
		return folder;
	}

	/**
	 * Configures the MATSim scenario settings for emissions analysis.
	 *
	 * @param config          The MATSim configuration object.
	 * @param rootPath        The output directory path.
	 * @param warmEmissionFile Path to the warm emission factors file.
	 * @param coldEmissionFile Path to the cold emission factors file.
	 */
	public static void prepareConfig(Config config, File rootPath, String warmEmissionFile, String coldEmissionFile) {
		config.controller().setOutputDirectory(rootPath.getPath());
		config.network().setInputFile("../../../" + rootPath.getParentFile() + "/output_network.xml.gz");
		config.plans().setInputFile("../../../" + rootPath.getParentFile() + "/output_plans.xml.gz");
		config.vehicles().setVehiclesFile("../../../" + rootPath.getParentFile() + "/output_allVehicles.xml.gz");
		config.controller().setOverwriteFileSetting(OutputDirectoryHierarchy.OverwriteFileSetting.deleteDirectoryIfExists);

		EmissionsConfigGroup emissionsConfig = ConfigUtils.addOrGetModule(config, EmissionsConfigGroup.class);
		emissionsConfig.setAverageColdEmissionFactorsFile(coldEmissionFile);
		emissionsConfig.setAverageWarmEmissionFactorsFile(warmEmissionFile);
		emissionsConfig.setNonScenarioVehicles(EmissionsConfigGroup.NonScenarioVehicles.abort);
		emissionsConfig.setDetailedVsAverageLookupBehavior(EmissionsConfigGroup.DetailedVsAverageLookupBehavior.directlyTryAverageTable);
		emissionsConfig.setEmissionsComputationMethod(EmissionsConfigGroup.EmissionsComputationMethod.StopAndGoFraction);
	}



	/**
	 * Processes the emission events and writes the output.
	 */
	public static void processEvents(Config config, EventsManager eventsManager, String eventsFile) {
		final EventWriterXML eventWriterXML = new EventWriterXML(config.controller().getOutputDirectory() + '/' + emissionEventOutputFileName);
		eventsManager.addHandler(eventWriterXML);
		EventsUtils.readEvents(eventsManager, eventsFile);
		eventWriterXML.closeFile();
	}

	/**
	 * Writes output files such as vehicle, network, and configuration data.
	 */
	public static void writeOutputs(Config config, Scenario scenario, File rootPath) {
		new MatsimVehicleWriter(scenario.getVehicles()).writeFile(config.controller().getOutputDirectory() + "/output_vehicles.xml.gz");
		NetworkUtils.writeNetwork(scenario.getNetwork(), config.controller().getOutputDirectory() + "/output_network.xml.gz");
		ConfigUtils.writeConfig(config, config.controller().getOutputDirectory() + "/output_config.xml");
		ConfigUtils.writeMinimalConfig(config, config.controller().getOutputDirectory() + "/output_config_reduced.xml");

		generateExcelSummary(config, rootPath);
	}

	/**
	 * Generates an Excel summary of emission data.
	 *
	 * @param config   The MATSim configuration object.
	 * @param rootPath The root path where the summary will be saved.
	 */
	public static void generateExcelSummary(Config config, File rootPath) {
		try {
			log.info("Start parsing the vehicle file");
			Map<String, String> vehicleMap = EmissionDataProcessor.parseVehicleFile(rootPath + "/output_vehicles.xml.gz");

			log.info("Start parsing the event file");
			Map<String, Map<Double, Map<String, EmissionDataProcessor.EmissionData>>> data =
				EmissionDataProcessor.parseEventFile(rootPath.getPath() + '/' + emissionEventOutputFileName, vehicleMap);

			log.info("Start saving the data to Excel");
			EmissionDataProcessor.saveToExcel(data, config.controller().getOutputDirectory() + "/emissions_summary_" + rootPath.getParentFile().getName() + ".xlsx");

			log.info("Excel file created: " + config.controller().getOutputDirectory() + "/emissions_summary_" + rootPath.getParentFile().getName() + ".xlsx");

		} catch (IOException | SAXException | javax.xml.parsers.ParserConfigurationException | NumberFormatException e) {
			log.error("Failed to generate Excel summary", e);
		}




	}

	/**
	 * Assigns HBEFA road types to links in the scenario.
	 *
	 * @param scenario The MATSim scenario object.
	 */
	public static void setupHbefaRoadTypes(Scenario scenario) {
		for (Link link : scenario.getNetwork().getLinks().values()) {
			double freeSpeed = link.getFreespeed() * 3.6;
			String roadType = classifyRoadType(freeSpeed);
			EmissionUtils.setHbefaRoadType(link, roadType);
		}
	}

	/**
	 * Classifies a road type based on free flow speed.
	 *
	 * @param freeSpeed The free flow speed of the road in km/h.
	 * @return The corresponding HBEFA road type.
	 */
	public static String classifyRoadType(double freeSpeed) {
		if (freeSpeed <= 30) return "URB/Local/30";
		if (freeSpeed <= 40) return "URB/Local/40";
		if (freeSpeed <= 50) return "URB/Trunk-City/50";
		if (freeSpeed <= 60) return "URB/Trunk-City/60";
		if (freeSpeed <= 70) return "URB/Trunk-City/70";
		if (freeSpeed <= 80) return "URB/Trunk-City/80";
		if (freeSpeed <= 90) return "URB/Trunk-City/90";
		if (freeSpeed <= 100) return "URB/MW-City/100";
		if (freeSpeed <= 110) return "URB/MW-Nat./120";
		return "URB/MW-Nat./130";
	}

	/**
	 * Sets up vehicle attributes for emissions calculations.
	 *
	 * @param scenario The MATSim scenario object.
	 */
	public static void setupVehicleAttributes(Scenario scenario) {
		Set<String> nonHbefaVehicleTypes = Set.of("Tram_veh_type", "Ferry_veh_type", "Bus_veh_type", "RE_RB_veh_type", "S-Bahn_veh_type", "U-Bahn_veh_type");
		for (VehicleType vehicleType : scenario.getVehicles().getVehicleTypes().values()) {
			if (nonHbefaVehicleTypes.contains(vehicleType.getId().toString())) {
				EngineInformation engineInfo = vehicleType.getEngineInformation();
				VehicleUtils.setHbefaVehicleCategory(engineInfo, HbefaVehicleCategory.NON_HBEFA_VEHICLE.toString());
				VehicleUtils.setHbefaTechnology(engineInfo, "average");
				VehicleUtils.setHbefaEmissionsConcept(engineInfo, "average");
				VehicleUtils.setHbefaSizeClass(engineInfo, "average");
			}
		}
	}

	/**
	 * Initializes the emission module for MATSim.
	 */
	public static void initializeEmissionModule(Config config, Scenario scenario, EventsManager eventsManager) {
		AbstractModule module = new AbstractModule() {
			@Override
			public void install() {
				bind(Scenario.class).toInstance(scenario);
				bind(EventsManager.class).toInstance(eventsManager);
				bind(EmissionModule.class);
			}
		};
		com.google.inject.Injector injector = Injector.createInjector(config, module);
		injector.getInstance(EmissionModule.class);
	}


	/**
	 * Prepares the scenario for emissions simulation by setting up vehicle attributes.
	 *
	 * @param scenario The MATSim scenario object.
	 */
	public static void prepareScenario(Scenario scenario) {
		HbefaRoadTypeMapping roadTypeMapping = OsmHbefaMapping.build();
		roadTypeMapping.addHbefaMappings(scenario.getNetwork());

		setupVehicleAttributes(scenario);
	}

}


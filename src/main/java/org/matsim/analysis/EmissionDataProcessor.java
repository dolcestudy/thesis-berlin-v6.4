package org.matsim.analysis;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import java.io.*;
import java.util.*;
import java.util.zip.GZIPInputStream;

/**
 * Utility class for processing emission data from MATSim simulation.
 * It reads vehicle and event files, aggregates data, and exports results to Excel.
 */
public final class EmissionDataProcessor {

	private static final Logger logger = LogManager.getLogger(EmissionDataProcessor.class);

	private EmissionDataProcessor() {
		throw new UnsupportedOperationException("This is a utility class and cannot be instantiated");
	}


	/**
	 * Parses the vehicle file and extracts vehicle types.
	 * @param vehicleFile Path to the vehicle file (compressed XML).
	 * @return A map where the key is the vehicle ID and the value is the vehicle type.
	 * @throws Exception If an error occurs while reading the file.
	 */
	public static Map<String, String> parseVehicleFile(String vehicleFile) throws IOException, SAXException, javax.xml.parsers.ParserConfigurationException {
		Map<String, String> vehicleMap = new HashMap<>();
		InputStream inputStream = new GZIPInputStream(new FileInputStream(vehicleFile));


		javax.xml.parsers.SAXParserFactory factory = javax.xml.parsers.SAXParserFactory.newInstance();
		javax.xml.parsers.SAXParser parser = factory.newSAXParser();


		DefaultHandler handler = new DefaultHandler() {
			boolean vehicleId = false;
			boolean vehicleType = false;

			public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
				if (qName.equals("vehicle")) {
					vehicleId = attributes.getValue("id") != null;
					vehicleType = attributes.getValue("type") != null;
					if (vehicleId && vehicleType) {
						String id = attributes.getValue("id");
						String type = attributes.getValue("type");
						vehicleMap.put(id, type);
					}
				}
			}
		};

		parser.parse(inputStream, handler);
		inputStream.close();
		return vehicleMap;
	}

	/**
	 * Parses the event file and aggregates emissions data.
	 * @param eventFile Path to the event file (compressed XML).
	 * @param vehicleMap A map of vehicle IDs to vehicle types.
	 * @return A nested map containing emissions data by vehicle type, hour, and link ID.
	 * @throws Exception If an error occurs while reading the file.
	 */
	public static Map<String, Map<Double, Map<String, EmissionData>>> parseEventFile(String eventFile, Map<String, String> vehicleMap) throws IOException, SAXException, javax.xml.parsers.ParserConfigurationException, NumberFormatException {
		Map<String, Map<Double, Map<String, EmissionData>>> data = new HashMap<>();
		InputStream inputStream = new GZIPInputStream(new FileInputStream(eventFile));


		javax.xml.parsers.SAXParserFactory factory = javax.xml.parsers.SAXParserFactory.newInstance();
		javax.xml.parsers.SAXParser parser = factory.newSAXParser();


		DefaultHandler handler = new DefaultHandler() {
			boolean isWarmEmissionEvent = false;
			String vehicleId;
			Double time;
			double hour;
			String linkId;
			double fcMj;
			double co2e;

			public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
				if (qName.equals("event") && attributes.getValue("type").equals("warmEmissionEvent")) {
					vehicleId = attributes.getValue("vehicleId");
					time = Double.parseDouble(attributes.getValue("time"));
					hour = Math.floor(time / 3600);
					linkId = attributes.getValue("linkId");
					fcMj = Double.parseDouble(attributes.getValue("FC_MJ"));
					co2e = Double.parseDouble(attributes.getValue("CO2e"));

//					System.out.println(hour + ":" + vehicleId);


					String vehicleType = vehicleMap.getOrDefault(vehicleId, "unknown");

					String vehicleCategory = switch (vehicleType) {
						case "car", "ride", "vwCaddy", "golf1.4" -> "car";
						case "heavy40t", "medium18t", "freight", "truck" -> "HGV";
						case "mercedes313", "light8t" -> "LCV";
						case "microcar" -> "microcar";
						case "Tram_veh_type", "Ferry_veh_type", "Bus_veh_type", "RE_RB_veh_type", "S-Bahn_veh_type", "U-Bahn_veh_type" -> "pt";
						default -> "unknown";
					};



//					System.out.println(vehicleCategory);

					data.putIfAbsent(vehicleCategory, new HashMap<>());
					data.get(vehicleCategory).putIfAbsent(hour, new HashMap<>());
					data.get(vehicleCategory).get(hour).putIfAbsent(linkId, new EmissionData(0.0, 0.0));

					EmissionData emission = data.get(vehicleCategory).get(hour).get(linkId);
					emission.setFcMj(emission.getFcMj() + fcMj);
					emission.setCo2e(emission.getCo2e() + co2e);
				}
			}
		};

		parser.parse(inputStream, handler);
		inputStream.close();
		return data;
	}

	/**
	 * Saves the aggregated emissions data to an Excel file.
	 *
	 * @param data The emissions data organized by vehicle category, time, and link ID.
	 * @param outputFile The path to the output Excel file.
	 * @throws IOException If an error occurs while writing the file.
	 */
	public static void saveToExcel(Map<String, Map<Double, Map<String, EmissionData>>> data, String outputFile) throws IOException {
		Workbook workbook = new XSSFWorkbook();


		Sheet sheet1 = workbook.createSheet("Summary_By_Time");
		Row headerRow1 = sheet1.createRow(0);
		headerRow1.createCell(0).setCellValue("vehicleCategory");
		headerRow1.createCell(1).setCellValue("Time");
		headerRow1.createCell(2).setCellValue("Sum_FC_MJ");
		headerRow1.createCell(3).setCellValue("Sum_CO2e");

		int rowNum1 = 1;

		for (Map.Entry<String, Map<Double, Map<String, EmissionData>>> vehicleEntry : data.entrySet()) {
			String vehicleCategory = vehicleEntry.getKey();

			for (Map.Entry<Double, Map<String, EmissionData>> timeEntry : vehicleEntry.getValue().entrySet()) {
				Double time = timeEntry.getKey();
				double sumFcMj = 0.0;
				double sumCo2e = 0.0;

				for (EmissionData emission : timeEntry.getValue().values()) {
					sumFcMj += emission.getFcMj();
					sumCo2e += emission.getCo2e();
				}

				Row row = sheet1.createRow(rowNum1++);
				row.createCell(0).setCellValue(vehicleCategory);
				row.createCell(1).setCellValue(time);
				row.createCell(2).setCellValue(sumFcMj);
				row.createCell(3).setCellValue(sumCo2e);
			}
		}


		Sheet sheet2 = workbook.createSheet("Summary_By_LinkId");
		Row headerRow2 = sheet2.createRow(0);
		headerRow2.createCell(0).setCellValue("vehicleCategory");
		headerRow2.createCell(1).setCellValue("LinkId");
		headerRow2.createCell(2).setCellValue("Sum_FC_MJ");
		headerRow2.createCell(3).setCellValue("Sum_CO2e");

		int rowNum2 = 1;

		for (Map.Entry<String, Map<Double, Map<String, EmissionData>>> vehicleEntry : data.entrySet()) {
			String vehicleCategory = vehicleEntry.getKey();
			Map<String, EmissionData> linkData = new HashMap<>();

			for (Map<String, EmissionData> timeMap : vehicleEntry.getValue().values()) {
				for (Map.Entry<String, EmissionData> linkEntry : timeMap.entrySet()) {
					String linkId = linkEntry.getKey();
					EmissionData emission = linkEntry.getValue();

					linkData.putIfAbsent(linkId, new EmissionData(0.0, 0.0));
					EmissionData aggregatedEmission = linkData.get(linkId);
					aggregatedEmission.setFcMj(aggregatedEmission.getFcMj() + emission.getFcMj());
					aggregatedEmission.setCo2e(aggregatedEmission.getCo2e() + emission.getCo2e());
				}
			}

			for (Map.Entry<String, EmissionData> linkEntry : linkData.entrySet()) {
				String linkId = linkEntry.getKey();
				EmissionData emission = linkEntry.getValue();

				Row row = sheet2.createRow(rowNum2++);
				row.createCell(0).setCellValue(vehicleCategory);
				row.createCell(1).setCellValue(linkId);
				row.createCell(2).setCellValue(emission.getFcMj());
				row.createCell(3).setCellValue(emission.getCo2e());
			}
		}


		try (FileOutputStream fileOut = new FileOutputStream(outputFile)) {
			workbook.write(fileOut);
		}
		workbook.close();
	}

	/**
	 * Data structure for storing fuel consumption and CO2 emissions.
	 */
	public static final class EmissionData {
		private double fcMj;
		private double co2e;

		public EmissionData(double fcMj, double co2e) {
			this.fcMj = fcMj;
			this.co2e = co2e;
		}

		public double getFcMj() {
			return fcMj;
		}

		public void setFcMj(double fcMj) {
			this.fcMj = fcMj;
		}

		public double getCo2e() {
			return co2e;
		}

		public void setCo2e(double co2e) {
			this.co2e = co2e;
		}
	}


}

package org.matsim.analysis;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import java.io.*;
import java.util.*;
import java.util.zip.GZIPInputStream;

public class EmissionDataProcessor {

    // Vehicle file parsing
    public static Map<String, String> parseVehicleFile(String vehicleFile) throws Exception {
        Map<String, String> vehicleMap = new HashMap<>();
        InputStream inputStream = new GZIPInputStream(new FileInputStream(vehicleFile));

        // SAXParserFactory for XML parsing
        javax.xml.parsers.SAXParserFactory factory = javax.xml.parsers.SAXParserFactory.newInstance();
        javax.xml.parsers.SAXParser parser = factory.newSAXParser();

        // SAX handler to parse XML
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

    // Event file parsing with memory optimization
    public static Map<String, Map<Double, Map<String, EmissionData>>> parseEventFile(String eventFile, Map<String, String> vehicleMap) throws Exception {
        Map<String, Map<Double, Map<String, EmissionData>>> data = new HashMap<>();
        InputStream inputStream = new GZIPInputStream(new FileInputStream(eventFile));

        // SAXParserFactory for XML parsing
        javax.xml.parsers.SAXParserFactory factory = javax.xml.parsers.SAXParserFactory.newInstance();
        javax.xml.parsers.SAXParser parser = factory.newSAXParser();

        // SAX handler to parse XML
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
					hour = Math.floor(time/3600);
                    linkId = attributes.getValue("linkId");
                    fcMj = Double.parseDouble(attributes.getValue("FC_MJ"));
                    co2e = Double.parseDouble(attributes.getValue("CO2e"));

					System.out.println(hour + ":" + vehicleId);




					String vehicleType = vehicleMap.getOrDefault(vehicleId, "unknown");

					String vehicleCategory = switch (vehicleType) {
						case "car", "ride", "vwCaddy","golf1.4"                                  -> "car";
						case "heavy40t", "medium18t", "freight", "truck"                         -> "HGV";
						case "mercedes313", "light8t"                                            -> "LCV";
						case "microcar"                                                          -> "microcar";  // add "golf1.4"???
						case "Tram_veh_type", "Ferry_veh_type", "Bus_veh_type", "RE_RB_veh_type", "S-Bahn_veh_type", "U-Bahn_veh_type" -> "pt";
						default                                                                  -> "unknown";
					};

//					String vehicleCategory = switch (vehicleType) {
//						case "car"                                -> "car";
//						case "ride"                                -> "ride";
//						case "golf1.4"                              -> "golf";
//						case "vwCaddy"                                 -> "vwCaddy";
//						case "heavy40t", "medium18t", "freight", "truck"                         -> "HGV";
//						case "mercedes313", "light8t"                                            -> "LCV";
//						case "microcar"                                                          -> "microcar";
//						case "Tram_veh_type", "Ferry_veh_type", "Bus_veh_type", "RE_RB_veh_type", "S-Bahn_veh_type", "U-Bahn_veh_type" -> "pt";
//						default                                                                  -> "unknown";
//					};

					System.out.println(vehicleCategory);

                    // Initialize data structure if not already
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

    // Helper class for storing FC_MJ and CO2e values
    public static class EmissionData {
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

	// Convert the aggregated data to Excel with two sheets
	public static void saveToExcel(Map<String, Map<Double, Map<String, EmissionData>>> data, String outputFile) throws IOException {
		Workbook workbook = new XSSFWorkbook();

		// Create first sheet: Summary by VehicleType and Time
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

		// Create second sheet: Summary by VehicleType and LinkId
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

		// Write to file
		try (FileOutputStream fileOut = new FileOutputStream(outputFile)) {
			workbook.write(fileOut);
		}
		workbook.close();
	}


    public static void main(String[] args) throws Exception {
        String vehicleFile = "output/micro100pct-sp60-pce0.5-DMC-2.5-MDR-0.24-iter1/emission-analysis/output_vehicles.xml.gz";
        String eventFile = "output/micro100pct-sp60-pce0.5-DMC-2.5-MDR-0.24-iter1/emission-analysis/output_event_emission.xml.gz";
        String outputFile = "output/micro100pct-sp60-pce0.5-DMC-2.5-MDR-0.24-iter1/emission-analysis/emissions_summary_2.xlsx";

        System.out.println("Start parsing the vehicle file");
        Map<String, String> vehicleMap = parseVehicleFile(vehicleFile);
        System.out.println("Start parsing the event file");
        Map<String, Map<Double, Map<String, EmissionData>>> data = parseEventFile(eventFile, vehicleMap);

        System.out.println("Start saving the data to Excel");
        saveToExcel(data, outputFile);

        System.out.println("Excel file created: " + outputFile);
    }
}

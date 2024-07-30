# Dashboard Waste Management

This repository contains a data visualization dashboard using Flask, Dash Plotly for waste management in Northern Ireland, utilizing the Northern Ireland Local Authority Collected Municipal Waste Management 2023 dataset.

https://ckan.publishing.service.gov.uk/dataset/northern-ireland-local-authority-collected-municipal-waste-management-statistics/resource/dd16815e-e183-41c0-90d3-ad078bfd7ded

| Variable Name                                             | Description |
|-----------------------------------------------------------|-------------|
| `quarter_code`                                            | Code representing the quarter. |
| `quarter_name`                                            | Name of the quarter. |
| `financial_year`                                          | Financial year associated with the data. |
| `area_code`                                               | Code representing the area. |
| `area_name`                                               | Name of the area. |
| `waste_mgmt_group`                                        | Waste management group. |
| `data_status`                                             | Status of the data (e.g., preliminary, final). |
| `la_collected_waste`                                      | Total local authority collected waste. |
| `la_preparing_for_reuse`                                  | Local authority waste prepared for reuse. |
| `la_dry_recycling`                                        | Local authority dry recycling waste. |
| `la_composting`                                           | Local authority composting waste. |
| `la_dry_recycling_composting`                             | Total dry recycling and composting by local authority. |
| `la_preparing_reuse_dry_recycling_composting`             | Local authority waste prepared for reuse, dry recycling, and composting. |
| `la_dry_recycling_composting_rate`                        | Rate of dry recycling and composting by local authority. |
| `la_energy_recovery_mixed`                                | Local authority mixed waste sent for energy recovery. |
| `la_energy_recovery_specific`                             | Local authority specific waste sent for energy recovery. |
| `la_energy_recovery_rate`                                 | Rate of energy recovery by local authority. |
| `la_landfilled`                                           | Local authority waste sent to landfill. |
| `la_landfill_rate`                                        | Rate of landfill by local authority. |
| `biodegradable_la_waste_to_landfill`                      | Biodegradable local authority waste sent to landfill. |
| `nilas_financial_year_allocation_before_transfers`        | NILAS financial year allocation before transfers. |
| `nilas_financial_year_allocation_after_transfers`         | NILAS financial year allocation after transfers. |
| `household_waste_arisings`                                | Total household waste arisings. |
| `household_waste_preparing_for_reuse`                     | Household waste prepared for reuse. |
| `household_waste_dry_recycling`                           | Household dry recycling waste. |
| `household_waste_composting`                              | Household composting waste. |
| `household_waste_dry_recycling_composting`                | Total dry recycling and composting by household. |
| `household_waste_preparing_reuse_dry_recycling_composting`| Household waste prepared for reuse, dry recycling, and composting. |
| `household_waste_dry_recycling_composting_rate`           | Rate of dry recycling and composting by household. |
| `household_waste_landfilled`                              | Household waste sent to landfill. |
| `household_waste_landfill_rate`                           | Rate of landfill by household. |
| `num_households`                                          | Number of households. |
| `household_waste_arisings_per_household`                  | Household waste arisings per household. |
| `population`                                              | Population of the area. |
| `household_waste_arisings_per_capita`                     | Household waste arisings per capita. |
| `waste_from_households_recycling`                         | Waste from households sent for recycling. |
| `waste_from_households_arisings`                          | Total waste arisings from households. |
| `waste_from_households_recycling_rate`                    | Rate of recycling from household waste. |
| `year`                                                    | Year of the data. |


# How to Run Dashboard on your Local?
Before you begin, ensure you have met the following requirements:
- You have installed [Git](https://git-scm.com/downloads).
- You have installed [Python](https://www.python.org/downloads/) 3.6 or higher.
- You have installed [Visual Studio Code (VS Code)](https://code.visualstudio.com/).

### Cloning the Repository

1. Open Visual Studio Code.
2. Open the integrated **terminal** in VS Code by selecting `Terminal` > `New Terminal` from the top menu.
3. Clone the repository using the following command:

```
git clone https://github.com/roniantoniius/Dashboard-Waste-Management.git
```

4. Navigate to the project directory:
```
cd Dashboard-Waste-Management
```

### Setting Up a Virtual Environment
1. Create a virtual environment. You can name the environment `venv`:
```
python -m venv venv
```
2. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
3. Install the required packages from the `requirements.txt` file:
```
pip install -r requirements.txt
```

### Running the Application
```
python app2.py
```

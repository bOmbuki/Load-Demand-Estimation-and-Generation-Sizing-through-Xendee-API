import pandas
import requests
from requests.auth import HTTPBasicAuth
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

""" API code to communicate with xendee servers to facilitate batch techno-economic analysis """

xendeeAPIbaseUrl = config.get('credentials', 'baseurl')
xendeeAPIUsername = config.get('credentials', 'username')
xendeeAPIPassword = config.get('credentials', 'password')
xendeeAPIUserId = config.get('credentials', 'userid')

basic = HTTPBasicAuth(xendeeAPIUsername, xendeeAPIPassword)

# Adjustable variables
Sites = pandas.read_csv("FijiSites.csv", index_col=None)

Folder = "Test Beta"
# resultsFolder = "results"

# Non adjustable variables
validWebIds = []
webIDProjectNames = []
resultIds = []

load_data = pandas.read_csv('Load Profile.csv')
solar_data = pandas.read_csv('Solar Profile TS.csv')

print('\n________________Technoeconomic Optimization______________')

for index, site in Sites.iterrows():
    name = site["Site"]
    latitude = site["Latitude"]
    longitude = site["Longitude"]
    load_profile = load_data[name].tolist()
    solar_profile = solar_data[name].tolist()

    iteration = 1
    Name = name + str(iteration)

    Done = False

    while not Done:
        project = {
            "FolderName": Folder,
            "Name": Name,
            "UserId": xendeeAPIUserId,
            "GridConnected": False,
            "MetricUnits": False,
            "CurrencyId": "USD",
            "PayBackPeriodInYears": 0,
            "InterestRate": 6,
            "DiscountRate": 7,
            "FedTaxRate": 0,
            "ProjectAddress": name + ", Fiji",
            "ProjectYear": 2021,
            "Locale": "Fiji",
            "Latitude": latitude,
            "Longitude": longitude,
            "IncludeSolarPV": True,
            "IncludeBatteryStorage": True,
            "IncludeWind": False,
            "IncludeEVCharging": False,
            "IncludeGenerator": True,
            "IncludeFuelCell": False
        }

        response = requests.post(f'{xendeeAPIbaseUrl}/OptimizationProjects', json=project, auth=basic)
        #print(f"OptimizationProjects(Setup) - Status Code: {response.status_code}, Response: {response.json()}")
        print("OptimizationProjects(Setup) - Status Code:", response.status_code)
        print("Response:", response.json())
        print()

        webID = response.json()["results"]["OptimizationProjectId"]

        # LOAD PROFILE SECTION
        load_profile_payload = {
            "OptimizationProjectId": webID,
            "Type": "ElectricityOnly",
            "Resolution": 1,
            "StartDate": "2021-01-01T00:00:00",
            "Units": "kW",
            "PreservePeak": True,
            "TimeSeriesData": load_profile,
        }

        response = requests.post(f'{xendeeAPIbaseUrl}/LoadProfile', json=load_profile_payload, auth=basic)
        print(f"OptimizationProjects(Load Profile) - Status Code: {response.status_code}, Response: {response.content}")

        # SOLAR SECTION
        solar_payload = {
            "OptimizationProjectId": webID,
            "TechDetails": {
                "FixedInvest": False,
                "ExistingTech": False,
                "ForcedInvest": 0,
                "TechAge": 0,
                "MaxNewSize": -1
            },
            "Costs": {
                "InverterCost": 632.33,
                "SolarPVCost": 568.6,
                "OtherProjectSpecificCosts": 0,
                "MaintenanceCosts": 0,
                "NonLinearCosts": None
            },
            "Incentives": {
                "FederalITC": 33,
                "FederalAmountDepreciable": 25,
                "FederalDepreciationSchedule": 7,
                "PTC": 0
            },
            "Details": {
                "Name": "JA 395W",
                "PanelLifetime": 20,
                "InverterLifetime": 15,
                "MaxSpace": 0,
                "PVExport": False
            },
            "PerformanceData": {
                "Description": "Joey Data",
                "Year": 2021,
                "Resolution": 1,
                "TotalSystemEfficiency": 21,
                "TimeSeriesData": solar_profile
            }
        }

        response = requests.post(f'{xendeeAPIbaseUrl}/SolarPV', json=solar_payload, auth=basic)
        print(f"OptimizationProjects(Solar) - Status Code: {response.status_code}, Response: {response.content}")

        # BATTERY SECTION
        BAE_Payload = {
            "OptimizationProjectId": webID,
            "TechDetails": {
                "FixedInvest": False,
                "ExistingTech": False,
                "ForcedInvest": 0,
                "TechAge": 0,
                "MaxNewSize": -1
            },
            "Costs": {
                "CapitalCostTechnology": 114.67,
                "InverterCost": 577.78,
                "OtherProjectSpecificCosts": 0,
                "MaintenanceCosts": 0,
            },
            "Incentives": {
                "FederalITC": 33,
                "FederalAmountDepreciable": 25,
                "FederalDepreciationSchedule": 7
            },
            "Details": {
                "Name": "BAE",
                "Lifetime": 5,
                "ChargingEfficiency": 90,
                "DischargingEfficiency": 90,
                "MaxChargeRate": 0.3,
                "MaxDischargeRate": 0.25,
                "MinSOC": 50,
                "MaxSOC": 100,
                "UnitSize": 1.31,
                "ChargeFromUtility": False,
                "MaxCyclesPerYear": 52,
                "Export": False
            }
        }

        response = requests.post(f'{xendeeAPIbaseUrl}/BatteryStorage', json=BAE_Payload, auth=basic)
        print(f"OptimizationProjects(Battery) - Status Code: {response.status_code}, Response: {response.content}")

        # GENERATOR SECTION
        FGWilson65_Payload = {
            "OptimizationProjectId": webID,
            "TechDetails": {
                "FixedInvest": False,
                "ExistingTech": False,
                "ForcedInvest": 0,
                "TechAge": 0,
                "MaxNewSize": -1
            },
            "Costs": {
                "PurchasePrice": 17239,
                "FixedMaintenanceCosts": 0.0000,
                "VariableMaintenanceCosts": 0.120000000,
                "NonLinearCosts": None
            },
            "Incentives": {
                "FederalITC": 33,
                "FederalAmountDepreciable": 25,
                "FederalDepreciationSchedule": 7,
                "PTC": 0
            },
            "Details": {
                "Name": "FGWilson65",
                "Capacity": 52,
                "Lifetime": 2,
                "Fuel": 4,
                "GeneratorType": "DG",
                "ElectricEfficiency": 30.00,
                "HeatToPowerRatio": None,
                "MinLoad": 60.00,
                "BackupOnly": True,
                "Export": False
            }
        }

        response = requests.post(f'{xendeeAPIbaseUrl}/Generator', json=FGWilson65_Payload, auth=basic)
        print(f"OptimizationProjects(Generator) - Status Code: {response.status_code}, Response: {response.content}")


        # RUNNING OPTIMIZATION
        economic_optimization = {
            "OptimizationProjectId": webID,
            "Name": Name + ", Fiji",
            "OptimizeCost": True,
            "OptimizeCO2": False,
            "Latitude": latitude,
            "Longitude": longitude,
            "OptimizeResilience": False,
            "OptimizeRedundancy": False,
            "OptimizeCostMultiplier": None,
            "OptimalGap": 1.5,
            "ReferenceCost": 100000000,  # this must match ReferenceEmissions either None or an integer >0<1,000,000,000
            "ReferenceEmissions": 100000,  # this must match ReferenceCost either None or an integer >0<1,000,000,000
            "TimeSeriesOptimization": False,
            "TimeSeriesReadingsPerHour": 1,
            "UpdateTemperatureData": True
        }

        response = requests.post(f'{xendeeAPIbaseUrl}/EconomicOptimization', json=economic_optimization, auth=basic)

        print(f"OptimizationProjects(Final) - Status Code: {response.status_code}, Response: {response.content}")
        resultID = response.json()["results"]["OptimizationProjectResultId"]

        if response.status_code == 201:
            Done = True
            validWebIds.append(webID)
            webIDProjectNames.append(Name)
            resultIds.append(resultID)
        else:
            print('Recalculating....')
            response = requests.delete(f'{xendeeAPIbaseUrl}/OptimizationProjects?optimizationProjectId={webID}', json=0,
                                       auth=basic)

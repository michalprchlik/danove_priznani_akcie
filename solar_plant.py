

import logging
import requests
import growattServer


from backoff import on_exception, constant
from rest_framework import status


def handle_solar_plant(token, current_price, solar_plant_1_price, solar_plant_2_price):
    get_solar_plant_info(token)

    if current_price > solar_plant_1_price:
        turn_on_solar_plant()
    else:
        turn_off_solar_plant()

    if current_price > solar_plant_2_price:
        turn_on_solar_plant()
    else:
        turn_off_solar_plant()



def get_solar_plant_info(token):
    try:

        # Initialize the API with token instead of using login
        api = growattServer.OpenApiV1(token=token)

        print(api)

        # Plant info
        plants = api.plant_list()
        print(plants)
        print(f"Plants: Found {plants['count']} plants")


        plants = api.dashboard_data()
        print('------')
        print(plants)
        print('------')

        plant_id = plants['plants'][0]['plant_id']

        # Devices
        devices = api.device_list(plant_id)

        for device in devices['devices']:
            if device['type'] == 7:  # (MIN/TLX)
                inverter_sn = device['device_sn']
                print(f"Processing inverter: {inverter_sn}")

                # Get device details
                inverter_data = api.min_detail(inverter_sn)
                print("Saving inverter data to inverter_data.json")
                with open('inverter_data.json', 'w') as f:
                    json.dump(inverter_data, f, indent=4, sort_keys=True)

                # Get energy data
                energy_data = api.min_energy(device_sn=inverter_sn)
                print("Saving energy data to energy_data.json")
                with open('energy_data.json', 'w') as f:
                    json.dump(energy_data, f, indent=4, sort_keys=True)

                # Get energy history
                energy_history_data = api.min_energy_history(inverter_sn)
                print("Saving energy history data to energy_history.json")
                with open('energy_history.json', 'w') as f:
                    json.dump(energy_history_data['datas'],
                            f, indent=4, sort_keys=True)

                # Get settings
                settings_data = api.min_settings(device_sn=inverter_sn)
                print("Saving settings data to settings_data.json")
                with open('settings_data.json', 'w') as f:
                    json.dump(settings_data, f, indent=4, sort_keys=True)

                # Read time segments
                tou = api.min_read_time_segments(inverter_sn, settings_data)
                print(json.dumps(tou, indent=4))

                # Read discharge power
                discharge_power = api.min_read_parameter(
                    inverter_sn, 'discharge_power')
                print("Current discharge power:", discharge_power, "%")

                # Settings parameters - Uncomment to test

                # Turn on AC charging
    #            api.min_write_parameter(inverter_sn, 'ac_charge', 1)
    #            print("AC charging enabled successfully")

                # Enable Load First between 00:00 and 11:59 using time segment 1
    #            api.min_write_time_segment(
    #                device_sn=inverter_sn,
    #                segment_id=1,
    #                batt_mode=growattServer.BATT_MODE_BATTERY_FIRST,
    #                start_time=datetime.time(0, 0),
    #                end_time=datetime.time(00, 59),
    #                enabled=True
    #            )
    #            print("Time segment updated successfully")


    except growattServer.GrowattV1ApiError as e:
        print(f"API Error: {e} (Code: {e.error_code}, Message: {e.error_msg})")

    except growattServer.GrowattParameterError as e:
        print(f"Parameter Error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

def turn_on_solar_plant():
    logging.info('turn_on_solar_plant')

    pass


def turn_off_solar_plant():
    logging.info('turn_off_solar_plant')

    pass







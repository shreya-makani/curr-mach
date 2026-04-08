from quantum.CoreEngine import CoreEngine
import json
import requests

class MyMachine(CoreEngine):
    input_data = {}
    dependent_machine_data = {}

    def __init__(self):
        super().__init__()

    def receiving(self, input_data, dependent_machine_data, callback):
        data = {}
        error_list = []
        try:
            data = self.get_final_data()
            error_list = self.get_error_list()
            self.input_data = input_data
            self.dependent_machine_data = dependent_machine_data
            
            # Validate input data
            if 'amount' not in self.input_data or 'from_currency' not in self.input_data or 'to_currency' not in self.input_data:
                raise ValueError("Missing required input parameters.")

        except Exception as e:
            error_list.append(f"Error : {str(e)}")
        finally:
            callback(data, error_list)

    def pre_processing(self, callback):
        data = {}
        error_list = []
        try:
            data = self.get_final_data()
            error_list = self.get_error_list()
            
            # No specific pre-processing needed for this machine
            
        except Exception as e:
            error_list.append(f"Error : {str(e)}")
        finally:
            callback(data, error_list)

    def processing(self, callback):
        data = {}
        error_list = []
        try:
            data = self.get_final_data()
            error_list = self.get_error_list()
            
            # Fetch exchange rate from an external API
            api_url = "https://api.exchangerate-api.com/v4/latest/" + self.input_data['from_currency']
            response = requests.get(api_url)
            if response.status_code != 200:
                raise Exception("Failed to fetch exchange rates.")

            rates = response.json().get('rates', {})
            if self.input_data['to_currency'] not in rates:
                raise ValueError("Target currency not available.")

            exchange_rate = rates[self.input_data['to_currency']]
            converted_amount = self.input_data['amount'] * exchange_rate

            # Write the result to a file
            result = {
                "converted_amount": converted_amount,
                "exchange_rate": exchange_rate
            }
            self.write_file('output.json', data=result)

        except Exception as e:
            error_list.append(f"Error : {str(e)}")
        finally:
            callback(data, error_list)

    def post_processing(self, callback):
        data = {}
        error_list = []
        try:
            data = self.get_final_data()
            error_list = self.get_error_list()
            
            # No specific post-processing needed for this machine
            
        except Exception as e:
            error_list.append(f"Error : {str(e)}")
        finally:
            callback(data, error_list)

    def packaging_shipping(self, callback):
        data = {}
        error_list = []
        try:
            data = self.get_final_data()
            error_list = self.get_error_list()
            
            # No specific packaging logic needed for this machine
            
        except Exception as e:
            error_list.append(f"Error : {str(e)}")
        finally:
            callback(data, error_list)

if __name__ == '__main__':
    machine = MyMachine()
    machine.start()

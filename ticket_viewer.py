import requests
from requests.exceptions import HTTPError
import json
import pandas as pd
from tabulate import tabulate
import re
import textwrap

class ticket_viewer:

    def __init__(self, user= 'shreyanssakhlecha@gmail.com' + '/token', pwd = 'Qapoz3sFCneeu2cLFzEWGJoQufPkR17xolryrnmR'):
        self.user = user
        self.pwd = pwd

    def list_api_call(self, url= 'https://zccstudentshelp.zendesk.com/api/v2/tickets.json', param = {'page[size]':'25'}):
        try:
            response = requests.get(url, auth=(self.user, self.pwd), params=param)
            response.raise_for_status()
            return response
        except HTTPError as http_err:
            if response.status_code == 400:
                print(f'Bad request, make sure you typed everything correctly. {http_err}')
            elif response.status_code == 403:
                print(f'The user does not have permission for api call. {http_err}')
            elif response.status_code == 404:
                print(f'Check if the url entered is correct. {http_err}')
            else:
                print(f'HTTP error occurred: {http_err}')
        except Exception as err:
                print(f'Other error occurred: {err}')

    def list_reformat(self, response):

        def wrap(row):
            return '\n'.join(re.findall('.{1,60}', row))

        if response:
            df =pd.DataFrame(response['tickets'])
            if not df.empty:
                df.fillna("Unknown", inplace=True)
                data = df.loc[:, ['id', 'created_at', 'subject', 'priority', 'status', 'description']]
                desc_wraped = data.description.apply(wrap)
                del data['description']
                data['description'] = desc_wraped
                return data
        else:
            print("No tickets available to show!")


def main():
    obj = ticket_viewer()
    x = obj.list_api_call()
    data = obj.list_reformat(x.json())
    print(data)

if __name__ == "__main__":
    main()



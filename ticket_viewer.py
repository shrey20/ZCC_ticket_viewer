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
        while url:
            try:
                response = requests.get(url, auth=(self.user, self.pwd), params=param)
                response.raise_for_status()
                return response
            except HTTPError as http_err:
                if response.status_code == 400:
                    print('{0:s}: Bad request, make sure you typed everything correctly'.format(http_err))
                elif response.status_code == 403:
                    print('{0:s}: The user does not have permission for api call'.format(http_err))
                elif response.status_code == 400:
                    print('{0:s}: Check if the url entered is correct')
                else:
                    print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                    print(f'Other error occurred: {err}')

def main():
    obj = ticket_viewer()
    x = obj.list_api_call()
    print (x.json())

if __name__ == "__main__":
    main()



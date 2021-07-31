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

    def list_reformat(self, response_json):

        def wrap(row):
            return '\n'.join(re.findall('.{1,60}', row))

        if response_json:
            df =pd.DataFrame(response_json['tickets'])
            if not df.empty:
                df.fillna("Unknown", inplace=True)
                data = df.loc[:, ['id', 'created_at', 'subject', 'priority', 'status', 'description']]
                desc_wraped = data.description.apply(wrap)
                del data['description']
                data['description'] = desc_wraped
                return data
        else:
            print("No tickets available to show!")

    def display_list(self, response_json):

        while True:
            print("Menu:")
            print("1. Type 'next': To go to next page ")
            print("2. Type 'prev': To go to previous page")
            print("3. Type 'exit': To return to main menu")
            x = input("Choose option:")
            if x in ['next', 'prev']:
                if response_json['meta']['has_more']:
                    new_url = response_json['links'][x]
                    #print(new_url)
                    move = self.list_api_call(new_url)
                    if move:
                        response_json = move.json()
                        data = self.list_reformat(move.json())
                        print(tabulate(data, headers="keys", tablefmt='fancy_grid'))

                else:
                    print("No more pages available!")
                    print("Returning to main menu!")
                    return
            elif x == 'exit':
                print("Returning to main menu!")
                return
            else:
                print("Please input a valid option")



    def single_api_call(self, id):
        url = 'https://zccstudentshelp.zendesk.com/api/v2/tickets/' + str(id) + '.json'

        try:
            response = requests.get(url, auth=(self.user, self.pwd))
            response.raise_for_status()
            return response

        except HTTPError as http_err:
            if response.status_code == 404:
                print("Please enter a valid ticket id.")
            else:
                print(f'HTTP error occurred: {http_err}')

        except Exception as err:
            print(f'Other error occurred: {err}')

    def display_single(self, response_json):
        data = response_json['ticket']
        print("id: {0:d}".format(data['id'])) if data['id'] else print("id: Unknown")
        print("created at: {0:s}".format(data['created_at'])) if data['created_at'] else print("created_at: Unknown")
        print("subject: {0:s}".format(data['subject'])) if data['subject'] else print("subject: Unknown")
        print("priority: {0:s}".format(data['priority'])) if data['priority'] else print("priority: Unknown")
        print("status: {0:s}".format(data['status'])) if data['status'] else print("status: Unknown")
        if not data['description']:
            print("Description: Unknown")
        else:
            desc_wrap = textwrap.wrap(data['description'], width=70)
            print("description:")
            for text in desc_wrap:
                print(text)


def main():
    obj = ticket_viewer()
    print("Hello User!")

    while True:
        print()
        print("Main Menu")
        print("Enter 1: To view a single ticket (requires id)")
        print("Enter 2: To view a list of tickets")
        print("Enter 3: To exit")
        user_input = input("Choose option:")

        if user_input == "1":
            tick_id = int(input("Please enter ticket id:"))
            response = obj.single_api_call(tick_id)
            if response:
                obj.display_single(response.json())

        elif user_input == "2":
            response = obj.list_api_call()
            if response:
                data = obj.list_reformat(response.json())
                if not data.empty:
                    print(tabulate(data, headers="keys", tablefmt='fancy_grid'))
                    obj.display_list(response.json())

        elif user_input == "3":
            print("Closing application!")
            return

        else:
            print("Please choose a valid option")


if __name__ == "__main__":
    main()



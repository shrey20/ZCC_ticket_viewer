import json
import os
import pytest
import unittest
from unittest.mock import patch
from ticket_viewer import ticket_viewer


def test_list_api_call(capsys):
    """
    Checks if the list_api_call works for given credentials and url
    :param capsys: Captures stdout and stderr
    """

    obj1 = ticket_viewer()
    obj2 = ticket_viewer(pwd=os.environ.get('zcc_pwd2'))
    obj3 = ticket_viewer(pwd="abcd")

    # mocks get request for ticket_viewer module and verifies if the right get request is made

    with patch('ticket_viewer.requests.get') as mocked_get:
        obj1.list_api_call()
        mocked_get.assert_called_with('https://zccstudentshelp.zendesk.com/api/v2/tickets.json',
                                      auth=(os.environ.get('zcc_user') + '/token', os.environ.get('zcc_pwd1')),
                                      params={'page[size]': '25'})

    with patch('ticket_viewer.requests.get') as mocked_get:
        obj2.list_api_call()
        mocked_get.assert_called_with('https://zccstudentshelp.zendesk.com/api/v2/tickets.json',
                                      auth=(os.environ.get('zcc_user') + '/token', os.environ.get('zcc_pwd2')),
                                      params={'page[size]': '25'})

    with patch('ticket_viewer.requests.get') as mocked_get:
        obj3.list_api_call()
        mocked_get.assert_called_with('https://zccstudentshelp.zendesk.com/api/v2/tickets.json',
                                      auth=(os.environ.get('zcc_user') + '/token', "abcd"),
                                      params={'page[size]': '25'})

    with patch('ticket_viewer.requests.get') as mocked_get:
        obj1.list_api_call(url="https://zccstudentshelp.zendesk.com/api/v2/tic")
        mocked_get.assert_called_with("https://zccstudentshelp.zendesk.com/api/v2/tic",
                                      auth=(os.environ.get('zcc_user') + '/token', os.environ.get('zcc_pwd1')),
                                      params={'page[size]': '25'})


def test_list_reformat(capsys):
    """
    Checks if the method returns the correct dataframe for a given response
    (Or output message for no response)
    :param capsys: Captures stdout and stderr
    """

    obj = ticket_viewer()

    # retrives data which contains information corresponding to a page of tickets
    with open("list_data.json", "r") as a_file:
        response_json = json.load(a_file)
        data_frame = obj.list_reformat(response_json)

        if set(['id', 'created_at', 'subject', 'priority', 'status', 'description']).issubset(data_frame.columns):
            assert True

        else:
            assert False

        assert data_frame['id'][10] == 11
        assert data_frame['priority'][20] == "Unknown"
        assert data_frame['status'][15] == 'open'
        assert data_frame['created_at'][17] == '2021-07-28T12:58:12Z'

    response = None
    obj.list_reformat(response)
    captured = capsys.readouterr()
    assert captured.out == "No tickets available to show!\n"


def test_single_api_call(capsys):
    """
    Checks if single_api_call returns correct response for a given id and credentials
    :param capsys: Captures stdout and stderr
    """

    obj1 = ticket_viewer()
    obj2 = ticket_viewer(pwd="abcd")

    #checks if the correct get request is made for different credentials and ids
    with patch('ticket_viewer.requests.get') as mocked_get:
        obj1.single_api_call(1)
        mocked_get.assert_called_with('https://zccstudentshelp.zendesk.com/api/v2/tickets/1.json',
                                      auth=(os.environ.get('zcc_user') + '/token', os.environ.get('zcc_pwd1')))

    with patch('ticket_viewer.requests.get') as mocked_get:
        obj1.single_api_call(10)
        mocked_get.assert_called_with('https://zccstudentshelp.zendesk.com/api/v2/tickets/10.json',
                                      auth=(os.environ.get('zcc_user') + '/token', os.environ.get('zcc_pwd1')))

    with patch('ticket_viewer.requests.get') as mocked_get:
        obj1.single_api_call(50)
        mocked_get.assert_called_with('https://zccstudentshelp.zendesk.com/api/v2/tickets/50.json',
                                      auth=(os.environ.get('zcc_user') + '/token', os.environ.get('zcc_pwd1')))

    with patch('ticket_viewer.requests.get') as mocked_get:
        obj2.single_api_call(50)
        mocked_get.assert_called_with('https://zccstudentshelp.zendesk.com/api/v2/tickets/50.json',
                                      auth=(os.environ.get('zcc_user') + '/token', "abcd"))


def test_display_single(capsys):
    """
    Checks if the correct output is displayed for given data
    We don't have to when response is null as the function isn't
    called in that scenario
    :param capsys: Captures stdout and stderr
    """

    obj1 = ticket_viewer()

    #loads the data for various ticket ids and checks if the correct output is displayed
    with open("data1.json", "r") as a_file:
        response_json = json.load(a_file)
        obj1.display_single(response_json)
        captured = capsys.readouterr()

        assert "id: 1" in captured.out
        assert "priority: Unknown" in captured.out
        assert "subject: Unknown" in captured.out

    with open("data10.json", "r") as a_file:
        response_json = json.load(a_file)
        obj1.display_single(response_json)
        captured = capsys.readouterr()

        assert "id: 10" in captured.out
        assert "priority: Unknown" in captured.out
        assert "subject: magna reprehenderit nisi est cillum" in captured.out

    with open("data50.json", "r") as a_file:
        response_json = json.load(a_file)
        obj1.display_single(response_json)
        captured = capsys.readouterr()

        assert "id: 50" in captured.out
        assert "priority: Unknown" in captured.out
        assert "subject: officia magna velit nostrud ullamco" in captured.out

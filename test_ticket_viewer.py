import pytest
from ticket_viewer import ticket_viewer
from ticket_viewer import main


def test_list_api_call(capsys):
    """
    Checks if the list_api_call works for given credentials and url
    :param capsys: Captures stdout and stderr
    """

    # obj1 and obj2 have valid credential while obj3 has invalid credentials
    obj1 = ticket_viewer()
    obj2 = ticket_viewer(pwd="e081nL1b2wzlokyTQMcsHHutYMKScLkyEqc1KbUz")
    obj3 = ticket_viewer(pwd= "abcd")


    response = obj1.list_api_call()
    if response:
        assert response.status_code == 200
        assert response.url == "https://zccstudentshelp.zendesk.com/api/v2/tickets.json?page%5Bsize%5D=25"

    response = obj2.list_api_call()
    if response:
        assert response.status_code == 200
        assert response.url == "https://zccstudentshelp.zendesk.com/api/v2/tickets.json?page%5Bsize%5D=25"

    #Accessing the api with invalid credential
    obj3.list_api_call()
    captured = capsys.readouterr()
    assert "HTTP error occurred: 401 Client Error:" in captured.out

    #Passing in the wrong url
    obj1.list_api_call(url="https://zccstudentshelp.zendesk.com/api/v2/tic")
    captured = capsys.readouterr()
    assert "Check if the url entered is correct. 404 Client Error:" in captured.out


def test_list_reformat(capsys):
    """
    Checks if the method returns the correct dataframe for a given response
    (Or output message for no response)
    :param capsys: Captures stdout and stderr
    """
    obj = ticket_viewer()

    response = obj.list_api_call()
    if response:
        data_frame = obj.list_reformat(response.json())

        if not data_frame.empty:
            if set(['id', 'created_at', 'subject', 'priority', 'status', 'description']).issubset(data_frame.columns):
                assert True

            else:
                assert False


        response = None
        obj.list_reformat(response)
        captured = capsys.readouterr()
        assert captured.out == "No tickets available to show!\n"


def test_single_api_call(capsys):
    """
    Checks if single_api_call returns correct response for a given id and credentials
    :param capsys: Captures stdout and stderr
    """

    #obj1 has valid credentials while obj2 has invalid credentials
    obj1 = ticket_viewer()
    obj2 = ticket_viewer(pwd="abcd")
    exist = False # Flag to check whether id exists in the database

    #Check response for various ticket ids
    response = obj1.single_api_call(1)
    if response:
        assert response.json()['ticket']['id'] == 1
        assert response.url == "https://zccstudentshelp.zendesk.com/api/v2/tickets/1.json"

        exist = True

    else:
        captured = capsys.readouterr()
        assert captured.out == "Please enter a valid ticket id.\n"

    response = obj1.single_api_call(10)
    if response:
        assert response.json()['ticket']['id'] == 10
        assert response.url == "https://zccstudentshelp.zendesk.com/api/v2/tickets/10.json"

    else:
        captured = capsys.readouterr()
        assert captured.out == "Please enter a valid ticket id.\n"


    response = obj1.single_api_call(50)
    if response:
        assert response.json()['ticket']['id'] == 50
        assert response.url == "https://zccstudentshelp.zendesk.com/api/v2/tickets/50.json"

    else:
        captured = capsys.readouterr()
        assert captured.out == "Please enter a valid ticket id.\n"


    obj1.single_api_call(1087)
    captured = capsys.readouterr()
    assert captured.out == "Please enter a valid ticket id.\n"

    if exist:
        obj2.single_api_call(1)
        captured = capsys.readouterr()
        assert "HTTP error occurred: 401 Client Error:" in captured.out


def test_display_single(capsys):
    """
    Checks if the correct output is displayed for given data
    :param capsys: Captures stdout and stderr
    """

    obj1 = ticket_viewer()

    response = obj1.single_api_call(1)
    if response:
        obj1.display_single(response.json())
        captured = capsys.readouterr()
        assert "id: 1" in captured.out

    response = obj1.single_api_call(10)
    if response:
        obj1.display_single(response.json())
        captured = capsys.readouterr()
        assert "id: 10" in captured.out

    response = obj1.single_api_call(50)
    if response:
        obj1.display_single(response.json())
        captured = capsys.readouterr()
        assert "id: 50" in captured.out









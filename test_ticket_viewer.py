import pytest
from ticket_viewer import ticket_viewer


def test_list_api_call(capsys):
    obj1 = ticket_viewer()
    obj2 = ticket_viewer(pwd="e081nL1b2wzlokyTQMcsHHutYMKScLkyEqc1KbUz")
    obj3 = ticket_viewer(pwd= "abcd")


    response = obj1.list_api_call()
    assert response.status_code == 200

    response = obj2.list_api_call()
    assert response.status_code == 200

    obj3.list_api_call()
    captured = capsys.readouterr()
    # print(captured.out[:123])
    assert captured.out[:59] == "HTTP error occurred: 401 Client Error: Unauthorized for url"

    obj1.list_api_call(url="https://zccstudentshelp.zendesk.com/api/v2/tic")
    captured = capsys.readouterr()
    assert captured.out[:72] == "Check if the url entered is correct. 404 Client Error: Not Found for url"


def test_list_reformat(capsys):
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
    obj1 = ticket_viewer()
    obj2 = ticket_viewer(pwd="abcd")
    exist = False

    response = obj1.single_api_call(1)
    if response:
        assert response.json()['ticket']['id'] == 1
        exist = True

    response = obj1.single_api_call(10)
    if response:
        assert response.json()['ticket']['id'] == 10

    response = obj1.single_api_call(50)
    if response:
        assert response.json()['ticket']['id'] == 50

    obj1.single_api_call(1087)
    captured = capsys.readouterr()
    assert captured.out == "Please enter a valid ticket id.\n"

    if exist:
        obj2.single_api_call(1)
        captured = capsys.readouterr()
        assert captured.out[:59] == "HTTP error occurred: 401 Client Error: Unauthorized for url"



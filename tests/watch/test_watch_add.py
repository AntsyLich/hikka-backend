from client_requests import request_watch_add
from client_requests import request_watch
from sqlalchemy import select, desc
from app.models import Log
from fastapi import status
from app import constants


async def test_watch_add(
    client,
    create_test_user,
    aggregator_anime,
    get_test_token,
    test_session,
):
    # Add anime to watch list
    response = await request_watch_add(
        client,
        "bocchi-the-rock-9e172d",
        get_test_token,
        {
            "status": "watching",
            "note": "Test",
            "episodes": 10,
            "score": 8,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["anime"]["slug"] == "bocchi-the-rock-9e172d"
    assert response.json()["status"] == "watching"
    assert response.json()["rewatches"] == 0
    assert response.json()["episodes"] == 10
    assert response.json()["note"] == "Test"
    assert response.json()["score"] == 8

    # Check log
    log = await test_session.scalar(select(Log).order_by(desc(Log.created)))
    assert log.log_type == constants.LOG_WATCH_CREATE
    assert log.user == create_test_user
    assert log.data == {
        "after": {
            "episodes": 10,
            "note": "Test",
            "rewatches": 0,
            "score": 8,
            "status": "watching",
        },
        "before": {
            "episodes": None,
            "note": None,
            "rewatches": None,
            "score": None,
            "status": None,
        },
    }

    # Update watch list entry
    response = await request_watch_add(
        client,
        "bocchi-the-rock-9e172d",
        get_test_token,
        {
            "status": "completed",
            "note": "Good anime!",
            "rewatches": 2,
            "episodes": 12,
            "score": 10,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["anime"]["slug"] == "bocchi-the-rock-9e172d"
    assert response.json()["status"] == "completed"
    assert response.json()["note"] == "Good anime!"
    assert response.json()["rewatches"] == 2
    assert response.json()["episodes"] == 12
    assert response.json()["score"] == 10

    # Check whether Bocchi is in user's watch list again
    response = await request_watch(
        client, "bocchi-the-rock-9e172d", get_test_token
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["anime"]["slug"] == "bocchi-the-rock-9e172d"
    assert response.json()["score"] == 10

    # Check log
    log = await test_session.scalar(select(Log).order_by(desc(Log.created)))
    assert log.log_type == constants.LOG_WATCH_UPDATE
    assert log.user == create_test_user
    assert log.data == {
        "after": {
            "episodes": 12,
            "note": "Good anime!",
            "rewatches": 2,
            "score": 10,
            "status": "completed",
        },
        "before": {
            "episodes": 10,
            "note": "Test",
            "rewatches": 0,
            "score": 8,
            "status": "watching",
        },
    }

from client_requests import request_characters_info
from fastapi import status


async def test_characters_info(client, aggregator_characters):
    # Get individual character info
    response = await request_characters_info(client, "levi-565409")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name_en"] == "Levi"
    assert response.json()["slug"] == "levi-565409"

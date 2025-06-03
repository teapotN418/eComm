from .conftest import AsyncClient, settings
import pytest

@pytest.fixture()
async def test_product_data():
    return {"id": 100, "q": 5}

@pytest.fixture()
async def test_product_data_2():
    return {"id": 200, "q": 30}

async def test_get_cart(client: AsyncClient):
    response = await client.get("/cart")
    assert response.status_code == 200
    assert response.json()["pr"] == []

async def test_post_items(client: AsyncClient, test_product_data: dict):
    assert not settings.CART_COOKIE_LOCATION in client.cookies
    
    response = await client.post("/cart/items", json=test_product_data)
    assert response.status_code == 200
    client.cookies = dict(response.cookies)
    assert settings.CART_COOKIE_LOCATION in client.cookies
    
    response = await client.get("/cart")
    assert response.status_code == 200
    assert response.json()["pr"] == [test_product_data]

async def test_delete_cart(client: AsyncClient):
    response = await client.post("/cart/items", json={"id": 100, "q": 5})
    client.cookies = dict(response.cookies)
    
    response = await client.get("/cart")
    assert response.json()["pr"] != []
    
    response = await client.delete("/cart")
    client.cookies = dict(response.cookies)
    
    response = await client.get("/cart")
    assert response.json()["pr"] == []

async def test_put_delete_items(client: AsyncClient, test_product_data: dict, test_product_data_2: dict):
    new_quantity = 10
    
    new_data = test_product_data
    new_data["q"] = new_quantity
    
    id = test_product_data["id"]

    response = await client.post("/cart/items", json=test_product_data)
    client.cookies = dict(response.cookies)
    
    response = await client.post("/cart/items", json=test_product_data_2)
    client.cookies = dict(response.cookies)
    
    response = await client.put(f"/cart/items/{id}?quantity={new_quantity}")
    assert response.status_code == 200
    assert response.json()["pr"] == [new_data, test_product_data_2]
    client.cookies = dict(response.cookies)
    
    response = await client.delete(f"/cart/items/{id}")
    assert response.status_code == 200
    assert response.json()["pr"] == [test_product_data_2]

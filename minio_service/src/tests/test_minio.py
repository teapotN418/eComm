from .conftest import AsyncClient
import pytest
import io
import uuid

@pytest.fixture
def admin_headers():
    return {
        "x-user-id": "1",
        "x-user-role": "admin"
    }

@pytest.fixture
def non_admin_headers():
    return {
        "x-user-id": "2",
        "x-user-role": "user"
    }

@pytest.fixture
def mock_image_file():
    file_data = io.BytesIO(b"fake image data")
    file_data.name = "test_image.jpg"
    return file_data

async def test_upload_admin(client, admin_headers, mock_image_file):
    files = {"file": ("test_image.jpg", mock_image_file, "image/jpeg")}
    response = await client.post(
        "/files/upload/file",
        files=files,
        headers=admin_headers
    )
    
    assert response.status_code == 200
    assert "file_id" in response.json()

async def test_upload_forbidden(client, non_admin_headers, mock_image_file):
    files = {"file": ("test_image.jpg", mock_image_file, "image/jpeg")}
    response = await client.post(
        "/files/upload/file",
        files=files,
        headers=non_admin_headers
    )
    
    assert response.status_code == 403

async def test_upload_wrong(client, admin_headers):
    file_data = io.BytesIO(b"fake text data")
    files = {"file": ("test.txt", file_data, "text/plain")}
    response = await client.post(
        "/files/upload/file",
        files=files,
        headers=admin_headers
    )
    
    assert response.status_code == 400

async def test_get(client, admin_headers, mock_image_file):
    files = {"file": ("test_image.jpg", mock_image_file, "image/jpeg")}
    response = await client.post(
        "/files/upload/file",
        files=files,
        headers=admin_headers
    )
    file_id = response.json()["file_id"]
    
    response = await client.get(f"/files/get-url/{file_id}")
    
    assert response.status_code == 200

async def test_get_wrong(client):
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/files/get-url/{fake_id}")
    
    assert response.status_code == 404

async def test_no_headers(client, mock_image_file):
    files = {"file": ("test_image.jpg", mock_image_file, "image/jpeg")}
    response = await client.post(
        "/files/upload/file",
        files=files
    )
    
    assert response.status_code == 422
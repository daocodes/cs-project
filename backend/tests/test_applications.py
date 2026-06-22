def test_create_and_get_application(client, job_posting):
    create_response = client.post("/applications", json={**job_posting, "status": "SAVED"})
    assert create_response.status_code == 201
    application_id = create_response.json()["id"]

    get_response = client.get(f"/applications/{application_id}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "SAVED"


def test_list_applications_by_user(client, job_posting):
    client.post("/applications", json={**job_posting, "status": "SAVED"})

    response = client.get("/applications", params={"user_id": job_posting["user_id"]})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_patch_status_creates_status_event(client, job_posting):
    create_response = client.post("/applications", json={**job_posting, "status": "SAVED"})
    application_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/applications/{application_id}", json={"status": "APPLIED"}
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "APPLIED"

    events_response = client.get(f"/applications/{application_id}/status-events")
    assert events_response.status_code == 200
    events = events_response.json()
    assert len(events) == 1
    assert events[0]["from_status"] == "SAVED"
    assert events[0]["to_status"] == "APPLIED"


def test_delete_application(client, job_posting):
    create_response = client.post("/applications", json={**job_posting, "status": "SAVED"})
    application_id = create_response.json()["id"]

    delete_response = client.delete(f"/applications/{application_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/applications/{application_id}")
    assert get_response.status_code == 404


def test_get_missing_application_returns_404(client):
    response = client.get("/applications/999")
    assert response.status_code == 404


def test_delete_application_with_status_events(client, job_posting):
    create_response = client.post("/applications", json={**job_posting, "status": "SAVED"})
    application_id = create_response.json()["id"]
    client.patch(f"/applications/{application_id}", json={"status": "APPLIED"})

    delete_response = client.delete(f"/applications/{application_id}")
    assert delete_response.status_code == 204

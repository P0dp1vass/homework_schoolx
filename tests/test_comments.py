import pytest
@pytest.mark.asyncio
async def test_create_comment(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    task_res = await client.post("/tasks/", json={"title": "Task for comment"}, headers=headers)
    task_id = task_res.json()["id"]
    
    comment_data = {"text": "This is a test comment"}
    response = await client.post(f"/tasks/{task_id}/comments", json=comment_data, headers=headers)
    
    assert response.status_code == 201
    assert response.json()["text"] == "This is a test comment"
    assert response.json()["task_id"] == task_id

@pytest.mark.asyncio
async def test_create_comment_task_not_found(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = await client.post("/tasks/999/comments", json={"text": "Hello"}, headers=headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TASK_NOT_FOUND"

@pytest.mark.asyncio
async def test_get_comments(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    task_res = await client.post("/tasks/", json={"title": "Task with comments"}, headers=headers)
    task_id = task_res.json()["id"]
    
    await client.post(f"/tasks/{task_id}/comments", json={"text": "Comment 1"}, headers=headers)
    await client.post(f"/tasks/{task_id}/comments", json={"text": "Comment 2"}, headers=headers)
    
    response = await client.get(f"/tasks/{task_id}/comments", headers=headers)
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 2
    assert comments[0]["text"] == "Comment 1"
    assert comments[1]["text"] == "Comment 2"

@pytest.mark.asyncio
async def test_get_comments_task_not_found(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/tasks/999/comments", headers=headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TASK_NOT_FOUND"

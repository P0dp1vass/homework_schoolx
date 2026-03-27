def test_create_comment(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 1. Создаем задачу
    task_res = client.post("/tasks/", json={"title": "Task for comment"}, headers=headers)
    task_id = task_res.json()["id"]
    
    # 2. Оставляем комментарий
    comment_data = {"text": "This is a test comment"}
    response = client.post(f"/tasks/{task_id}/comments", json=comment_data, headers=headers)
    
    assert response.status_code == 201
    assert response.json()["text"] == "This is a test comment"
    assert response.json()["task_id"] == task_id

def test_create_comment_task_not_found(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Пытаемся оставить комментарий к несуществующей задаче
    response = client.post("/tasks/999/comments", json={"text": "Hello"}, headers=headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TASK_NOT_FOUND"

def test_get_comments(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    task_res = client.post("/tasks/", json={"title": "Task with comments"}, headers=headers)
    task_id = task_res.json()["id"]
    
    client.post(f"/tasks/{task_id}/comments", json={"text": "Comment 1"}, headers=headers)
    client.post(f"/tasks/{task_id}/comments", json={"text": "Comment 2"}, headers=headers)
    
    response = client.get(f"/tasks/{task_id}/comments", headers=headers)
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 2
    assert comments[0]["text"] == "Comment 1"
    assert comments[1]["text"] == "Comment 2"

def test_get_comments_task_not_found(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/tasks/999/comments", headers=headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TASK_NOT_FOUND"

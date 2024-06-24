from task.celery_task import send_email

result = send_email.delay("da")
print(result.id)
result2 = send_email.delay("li")
print(result2.id)

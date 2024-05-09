import uuid
import time 

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null = False)
    email = models.EmailField(null = False)
    password = models.CharField(max_length=50, null = False)
    
    def __str__(self):
        return (f"<name={self.name} user_id={self.id} email={self.email} password={self.password}")


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null = False)
    admin_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name = "admin_id")

    members = models.ManyToManyField(User, related_name = "members")

    def __str__(self):
        return (f"<group_name={self.name} group_id={self.id} admin_id={self.admin_id}")
    

class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null = False)
    group_id = models.ForeignKey(Group, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return (f"<title={self.title} page_id={self.id} group_id={self.group_id}")
    

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(null = False)
    page_id = models.ForeignKey(Page, null=False, on_delete=models.CASCADE)
    due_date = models.DateField()
    
    def __str__(self):
        return (f"<note={self.content} note_id={self.id} page_id={self.page_id} due_date={self.due_date}")
    
    
    
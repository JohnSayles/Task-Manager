s = "<group_name=Test Group group_id=f1edb9df-99b1-4127-885c-43c261078640 admin_id=<name=john user_id=aa29168b-b7e9-4261-a836-cef457dc5fdb email=email password=john"
pos = s.find("group_id=")
pos2 = s.find("admin_id=")
s = s[pos+9:pos2]
print()
print(s)
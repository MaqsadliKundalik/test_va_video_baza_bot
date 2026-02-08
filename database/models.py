from tortoise import Model, fields

class User(Model):
    id = fields.IntField(pk=True)
    tg_id = fields.IntField(unique=True)
    full_name = fields.CharField(max_length=100, null=True)    

class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

class Test(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    file_id = fields.CharField(max_length=512)
    test_key = fields.CharField(max_length=512)
    category_id = fields.IntField()

class TestAnswers(Model):
    id = fields.IntField(pk=True)
    test_id = fields.IntField()
    user_id = fields.IntField()
    answer = fields.CharField(max_length=512)
    score = fields.IntField()

    created_at = fields.DatetimeField(auto_now_add=True)

class VideoLessons(Model):
    id = fields.IntField(pk=True)
    file_id = fields.CharField(max_length=512)
    caption = fields.CharField(max_length=512)
    test_id = fields.IntField()

    created_at = fields.DatetimeField(auto_now_add=True)

class Subscriptions(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()

    created_at = fields.DatetimeField(auto_now_add=True)
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    fullname = models.CharField(max_length=200)
    age = models.IntegerField()
    is_admin = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Category(models.Model):
    id = models.AutoField(primary_key=id)
    name = models.CharField(max_length=200)
    def __str__(self):
            return self.name

class Book(models.Model):
    id = models.AutoField(primary_key=id)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField(upload_to='book_cover', null=True)
    file = models.FileField(upload_to='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Rating(models.Model):
    id = models.AutoField(primary_key=id)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return self.book.name

class Cart(models.Model):
    id = models.AutoField(primary_key=id)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + self.book.name

class Report(models.Model):
    id = models.AutoField(primary_key=id)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)

    def __str__(self):
        return self.reason

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.name

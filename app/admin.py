from django.contrib import admin
from app.models import User,Book,Category,Cart,Rating

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(Rating)



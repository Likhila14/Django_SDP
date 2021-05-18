from django.contrib import admin
from .models import Anniversary, Birthday, Book, Mothersday, Register, Review

admin.site.register(Register)
admin.site.register(Birthday)
admin.site.register(Anniversary)
admin.site.register(Book)
admin.site.register(Mothersday)
admin.site.register(Review)
# Register your models here.

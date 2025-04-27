from django.contrib import admin
from news.models import Post,Comment
class PostAdmin(admin.ModelAdmin):
    list_display=["id","title","content","publish_date"]
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id","comment"]
# Register your models here.
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
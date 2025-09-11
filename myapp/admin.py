from django.contrib import admin
from .models import CustomUser,Chat

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email","img"] # list_display で表示するフィールドを指定
    list_filter = ["username"] # list_filter で絞り込むフィールドを指定
    search_fields = ["username"] # search_fields で文字で検索するフィールドを指定
    ordering = ["id"] # ordering で並べるためのソート対象フィールドを指定
    list_per_page = 30 # list_per_page で1ページに表示する件数を指定
    list_editable = ["username","img"] # list_editable で一覧画面で一括編集ができるフィールドを指定
    readonly_fields = ["email"] # readonly_fields で管理者画面でも編集できないフィールドを指定
    exclude = ["password"] # exclude で逆に表示しない項目を指定
    fieldsets = [
        ("変更不可", {"fields": ["email"]}),
        ("変更可能", {"fields": ["username"]}),
    ] # fieldsets で詳細ページの分類ができる

admin.site.register(CustomUser,UserAdmin)
admin.site.register(Chat)


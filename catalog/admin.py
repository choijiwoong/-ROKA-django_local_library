from django.contrib import admin

# Register your models here.

#model 등록
from catalog.models import Author, Genre, Book, BookInstance, Language#call

#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(Genre)
#admin.site.register(BookInstance)
#admin.site.register(Language)

#<<edit>>

#Define the admin class
class AuthorAdmin(admin.ModelAdmin):#새 클래스 정의 
    list_display=('last_name', 'first_name', 'date_of_birth', 'date_of_death')

#Register thr admin class with the associated model
admin.site.register(Author, AuthorAdmin)#선언

#admin.site.register(Book)
#admin.site.register(BookInstance)

#Register the Admin classes for Book using the decorator
#@admin.register(Book)
#class BookAdmin(admin.ModelAdmin):#목록뷰
#    list_display=('title', 'author', 'display_genre')#장르는 다대다필드여서 리스트에 직접적으로 특정 불가. 그래서 함수 display_genre정의

#Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):#목록 필터
    list_display=('book', 'status', 'borrower', 'due_back', 'id')
    list_filter=('status', 'due_back')
    #<<edit>>세부뷰구역나누기
    fieldsets=(
        (None, {
            'fields':('book', 'imprint', 'id')
            }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
            }),
        )
    

class AuthorAdmin(admin.ModelAdmin):#세부보기
    list_display=('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields=['first_name', 'last_name', ('date_of_birth', 'date_of_death')]#튜플 수평뷰 가능...인데 왜 안돼지..

class BookInstanceInline(admin.TabularInline):
    model=BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'display_genre')
    inlines=[BookInstanceInline]

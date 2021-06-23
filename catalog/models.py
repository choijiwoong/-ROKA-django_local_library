from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

#<<edit>> 장르
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    #객체의 네임 변수 할당. science fiction
    def __str__(self):#문자열로 사용시 self.name반환
        """String for representing the Model object."""
        return self.name
    
#<<edit>> 책
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)#객체의 제목 변수 할당. 노인과 바다
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)#객체의 작가변수 할당. 일대다
    #일대일(OneToOneField), 일대다(ForeignKey), 다대다(ManyToManyField)
    # Foreign Key used because book can only have one author, but authors can have multiple books 책은 하나의 저자, 저자는 여러 책
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')#객체의 요약 텍스트필드 할당.
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    #객체에 문자필드 생성
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):#책을 문자열로 사용할 시 title반환
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])#세부적인 레코드에 접근하는 URL반환_book-datail에 해당하는 url매핑 정의와 관련 뷰, 탬플릿 정의 필요
    #<<edit>>
    def display_genre(self):
        """Create as string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
        display_genre.short_description='Genre'
#<<edit>> 복사본
import uuid

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    #객체의 고유 primary key 할당 uuid
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)#객체의 연관된 책을 찾는 변수 할당_일대다
    imprint = models.CharField(max_length=200)#객체의 발간일 변수 할당
    due_back = models.DateField(null=True, blank=True)#객체의 만기일 할당_반납
    borrower=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),#유지 관리
        ('o', 'On loan'),#대출
        ('a', 'Available'),#가능
        ('r', 'Reserved'),#반납
    )

    status = models.CharField(#선택목록을 정의하는 charfield 
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() >self.due_back:
            return True
        return False
    

    class Meta:
        ordering = ['due_back']
        permissions=(("can_mark_returned", "Set book as returned"),)

    def __str__(self):#문자열로 사용 시 고유id와 책 제목을 조합하여 반환
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
#<<edit>> 저자
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)#객체의 성 
    last_name = models.CharField(max_length=100)#객체의 이름
    date_of_birth = models.DateField(null=True, blank=True)#객체의 태어난 날
    date_of_death = models.DateField('died', null=True, blank=True)#객체의 뒤진날

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):#author-detail에 매핑된 아이디 상세정보 뭐 이런거겠지
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):#문자열 호출시 이름이랑 성 
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

#<<edit>> 언어
class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name



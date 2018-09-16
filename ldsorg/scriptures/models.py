from django.db import models

# Create your models here.

class Volume(models.Model):
    """Model for scripture volumes (e.g. Old Testament, New Testament)"""
    # Primary key is a volume index
    index = models.IntegerField(primary_key=True)
    # Scripture volume abbreviation (should match abbreviation used in lds.org URL e.g. 'ot' for Old Testament, 'bofm' for Book of Mormon)
    abbreviation = models.CharField(max_length=8)
    # Human-readable name for scripture volume (e.g. "Old Testament", "New Testament", "Book of Mormon")
    name = models.CharField(max_length=32)
    # Text of the lds.org title page for the volume
    title_page = models.TextField()
    # Text of the lds.org introduction page (if available) for the volume
    introduction = models.TextField(blank=True)
    # Date and time of last modification to the current record
    last_modified = models.DateTimeField('date last modified')
    
    # Define __str__ attribute for Volume
    def __str__(self):
        return self.name

class Book(models.Model):
    """Model for scripture books (e.g. Genesis for Old Testament, 1 Nephi for Book of Mormon)"""
    # Foreign key that references the scripture volume the book belongs to
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
    # Primary key is a book index
    index = models.IntegerField(primary_key=True)
    # Book abbreviation (should match abbreviation used in lds.org URL e.g. 'gen' for Genesis, '1-ne' for First Nephi)
    abbreviation = models.CharField(max_length=8)
    # Human-readable name for book (e.g. "Genesis", "St John", "First Nephi")
    name = models.CharField(max_length=32)
    # Text of the lds.org introduction page (if available) for the book
    introduction = models.TextField(blank=True)
    # Date and time of last modification to the current record
    last_modified = models.DateTimeField('date last modified')
    
    # Define __str__ attribute for Book
    def __str__(self):
        return self.name

class Chapter(models.Model):
    """Model for scripture chapters. These will be named by chapter number and therefore will be non-unique. The 'index' field will serve as the unique identifier."""
    # Foreign key that references the scripture book
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # Primary key that will serve as unique identifier
    index = models.IntegerField(primary_key=True)
    # Chapter number stored as integer (will need to be converted to string when constructing a URL)
    number = models.PositiveIntegerField(null=True)
    # Text of the lds.org introduction page (if available) for the book
    introduction = models.TextField(blank=True)
    # Text of the lds.org chapter summary (required field)
    summary = models.TextField()
    # Date and time of last modification to the current record
    last_modified = models.DateTimeField('date last modified')
    
    # Define __str__ attribute for Chapter
    def __str__(self):
        return str(self.number)

class Verse(models.Model):
    """Model for scripture verses. These will be named by verse number and therefore will be non-unique. The 'index' field will serve as the unique identifier."""
    # Foreign key that references the scripture book
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    # Primary key that will serve as unique identifier
    index = models.IntegerField(primary_key=True)
    # Verse number stored as integer (will need to be converted to string when constructing a URL)
    number = models.PositiveIntegerField(null=True)
    # Text of the verse (required field)
    text = models.TextField()
    # Date and time of last modification to the current record
    last_modified = models.DateTimeField('date last modified')
    
    # Define __str__ attribute for Verse
    def __str__(self):
        return str(self.number)


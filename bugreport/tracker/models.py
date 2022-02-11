from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances

PROJECT = (
    ('cmm', 'CheckMyMetal'),
    ('o', 'Other'),
)

class Bug(models.Model):
    """Model representing a bug."""
    ticket_number = models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular bug')
    created_at = models.DateField(auto_now_add=True)

    project = models.CharField(
        max_length=10,
        choices=PROJECT,
        blank=False,
        help_text='Project where bug is occuring',
    )

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the bug')

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    affiliation = models.CharField(max_length=200, null=True, blank=True, help_text='Institution')

    LOCATION = (
        ('us', 'United States'),
        ('c', 'Canada'),
        ('m', 'Mexico'),
        ('a', 'Africa'),
        ('as', 'Asia'),
        ('e', 'Europe'),
        ('o', 'Oceania'),
        ('sa', 'South America'),
    )

    location = models.CharField(
        max_length=2,
        choices=LOCATION,
        null=True,
        blank=True,
        default='us',
    )

    email = models.EmailField(max_length=254, null=True, blank=True)

    QUERY_TYPE = (
        ('b', 'bug'),
        ('q', 'question'),
        ('s', 'suggestion'),
        ('f', 'feedback'),
        ('l', 'like'),
        ('d', 'dislike'),
        ('o', 'other'),
    )

    query_type = models.CharField(
        max_length=1,
        choices=QUERY_TYPE,
        null=True,
        blank=True,
        default='b',
    )

    screenshot_or_attachment = models.FileField(upload_to ='uploads/', help_text = "Upload screenshot or a problematic data file", null=True, blank=True)

    status = models.CharField(max_length=20, default='Not fixed', help_text='Select a status for this bug')
    date_fixed = models.DateField('Fixed', null=True, blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('bug-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.description

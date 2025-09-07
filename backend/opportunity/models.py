from django.db import models
from user.models import User
from company.models import Company
from tag.models import Tag

# Create your models here.

class Opportunity(models.Model):
    OPPORTUNITY_TYPES = [
        ('internship', 'Internship'),
        ('hackathon', 'Hackathon'),
        ('scholarship', 'Scholarship'),
        ('event', 'Career Event'),
        ('job', 'Job Opening'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='opportunities', null=True, blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    is_remote = models.BooleanField(default=False)
    compensation = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    application_link = models.URLField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    
    # Metadata
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)
    visibility = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    
    # Relationships
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_opportunities')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_opportunities')
    tags = models.ManyToManyField(Tag, related_name='opportunities', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_opportunities', blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.opportunity_type}"

class Mentorship(models.Model):
    MENTORSHIP_TYPES = [
        ('career_guidance', 'Career Guidance'),
        ('technical_mentoring', 'Technical Mentoring'),
        ('interview_prep', 'Interview Preparation'),
        ('resume_review', 'Resume Review'),
        ('project_guidance', 'Project Guidance'),
        ('general', 'General Mentorship'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    mentorship_type = models.CharField(max_length=30, choices=MENTORSHIP_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Participants
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentoring_sessions')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorship_sessions')
    
    # Scheduling
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    meeting_link = models.URLField(null=True, blank=True)
    meeting_notes = models.TextField(null=True, blank=True)
    
    # Metadata
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.mentor.name} -> {self.mentee.name}: {self.title}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('opportunity', 'New Opportunity'),
        ('experience', 'New Experience'),
        ('mentorship', 'Mentorship Update'),
        ('verification', 'Verification Required'),
        ('system', 'System Notification'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    
    # Relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    related_opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True, blank=True)
    related_experience = models.ForeignKey('experience.Experience', on_delete=models.CASCADE, null=True, blank=True)
    related_mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE, null=True, blank=True)
    
    # Metadata
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.name}: {self.title}"

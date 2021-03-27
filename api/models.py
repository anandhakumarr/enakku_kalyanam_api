from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

User._meta.get_field('email')._unique = True

class HobbyCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Hobby(models.Model):
    title = models.CharField(max_length=255, unique=True)
    hobby_category = models.ForeignKey(HobbyCategory, on_delete=models.PROTECT)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserHobby(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    hobby = models.ForeignKey(Hobby, on_delete=models.PROTECT)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + '|' + self.hobby.title

class UserFamily(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    user_type = models.CharField(choices=[('Mother', 'Mother'), ('Father', 'Father'), ('Sister', 'Sister'), ('Brother', 'Brother')], default='Mother', max_length=20)
    name = models.CharField(max_length=40,null=True, blank=True)
    is_employed = models.BooleanField(max_length=40,null=True, blank=True)
    occupation = models.CharField(max_length=40,null=True, blank=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + '|' + self.user_type

class Membership(models.Model):
    membership = models.CharField(choices=[('Silver', 'Silver'), ('Gold', 'Gold'), ('Diamond', 'Diamond'), ('Free', 'Free')], default='Free', max_length=20)
    offer_percent =models.IntegerField(default=25)
    membership_price = models.IntegerField(default=1000)
    features = models.TextField(null=True, blank=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.membership

def user_directory_path(instance, filename):
    return 'uploads/user_{0}/photos/{1}'.format(instance.user.id, filename)

def user_horoscope_path(instance, filename):
    return 'uploads/user_{0}/horoscope/{1}'.format(instance.user.id, filename)

class UserPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    photo = models.FileField(upload_to=user_directory_path)
    verified = models.BooleanField(default=False)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    message = models.TextField(null=True, blank=True)
    notification_type = models.CharField(max_length=40,null=True, blank=True)
    status = models.CharField(max_length=40,null=True, blank=True)
    link = models.CharField(max_length=40,null=True, blank=True)    
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name 

class Raasi(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class EducationCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class OccupationCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class Star(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class MotherTongue(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class Religion(models.Model):
    title = models.CharField(max_length=255, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class Caste(models.Model):
    title = models.CharField(max_length=255, unique=True)
    religion = models.ForeignKey(Religion, on_delete=models.PROTECT)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class SubCaste(models.Model):
    title = models.CharField(max_length=255, unique=True)
    religion = models.ForeignKey(Religion, on_delete=models.PROTECT)
    caste = models.ForeignKey(Caste, on_delete=models.PROTECT)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class PartnerPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    age_from = models.IntegerField()
    age_to = models.IntegerField()
    height_from = models.DecimalField(max_digits=2,decimal_places=2)
    height_to = models.DecimalField(max_digits=2,decimal_places=2)
    physical_choices = [('Normal', 'Normal'), ('Physically Challenged', 'Physically Challenged')]
    physical_status = models.CharField(choices=physical_choices, default='Normal', max_length=25)
    bodytype_choices = [('Average', 'Average'), ('Athletic', 'Athletic'), ('Slim', 'Slim'), ('Heavy', 'Heavy')]
    body_type = models.CharField(choices=bodytype_choices, default='Average', max_length=10)
    eating_choices = [('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Eggetarian', 'Eggetarian')]
    eating_habits = models.CharField(choices=eating_choices, default='Vegetarian', max_length=20)
    drinking_smoking_choices = [('No', 'No'), ('Yes', 'Yes'), ('Occasionally', 'Occasionally')]
    drinking_habits = models.CharField(choices=drinking_smoking_choices, default='No', max_length=20)
    smoking_habits = models.CharField(choices=drinking_smoking_choices, default='No', max_length=20)
    mother_tongue = models.ForeignKey(MotherTongue, on_delete=models.PROTECT)
    religion = models.ForeignKey(Religion, on_delete=models.PROTECT)
    caste = models.ForeignKey(Caste, on_delete=models.PROTECT)
    raasi = models.ForeignKey(Raasi, on_delete=models.PROTECT)
    sub_caste = models.ForeignKey(SubCaste, on_delete=models.PROTECT)
    star = models.ForeignKey(Star, on_delete=models.PROTECT)
    highest_education = models.ForeignKey(EducationCategory, on_delete=models.PROTECT)
    employment_choices = [
        ('Private', 'Private'), 
        ('Business', 'Business'), 
        ('Not Working', 'Not Working'), 
        ('Government/PSU', 'Government/PSU'), 
        ('Defence', 'Defence'), 
        ('Self Employed', 'Self Employed')
    ]
    employed_in = models.CharField(choices=employment_choices, default='Private', max_length=50)
    occupation = models.ForeignKey(OccupationCategory, on_delete=models.PROTECT)
    income_from = models.IntegerField()
    income_to = models.IntegerField()
    dosham = models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ("Doesn't Mater", "Doesn't Mater")], default='No', max_length=20)
    about_partner = models.TextField()
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)



class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    device_id = models.CharField(null=True, blank=True, max_length=50, unique=True)
    device_token = models.CharField(null=True, blank=True, max_length=200)    
    device_type = models.CharField(null=True, blank=True, default="mobile", max_length=50)
    device_os = models.CharField(null=True, blank=True, max_length=50)
    device_version = models.CharField(null=True, blank=True, max_length=50)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + ' | ' +self.device_id


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_editor = models.BooleanField(default=False)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE,null=True, blank=True)
    profile_image = models.CharField(max_length=500,null=True, blank=True)    
    gender = models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=20)
    about_me = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    about_family = models.TextField(null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=True)
    mother_tongue = models.ForeignKey(MotherTongue, on_delete=models.PROTECT,null=True, blank=True)
    bodytype_choices = [('Average', 'Average'), ('Athletic', 'Athletic'), ('Slim', 'Slim'), ('Heavy', 'Heavy')]
    body_type = models.CharField(choices=bodytype_choices, default='Average', max_length=20)
    physical_choices = [('Normal', 'Normal'), ('Physically Challenged', 'Physically Challenged')]
    physical_status = models.CharField(choices=physical_choices, default='Normal', max_length=25)
    eating_choices = [('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Eggetarian', 'Eggetarian')]
    eating_habits = models.CharField(choices=eating_choices, default='Vegetarian', max_length=20)
    drinking_smoking_choices = [('No', 'No'), ('Yes', 'Yes'), ('Occasionally', 'Occasionally')]
    drinking_habits = models.CharField(choices=drinking_smoking_choices, default='No', max_length=20)
    smoking_habits = models.CharField(choices=drinking_smoking_choices, default='No', max_length=20)
    profile_created_by_choices = [('Self', 'Self'), ('Parent', 'Parent'), ('Sibling', 'Sibling'), ('Friend', 'Friend'), ('Relative', 'Relative')]
    profile_created_by = models.CharField(choices=profile_created_by_choices, default='Self', max_length=20)
    height = models.DecimalField(max_digits=2,decimal_places=2,null=True, blank=True)
    weight = models.DecimalField(max_digits=2,decimal_places=2,null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    work_location = models.CharField(max_length=50,null=True, blank=True)
    native_location = models.CharField(max_length=50,null=True, blank=True)
    primary_phone = models.CharField(max_length=20,null=True, blank=True, unique=True)
    secondary_phone = models.CharField(max_length=20,null=True, blank=True)
    gothram = models.CharField(max_length=20,null=True, blank=True)
    dosham = models.CharField(max_length=20,null=True, blank=True)
    zodiac = models.CharField(max_length=20,null=True, blank=True)
    religion = models.ForeignKey(Religion, on_delete=models.PROTECT,null=True, blank=True)
    caste = models.ForeignKey(Caste, on_delete=models.PROTECT,null=True, blank=True)
    sub_caste = models.ForeignKey(SubCaste, on_delete=models.PROTECT,null=True, blank=True)
    star = models.ForeignKey(Star, on_delete=models.PROTECT,null=True, blank=True)
    horoscope = models.FileField(upload_to=user_horoscope_path,null=True, blank=True)
    highest_education = models.ForeignKey(EducationCategory, on_delete=models.PROTECT,null=True, blank=True)
    college = models.CharField(max_length=50,null=True, blank=True)
    employment_choices = [
        ('Private', 'Private'), 
        ('Business', 'Business'), 
        ('Not Working', 'Not Working'), 
        ('Government/PSU', 'Government/PSU'), 
        ('Defence', 'Defence'), 
        ('Self Employed', 'Self Employed')
    ]
    employed_in = models.CharField(choices=employment_choices, default='Private', max_length=50)
    occupation = models.ForeignKey(OccupationCategory, on_delete=models.PROTECT,null=True, blank=True)
    salary_per_month = models.DecimalField(max_digits=15, decimal_places=2,null=True, blank=True)
    salary_currency_type = models.CharField(max_length=10,null=True, blank=True)

    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    user_verified = models.BooleanField(default=False)
    completed_basic_details = models.BooleanField(default=False)
    completed_relegious_details = models.BooleanField(default=False)    
    completed_professional_details = models.BooleanField(default=False)
    completed_family_details = models.BooleanField(default=False)
    completed_profile_details = models.BooleanField(default=False)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name 

class RequestLogger(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    method = models.CharField(max_length=10)
    request_path = models.CharField(max_length=255)
    body = models.TextField()
    created_ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name


@receiver(pre_save, sender=Membership)
@receiver(pre_save, sender=HobbyCategory)
@receiver(pre_save, sender=Hobby)
@receiver(pre_save, sender=Raasi)
@receiver(pre_save, sender=EducationCategory)
@receiver(pre_save, sender=OccupationCategory)
@receiver(pre_save, sender=Star)
@receiver(pre_save, sender=MotherTongue)
@receiver(pre_save, sender=Religion)
@receiver(pre_save, sender=Caste)
@receiver(pre_save, sender=SubCaste)
def create_membership(sender, instance, *args, **kwargs):
    if kwargs['raw']:
        instance.updated_ts = timezone.now()
        instance.created_ts = timezone.now()


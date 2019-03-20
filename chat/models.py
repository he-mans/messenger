from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
	profile_picture = models.ImageField(
							upload_to='userPofilePic', 
							default='default.jpg'
						)
	status = models.CharField(max_length=100, default="no description")
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user.username}'

	def save(self):
		super().save()	
		
		output_size=(300,300)
		image = Image.open(self.profile_picture.path)
		image = image.resize(output_size)
		image.save(self.profile_picture.path)

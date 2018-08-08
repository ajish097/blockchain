from django.db import models

# Create your models here.
class User_account(models.Model):
	user_name = models.CharField(max_length=100, primary_key=True)
	account_balance = models.IntegerField(default=1000)


class Block_chain(models.Model):
	time_stamp =  models.CharField(max_length=200)
	previous_hash =  models.CharField(max_length=200)
	current_hash = models.CharField(max_length=200)
	amount = models.IntegerField(default=0)
	sender = models.CharField(max_length=200)
	receiver = models.CharField(max_length=200)
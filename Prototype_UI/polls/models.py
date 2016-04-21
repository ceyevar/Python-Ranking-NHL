from django.db import models


class Player(models.Model):
	name = models.CharField(max_length = 200)
	goals = models.IntegerField()
	assists = models.IntegerField()
	es_primary_pt_gp = models.DecimalField(max_digits=20,decimal_places=4)
	pim = models.IntegerField()
	es_gf_rel = models.DecimalField(max_digits=20,decimal_places=4)
	es_ga = models.IntegerField()


class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text

# Create your models here.

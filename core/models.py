from django.db import models
from django.contrib.auth.models import User


class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    nutri_score_weight = models.IntegerField(default=2)
    vegan_weight = models.IntegerField(default=1)
    vegetarian_weight = models.IntegerField(default=1)
    palm_oil_free_weight = models.IntegerField(default=1)
    eco_score_weight = models.IntegerField(default=2)
    nova_group_weight = models.IntegerField(default=1)
    # allergens_weight = models.FloatField(default=0.1)
    gluten_weight = models.IntegerField(default=1)
    milk_weight = models.IntegerField(default=1)
    nuts_weight = models.IntegerField(default=1)
    peanuts_weight = models.IntegerField(default=1)
    soybeans_weight = models.IntegerField(default=1)
    # nuts_peanuts_soybeans_weight = models.FloatField(default=0.1)
    additives_weight = models.IntegerField(default=1)

    def __str__(self):
        return f"Preferences for {self.user.username}"

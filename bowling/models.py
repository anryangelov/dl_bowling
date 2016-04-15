from django.db import models
from .constans import ALL_PINS


class Player(models.Model):

    name = models.CharField(max_length=200)
    score = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Frame(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    roll1 = models.IntegerField(null=True)
    roll2 = models.IntegerField(null=True)
    roll3 = models.IntegerField(null=True)  # because of the last frame
    strike = models.BooleanField(default=False)
    spare = models.BooleanField(default=False)
    score = models.IntegerField(null=True)

    def __str__(self):
        return "%s, %s, %s, strike:%s, spare:%s, score:%s" % (
            self.roll1, self.roll2, self.roll3,
            self.strike, self.spare, self.score
        )

    def get_dict(self):
        return {'roll1': self.roll1, 'roll2': self.roll2,
                'strike': self.strike, 'spare': self.spare,
                'score': self.score}

import uuid

from django.db import models


class Channel(models.Model):
    id = models.CharField(primary_key=True, max_length=50)


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    real_name = models.CharField(max_length=50)


class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    directs = models.CharField(max_length=50)
    s_manager = models.CharField(max_length=50)
    consolidated_primary_team = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    consolidated_teams = models.CharField(max_length=50, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)

    @property
    def is_consolidated_primary_team(self):
        return self.consolidated_primary_team and self.id == self.consolidated_primary_team.id

    @property
    def is_standalone_team(self):
        return not self.consolidated_primary_team and self.channel

    @property
    def is_secondary_team(self):
        return self.consolidated_primary_team and self.id != self.consolidated_primary_team.id









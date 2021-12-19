from rest_framework import serializers

from OrgChartApp import models


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class ChannelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = "__all__"

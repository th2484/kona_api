from http.client import HTTPResponse

from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from . import models
from .serializers import TeamSerializer, UsersSerializer, ChannelsSerializer


class ChannelsView(ListAPIView):
    queryset = models.Channel.objects.all()
    serializer_class = ChannelsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UsersView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = UsersSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ConsolidatedPrimaryView(ListAPIView):
    serializer_class = TeamSerializer
    queryset = models.Team.objects.all()

    def get(self, request, *args, **kwargs):
        data = []
        for team in self.queryset.all():
            if team.is_consolidated_primary_team:
                directs = []
                directs_list = team.directs.split(",")

                for direct_id in directs_list:
                    direct = models.User.objects.get(id=direct_id)
                    directs.append(dict(id=direct.id, name=direct.real_name))

                consolidated_teams_list = team.consolidated_teams.split(",")
                consolidated_teams = []
                for consolidated_team_id in consolidated_teams_list:
                    consolidated_team = models.Team.objects.get(id=consolidated_team_id)
                    consolidated_directs = []
                    consolidated_directs_list = consolidated_team.directs.split(",")

                    for consolidated_directs_id in consolidated_directs_list:
                        consolidated_direct = models.User.objects.get(id=consolidated_directs_id)
                        consolidated_directs.append(dict(id=consolidated_direct.id, name=consolidated_direct.real_name))
                    consolidated_teams.append(dict(id=consolidated_team.id, name=consolidated_team.name, directs=consolidated_directs))

                team_dict = dict(
                    id=team.id,
                    name=team.name,
                    manager={'id': team.manager.id, 'name': team.manager.real_name},
                    directs=directs,
                    consolidated_teams=consolidated_teams,
                    channel=team.channel.id
                )

                data.append(team_dict)
        return Response(status=200, data=data)


class ConsolidatedSecondaryView(ListAPIView):
    serializer_class = TeamSerializer
    queryset = models.Team.objects.all()

    def get(self, request, *args, **kwargs):
        data = []
        for team in self.queryset.all():
            if team.is_secondary_team:
                directs = []
                directs_list = team.directs.split(",")
                for direct_id in directs_list:
                    direct = models.User.objects.get(id=direct_id)
                    directs.append(dict(id=direct.id, name=direct.real_name))
                team_dict = dict(
                    id=team.id,
                    name=team.name,
                    manager={'id': team.manager.id, 'name': team.manager.real_name},
                    directs=directs,
                    channel=team.channel.id if team.channel else None
                )

                data.append(team_dict)
        return Response(status=200, data=data)


class StandAloneView(ListAPIView):
    serializer = TeamSerializer
    queryset = models.Team.objects.all()

    def get(self, request, *args, **kwargs):
        data = []
        for team in self.queryset.all():
            if team.is_standalone_team:
                directs = []
                directs_list = team.directs.split(",")
                for direct_id in directs_list:
                    direct = models.User.objects.get(id=direct_id)
                    directs.append(dict(id=direct.id, name=direct.real_name))
                team_dict = dict(
                    id=team.id,
                    name=team.name,
                    manager={'id': team.manager.id, 'name': team.manager.real_name},
                    directs=directs,
                    channel=team.channel.id if team.channel else None
                )

                data.append(team_dict)
        return Response(status=200, data=data)


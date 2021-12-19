import json
import django
from django.apps import AppConfig

from django.db import transaction



JSON = json.loads(open('./test_data.json').read())


class OrgChartAppConfig(AppConfig):
    name = 'OrgChartApp'
    json = JSON

    def ready(self):
        from OrgChartApp import models

        for user_id in self.json:

            user_dict = self.json[user_id]
            try:
                user, created = models.User.objects.get_or_create(
                    id=user_id,
                    real_name=user_dict['realName']
                )
            except django.db.utils.OperationalError:
                return

            if 'teams' in user_dict:
                for team_number in user_dict['teams']:

                    team_dict = user_dict['teams'][team_number]
                    directs = ",".join(team_dict["directs"])
                    s_manager = ",".join(team_dict["s_manager"])
                    manager = models.User.objects.get(id=user_id)
                    team_id = f"{user_id}&{team_number}"

                    team, created = models.Team.objects.get_or_create(
                        id=team_id,
                        name=team_dict['name'],
                        manager=manager,
                        directs=directs,
                        s_manager=s_manager,
                    )

                    if 'consolidatedPrimaryTeam' in team_dict['settings']:
                        cp_team_id = team_dict['settings']['consolidatedPrimaryTeam']
                        cp_team_number = cp_team_id.split("&")[1]
                        cp_team_user = cp_team_id.split("&")[0]

                        cp_team_dict = self.json[cp_team_user]['teams'][cp_team_number]
                        cp_directs = ",".join(cp_team_dict["directs"])
                        cp_s_manager = ",".join(cp_team_dict["s_manager"])
                        cp_manager = models.User.objects.get(id=cp_team_user)
                        consolidated_primary_team, created = models.Team.objects.get_or_create(
                            id=cp_team_id,
                            name=cp_team_dict['name'],
                            manager=cp_manager,
                            directs=cp_directs,
                            s_manager=cp_s_manager,
                        )
                        team.consolidated_primary_team = consolidated_primary_team

                    if 'consolidatedTeams' in team_dict['settings']:
                        consolidated_teams = ",".join(team_dict['settings']['consolidatedTeams'])
                        team.consolidated_teams = consolidated_teams

                    if 'channel_id' in team_dict['settings']:
                        channel, created = models.Channel.objects.get_or_create(id=team_dict['settings']['channel_id'])
                        team.channel = channel

                    team.save()

        print(f"Users: {models.User.objects.all()}, {len(models.User.objects.all())}")
        print(f"Teams: {models.Team.objects.all()}, {len(models.Team.objects.all())}")
        print(f"Channels: {models.Channel.objects.all()}, {len(models.Channel.objects.all())}")


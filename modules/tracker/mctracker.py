import datetime

from modules.config import Config
from modules.database import DB

import matplotlib.pyplot as plt

from .mcserver import MCServer

class MCTracker(DB):
    def __init__(self):
        self.all_servers = Config.SERVERS
        self.data = []
        self.is_fetched = False

    @staticmethod
    @DB.fetch
    def get_servers():
        return 'SELECT * FROM `servers`'

    def fetch_all(self):  
        self.data.clear()

        for server in self.all_servers:
            self.data.append(MCServer(server['name'], server['address']))
        
        self.is_fetched = True

        return self.data

    def sort_all(self):
        if not self.is_fetched:
            return print('You should exec MCTracker#fetch_all first!')
        
        self.data.sort(key=lambda x: x.get_online_players(), reverse=True)

        return self.data


    def fetch_and_sort(self):
        self.fetch_all()
        return self.sort_all()

    def separated_names_and_players(self):
        names = []
        players = []

        for server in self.data:
            name = server.get_name()
            names.append((name[:8] + '..') if len(name) > 8 else name)
            players.append(server.get_online_players())
            
        return {'names': names, 'players': players}

    def draw_chart(self, output_file='chart.png'):
        separated = self.separated_names_and_players()

        names = separated['names']
        players = separated['players']
        colors = ['lime','lime','green','green','darkgreen','darkgreen', 'gold', 'yellow','yellow', 'khaki', 'orangered', 'indianred', 'indianred', 'firebrick', 'firebrick']

        fig = plt.figure(figsize=(17,8))
        plt.bar(names, players, color=colors)
        plt.title(f"Iranian MineCraft Servers - {datetime.datetime.now():%Y-%m-%d %I:%M:%S}")
        plt.xlabel('Server Names', fontsize=8, labelpad=5)
        plt.ylabel('Players Count', fontsize=8, labelpad=5)
        plt.savefig(output_file)

        return output_file
    
    def zero_player_count(self):
        count = 0
        for server in self.data:
            if server.get_online_players() == 0:
                count += 1
        return count

    def all_player_count(self):
        total = 0
        for server in self.data:
            total += server.get_online_players()
        return total
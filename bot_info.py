# Stores information about servers the bot is in
import pickle
import discord


class Guild:
    def __init__(self, guild: discord.Guild):
        self.id = guild.id
        self.name = guild.name
        self.member_count = None
        self.show_members = None
        self.member_update_time = {}


class Bot_info:
    def __init__(self):
        self.guilds = {}

    def add_guild(self, guild: discord.Guild):
        self.guilds[guild.id] = Guild(guild)

    @staticmethod
    def load():
        try:
            with open("bot_info.pickle", "rb") as f:
                file = pickle.load(f)
        except FileNotFoundError:
            return Bot_info()

        return file

    def save(self):
        with open("bot_info.pickle", "wb") as f:
            pickle.dump(self, f)

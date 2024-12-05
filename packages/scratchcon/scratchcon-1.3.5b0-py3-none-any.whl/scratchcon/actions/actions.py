from .common import public
from scratchcon.exceptions import *

project = None
studio = None
user = None


def load():
    global project, studio, user
    project = public.login.connect_project(public.project_id)
    studio = public.login.connect_studio(public.studio_id)
    user = public.login.connect_user(public.username)


class Project:
    @staticmethod
    def post_comment(message):
        project.post_comment(message)

    @staticmethod
    def love():
        project.love()

    @staticmethod
    def unlove():
        project.unlove()

    @staticmethod
    def favorite():
        project.favorite()

    @staticmethod
    def unfavorite():
        project.unfavorite()

    @staticmethod
    def download(filename: str, dire="."):
        project.download(filename, dire)


class Studio:
    @staticmethod
    def post_comment(message: str):
        studio.post_comment(message)

    @staticmethod
    def follow():
        studio.follow()

    @staticmethod
    def unfollow():
        studio.unfollow()

    @staticmethod
    def add_project(proj_id: int):
        studio.add_project(proj_id)

    @staticmethod
    def remove_project(proj_id: int):
        studio.remove_project(proj_id)

    @staticmethod
    def invite(username: str):
        studio.invite_curator(username)

    @staticmethod
    def promote(username: str):
        studio.promote_curator(username)

    @staticmethod
    def remove(username: str):
        studio.remove_curator(username)


class User:
    @staticmethod
    def comment(message: str):
        user.post_comment(message)

    @staticmethod
    def follow():
        user.follow()

    @staticmethod
    def unfollow():
        user.unfollow()

    @staticmethod
    def exists() -> str:
        return user.does_exist()

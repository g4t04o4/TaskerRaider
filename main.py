from scripts.dbconfig import Settings

from scripts.taskerraider import TaskerRaider

settings = Settings()

tr = TaskerRaider(settings.database_url)
app = tr.app
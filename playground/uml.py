from pprint import pprint
from taiga import TaigaAPI

api = TaigaAPI()

api.auth(
    username='mouimet@infinisoft.world',
    password='S3l3c3A3!!!!'
)
pprint(api.token)

project = api.projects.get_by_slug("assistanceti-erp-phase-1")
storie = project.get_userstory_by_ref(527)
task = project.get_task_by_ref(529)
# pprint(vars(task))
# pprint(project.stats())
project.s
# pprint(vars(storie))
# for d in storie.list_tasks():
#     pprint(vars(d))

# pprint()
# pprint(vars(api.me()))
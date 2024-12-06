import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), verbose=True)

# pinpoint
##################################################################
from starlette_context.middleware import ContextMiddleware
from pinpointPy import set_agent, use_thread_local_context
from pinpointPy.Fastapi import async_monkey_patch_for_pinpoint, CommonPlugin
from starlette.middleware import Middleware
from pinpointPy.Fastapi import PinPointMiddleWare

use_thread_local_context()
async_monkey_patch_for_pinpoint()

app_id = os.getenv('pinpoint_id')
app_name = os.getenv('pinpoint_appname')
collector_agent_ip = os.getenv('collector_agent_ip')
collector_agent_port = os.getenv('collector_agent_port')
collect_agent_host = 'tcp:{}:{}'.format(collector_agent_ip, collector_agent_port)
print(app_id, app_name, collect_agent_host)

middleware = [
    Middleware(ContextMiddleware),
    Middleware(PinPointMiddleWare)
]

set_agent(app_id, app_name, collect_agent_host, -1, True)
##################################################################

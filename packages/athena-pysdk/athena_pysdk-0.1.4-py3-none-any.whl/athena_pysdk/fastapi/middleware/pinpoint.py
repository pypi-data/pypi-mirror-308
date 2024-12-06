import os
from pinpointPy import set_agent, use_thread_local_context
from pinpointPy.Fastapi import async_monkey_patch_for_pinpoint


def pinpoint_init():
    use_thread_local_context()
    async_monkey_patch_for_pinpoint()

    app_id = os.getenv('pinpoint_id')
    app_name = os.getenv('pinpoint_appname')
    collector_agent_ip = os.getenv('collector_agent_ip')
    collector_agent_port = os.getenv('collector_agent_port')
    collect_agent_host = 'tcp:{}:{}'.format(collector_agent_ip, collector_agent_port)
    print(app_id, app_name, collect_agent_host)

    set_agent(app_id, app_name, collect_agent_host, -1, True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import requests

CHAT_ID = "242125085"


def create_message(alert_json):
    # Get alert information
    title = alert_json['rule']['description'] if 'description' in alert_json['rule'] else ''
    description = alert_json['full_log'] if 'full_log' in alert_json else ''
    description.replace("\\n", "\n")
    alert_level = alert_json['rule']['level'] if 'level' in alert_json['rule'] else ''
    groups = ', '.join(alert_json['rule']['groups']) if 'groups' in alert_json['rule'] else ''
    rule_id = alert_json['rule']['id'] if 'rule' in alert_json else ''
    agent_name = alert_json['agent']['name'] if 'name' in alert_json['agent'] else ''
    agent_id = alert_json['agent']['id'] if 'id' in alert_json['agent'] else ''

    # Format message with markdown
    msg_text = f'*{title}*\n\n'
    msg_text += f'_{description}_\n'
    msg_text += f'*Groups:* {groups}\n' if len(groups) > 0 else ''
    msg_text += f'*Rule:* {rule_id} (Level {alert_level})\n'
    msg_text += f'*Agent:* {agent_name} ({agent_id})\n' if len(agent_name) > 0 else ''

    msg_data = {}
    msg_data['chat_id'] = CHAT_ID
    msg_data['text'] = msg_text
    msg_data['parse_mode'] = 'markdown'
    return json.dumps(msg_data)


# Read configuration parameters
alert_file = open(sys.argv[1])
hook_url = sys.argv[3]

# Read the alert file
alert_json = json.loads(alert_file.read())
alert_file.close()

# Send the request
msg_data = create_message(alert_json)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
response = requests.post(hook_url, headers=headers, data=msg_data)

sys.exit(0)

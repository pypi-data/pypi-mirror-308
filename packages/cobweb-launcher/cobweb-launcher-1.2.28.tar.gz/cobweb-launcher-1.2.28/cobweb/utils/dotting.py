import json

from aliyun.log import LogClient, PutLogsRequest, LogItem

import setting


class LoghubDot:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = LogClient(**setting.LOGHUB_CONFIG)

    def build(self, topic, data):
        log_item = LogItem()
        for key, value in data.items():
            if not isinstance(value, str):
                data[key] = json.dumps(value, ensure_ascii=False)
        contents = sorted(data.items())
        log_item.set_contents(contents)
        request = PutLogsRequest(
            project=setting.LOGHUB_PROJECT,
            logstore="cobweb_log",
            topic=topic,
            logitems=contents,
            compress=True
        )
        self.client.put_logs(request=request)

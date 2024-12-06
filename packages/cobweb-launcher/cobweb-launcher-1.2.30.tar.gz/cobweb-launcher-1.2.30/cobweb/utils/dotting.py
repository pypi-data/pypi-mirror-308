import json

from aliyun.log import LogClient, PutLogsRequest, LogItem

from cobweb import setting


class LoghubDot:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = LogClient(**setting.LOGHUB_CONFIG)

    def build(self, topic, **kwargs):
        temp = {}
        log_item = LogItem()
        for key, value in kwargs.items():
            if not isinstance(value, str):
                temp[key] = json.dumps(value, ensure_ascii=False)
        contents = sorted(temp.items())
        log_item.set_contents(contents)
        request = PutLogsRequest(
            project="databee-download-log",
            logstore="cobweb_log",
            topic=topic,
            logitems=contents,
            compress=True
        )
        self.client.put_logs(request=request)

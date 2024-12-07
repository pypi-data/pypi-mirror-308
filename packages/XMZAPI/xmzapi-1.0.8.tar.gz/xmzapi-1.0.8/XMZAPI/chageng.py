import requests
from XMZAPI.APM import OpenTelemetryConfigurator, get_tracer
from XMZAPI.KVS import LogHandler
from XMZAPI.headers import CustomRequestHeaders


class Change:
    def __init__(self):
        self.url = "https://api.yujn.cn/api/chageng.php"
        self.log = LogHandler()
        self.configurator = OpenTelemetryConfigurator(
            host_name="Change",
            service_name="XMZSDK",
            service_version="1.0.0",
            deployment_environment="prod",
            endpoint="http://tracing-analysis-dc-sh.aliyuncs.com/adapt_i8ucd7m6kr@c81a1d4e5cb019a_i8ucd7m6kr@53df7ad2afe8301/api/otlp/traces",
        )
        self.configurator.init_opentelemetry()
        self.tracer = get_tracer()
        M = CustomRequestHeaders()
        self.headers = M.reset_headers()

    def get_change(self, msg):
        with self.tracer.start_as_current_span("get_change") as span:
            url = self.url
            params = {"type": "json", "msg": msg}
            headers = self.headers
            M = requests.get(url, params, headers=headers)
            span.set_attribute("msg", msg)
            span.set_attribute("response", M.text)
            self.log.process_log(M.text, "Change")
            return M.text

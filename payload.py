 import requests
 def post_anomaly_event(self, device_name, message, details, ts, end_ts, created_by):
        created_date = int(pd.to_datetime(ts, unit='ms').value / 1000 / 1000)
        end_date = int(pd.to_datetime(end_ts, unit='ms').value / 1000 / 1000)
        payload = {"thingId": self.db.get_thing_id(device_name), "status": "warning", "description": message,
                   "source": "ANALYTIC_KMEANS", "priority": "MEDIUM", "parameter": "Anomaly",
                   "createdDate": created_date, "endDate": end_date, "additionalDetails": details}
        headers = {"cache-control": "no-cache",
                   "content-type": "application/json",
                   "uid": created_by}
        event_url = self.data_url + '/dashboard/api/v1/thingEvent'
        request = requests.Request('POST', event_url, headers=headers, json=payload)
        p = request.prepare()
        result = requests.Session().send(p)
        code = result.status_code
        if code != 200:
            print("WARNING: POST {} status_code={} result={}".format(event_url, code, str(result.text)))
        else:
            print("POST {} succeeded".format(event_url))

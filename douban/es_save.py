from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch("39.96.77.2:9200")


def save(index, doc_type, data):
    data=dict(data)
    index = es.index(index=index, doc_type=doc_type, body=data)
    print(index)


if __name__ == "__main__":
    data = {
        "@timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800"),
        "http_code": "404",
        "count": "10"
    }
    save("nihao", "nihao", data)

import os
import json
import subprocess
import hashlib

USERNAME = "elastic"
PASSWORD = "z7isN2WaZzTiGPUY6oUgYoDk"
ELASTIC_URL = "https://be0044d4d6e64e0c9bb083c9a6d120ed.westeurope.azure.elastic-cloud.com:9243"

def code_search(regex, size=10):
    query = {
        "query": {
            "regexp": {
                "content": {
                    "value": regex
                }
            }
        },
        "size": size
    }
    results = hit("code/_search?pretty=true", header = "content-Type: application/json",
            method = "GET", data = json.dumps(query))
    results = json.loads(results)
    lines = [hit["_source"]["content"] for hit in results["hits"]["hits"]]
    for line in lines:
        print(line, end = '')


def status():
    print(hit("_cat/indices?v"))


def hit(endpoint, method="GET", header=None, data=None, bin_data_path=None):
    args = ["curl", "-u", USERNAME + ":" + PASSWORD, "-X", method]
    if header is not None:
        args.append("-H")
        args.append(header)
    args.append(os.path.join(ELASTIC_URL, endpoint))
    if data is not None:
        args.append("-d")
        args.append(data)
    if bin_data_path is not None:
        args.append("--data-binary")
        args.append("@" + bin_data_path)

    proc = subprocess.run(args, stdout=subprocess.PIPE)
    return proc.stdout.decode("utf-8")

def jsonize_repo(root, repo_url, outfile, filetypes=["py"]):
    with open(outfile, "w+") as out:
        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if filename.split(".")[-1] in filetypes:
                    file_path = os.path.join(dirpath, filename)
                    print("Adding {}".format(file_path))
                    out.write(jsonize_file(file_path, repo_url))


def jsonize_file(file_path, repo_url):
    json_string = ""
    with open(file_path, "r") as f:
        for i, line in enumerate(f.readlines()):
            file_url = repo_url + "/blob/master" + file_path[file_path[2:].find("/")+2:]
            index, obj = jsonize_line(line, repo_url, file_url, i + 1)
            json_string += index + '\n'
            json_string += obj + '\n'
    return json_string

def jsonize_line(line, repo_url, file_url, line_num):
    m = hashlib.new("md5")
    m.update(repo_url.encode("utf-8"))
    m.update(file_url.encode("utf-8"))
    m.update(line.encode("utf-8"))
    _id = m.hexdigest()

    index = {
        "index": {"_id": _id}
    }
    obj = {
        "repo_url": repo_url,
        "file_url": file_url,
        "line_num": line_num,
        "content": line
    }
    return json.dumps(index), json.dumps(obj)


if __name__ == "__main__":
    # jsonize_repo("./django", "https://github.com/django/django", "ahhh.json")
    # hit("code/_bulk", header = "Content-Type: application/json", method = "POST",
    #        bin_data_path = "ahhh.json")

    mapping = {
        "settings":{
            "index":{
                "analysis":{
                    "analyzer":{
                        "analyzer_keyword":{
                            "tokenizer":"keyword"
                        }
                    }
                }
            }
        },
        "mappings":{
            "code":{
                "properties":{
                    "title":{
                        "analyzer":"analyzer_keyword",
                        "type":"string"
                    }
                }
            }
        }
    }
    result = hit("codeindex?pretty=true", header = "Content-Type: application/json", method = "PUT", data = json.dumps(mapping))
    print(result)

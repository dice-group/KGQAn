from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import io
from kgqan import KGQAn


hostName = "0.0.0.0"
serverPort = 5050

max_Vs = 1
max_Es = 10
max_answers = 41
limit_VQuery = 100
limit_EQuery = 100

class MyServer(BaseHTTPRequestHandler):

    def parse_answer(self, answers, entities):
        nodes = list(entities)
        nodes.remove('uri')
        objs = []
        for answer in answers:
            values = []
            if answer['results'] and answer['results']['bindings']:
                for value in answer['results']['bindings']:
                    values.append(value['uri']['value'])
            if len(values) > 0:
                obj = {'question': answer['question'], 'sparql': answer['sparql'], 'values': values, 'nodes': nodes}
                objs.append(obj)

        return json.dumps(objs)

    def do_POST(self):
        print("In post ")
        print(self.request)
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        print(post_data)
        fix_bytes_value = post_data.replace(b"'", b'"')
        data = json.load(io.BytesIO(fix_bytes_value))
        print(data)

        MyKGQAn = KGQAn(n_max_answers=max_answers, n_max_Vs=max_Vs, n_max_Es=max_Es,
                        n_limit_VQuery=limit_VQuery, n_limit_EQuery=limit_EQuery)
        answers, entities = MyKGQAn.ask(question_text=data['question'])
        result = self.parse_answer(answers, entities)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin" , "*")
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
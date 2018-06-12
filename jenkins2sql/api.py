import ConfigParser

from flask import Flask
from flask import request
import json
import requests
from subunit2sql import read_subunit
from subunit2sql import shell

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


def get_parameters(url):
    data = json.loads(requests.get(url))
    

def get_subunit_file(url):
    pass

@app.route('/runs', methods=['GET', 'POST'])
def create_run():
    try:
        url = request.args.get('build_url')
    except KeyError:
        return 'Wrong url parameters! \nExpecting build url from jenkins.'
    parameters = get_parameters('%s/api/json' % url)
    subunit_file = get_subunit_file('%s' % url)
    stream = read_subunit.ReadSubunit(subunit_file)
    shell.process_results(stream.get_results())
    shell.CONF.set_override('run_meta', metadata)
    shell.process_results(stream.get_results())

    
def main():
    config = ConfigParser.ConfigParer()
    config.read(['etc/jenkins2sql.conf'])
    host = 'http://%s' % config.get('default', 'host', '127.0.0.1')
    port = config.getint('default', 'port', '7000')
    db_uri = config.get('default', 'db_uri')
    shell.cli_opts()
    shell.parse_args([])
    shell.CONF.set_override('connection', db_uri, group='database')
    app.run(debug=True, host=host, port=port)
 

if __name__ == "__main__":
   main()

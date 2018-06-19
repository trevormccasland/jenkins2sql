import ConfigParser

from flask import Flask
from flask import request
import io
import json
import requests
from subunit2sql import read_subunit
from subunit2sql import shell

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


def get_app():
    return app


def get_metadata(json_data):
    data = json.loads(json_data.text)
    # make configurable
    url = data['url']
    url_parts = url.split('/')
    return {'build_name':  url_parts[-3:-2],
            'artifacts': url,
            'host': url_parts[-5:-4],
            'build_id':  url_parts[-3:-1]}

def requests_get(url, auth=None):
    try:
        resp = requests.get(url, auth=auth)
        resp.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise ValueError('Bad url: %s requests says %s' % (url, err))
    return resp
    

@app.route('/runs', methods=['GET', 'POST'])
def create_run():
    try:
        url = request.args.get('build_url')
        user = request.args.get('user')
        password = request.args.get('password')
    except KeyError as err:
        return 'Wrong url parameters! \nExpecting %s from jenkins.' % err
    if url.endswith('/'):
        url = url[:-1]
    # make configurable
    try:
        json_resp = requests_get('%s/api/json' % url, auth=(user, password))
        subunit_data = requests_get('%s/artifact/subunit.stream' % url, 
                                    auth=(user, password))
    except ValueError as err:
        return 'Failed getting build info... %s' % err
    try:
        parameters = get_metadata(json_resp)
    except ValueError as err:
        return 'Looks like your test json data is bad: %s' % err
    try:
        subunit_file = io.BytesIO(subunit_data.content)
    except ValueError as err:
        return 'Looks like your subunit stream is bad: %s' % err
    stream = read_subunit.ReadSubunit(subunit_file)
    shell.process_results(stream.get_results())
    shell.CONF.set_override('run_meta', metadata)
    shell.process_results(stream.get_results())

    
def main():
    config = ConfigParser.ConfigParser()
    config.read(['etc/jenkins2sql.conf'])
    host = config.get('default', 'host', '127.0.0.1')
    try:
        port = config.getint('default', 'port')
    except ConfigParser.NoOptionError:
        port = 5000
    db_uri = config.get('default', 'db_uri')
    shell.cli_opts()
    shell.parse_args([])
    shell.CONF.set_override('connection', db_uri, group='database')
    app.run(debug=True, host=host, port=port)
 

if __name__ == "__main__":
   main()

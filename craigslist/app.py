import subprocess
import os
from datetime import datetime
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/scrape')
def scrape():
    """
    Run spider in another process and store items in file. Simply issue command:

    > scrapy crawl spidername -o "output.json"

    wait for  this command to finish, and read output.json to client.
    """
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
    # /scrape?filename=jsonfilename
    filename = request.args.get('filename', default='output_'+date_time, type=str)
    output_json = filename + '.json'
    spider_name = "jobs"
    subprocess.check_output(['scrapy', 'crawl', spider_name, "-o", 'output/' + output_json])
    return render_template("scrape.html", output=output_json)


@app.route('/output-json')
def output_json():
    files = os.listdir('output')
    files = [file for file in files]
    return render_template('output-json.html', files=files)


@app.route('/output-json/<filenamejson>')
def read_json(filenamejson, static_folder="output"):
    output_path = os.path.join(static_folder, filenamejson)
    with open(output_path) as json_file:
        return json_file.read()


if __name__ == '__main__':
    app.run(debug=True)

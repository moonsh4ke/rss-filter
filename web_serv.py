from flask import Flask, Response, render_template_string, request
from rss_fetcher import fetch_rss

app = Flask(__name__)

@app.post("/add_feed")
def save_rss():
    print(request.form['channel'])
    return "success"


@app.route("/youtube/<string:channel_id>")
def hello_world(channel_id):
    
    view_count_gt = request.args.get("view_count_gt")
    if view_count_gt == None:
        view_count_gt = 0
    else:
        view_count_gt = int(view_count_gt)

    content = fetch_rss(channel_id, view_count_gt)

    return Response(content, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, redirect, url_for, jsonify, render_template_string, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("./home.html")

# Route for redirecting based on the key
@app.route('/<key>')
def redirect_to_url(key):
    # Connect to dynamo db and get the config json
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('GeneralConfigs')

    try:
        response = table.get_item(
            Key={
                'key': "url_redirect_config"
            }
        )

        if 'Item' in response:
            url_mappings = response['Item']["url_mappings"]
        else:
            return "an error occurred on our end. Sorry about that"

    except Exception as e:
        return "an error occurred on our end. Sorry about that"
    
    if key in url_mappings:
        return redirect(url_mappings[key])
    else:
        return render_template_string(f'<h1>No URL found for {key}</h1>')

if __name__ == "__main__":
    app.run(debug=True)
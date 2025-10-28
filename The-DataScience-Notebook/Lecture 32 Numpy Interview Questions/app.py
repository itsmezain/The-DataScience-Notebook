# ipl webpage

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get('http://127.0.0.1:5000/api/teams')
    teams = response.json().get('teams')
    return render_template("index.html", teams = sorted(teams))


@app.route('/teamvteam')
def team_vs_team():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    
    # Fetch the teams list again
    response_teams = requests.get('http://127.0.0.1:5000/api/teams')
    teams = response_teams.json().get('teams')
    
    # Fetch the team vs team record
    response = requests.get(f'http://127.0.0.1:5000/api/teamVteam?team1={team1}&team2={team2}')
    
    response = response.json()
    return render_template('index.html', teams=sorted(teams), result = response)

app.run(debug=True, port=7000)


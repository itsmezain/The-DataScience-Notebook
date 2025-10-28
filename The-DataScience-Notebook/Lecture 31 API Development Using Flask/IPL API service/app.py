from flask import Flask,jsonify, request
import ipl
import advanced_ipl_data_analysis
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

@app.route('/api/teams')
def teams():
    teams = ipl.teamsAPI()  # This returns a list, which jsonify converts to JSON.
    return jsonify(teams)


@app.route('/api/teamVteam')
def teamVteam():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    if team1 is None or team2 is None:
        # Return an error response with status code 400 (Bad Request)
        return jsonify({"error": "Both team1 and team2 parameters are required"}), 400
    
    response = ipl.teamVteamAPI(team1, team2)
    return jsonify(response)
    

@app.route('/api/team-record')
def team_record():
    team_name = request.args.get('team')

    if team_name is None:
        # Return an error response with status code 400 (Bad Request)
        return jsonify({"error": "Team name parameters is required"}), 400
    response = advanced_ipl_data_analysis.teamAPI(team_name)
    return response
    
    
@app.route('/api/batting-record')
def batting_record():
    batsman_name = request.args.get('batsman')

    if batsman_name is None:
        # Return an error response with status code 400 (Bad Request)
        return jsonify({"error": "Team name parameters is required"}), 400
    response = advanced_ipl_data_analysis.batsmanAPI(batsman_name)
    return response


@app.route('/api/bowling-record')
def balling_record():
    bowler_name = request.args.get('bowler')

    if bowler_name is None:
        # Return an error response with status code 400 (Bad Request)
        return jsonify({"error": "Team name parameters is required"}), 400
    response = advanced_ipl_data_analysis.bowlerAPI(bowler_name)
    return response


if __name__ == '__main__':
    app.run(debug=True)
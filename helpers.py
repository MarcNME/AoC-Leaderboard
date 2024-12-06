import requests

def getLeaderboard(leaderboardUrl: str, session: str):
    cookies={'session': session}
    response = requests.get(leaderboardUrl, cookies=cookies)
    
    if(response.ok):
        members = list(response.json()['members'].values())
        members = sorted(members, key=lambda x: x['stars'], reverse=True)
        
        return members
    else:
        RuntimeError("Could not get Leaderboard")
        
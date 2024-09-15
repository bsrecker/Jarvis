import requests
from datetime import datetime as dt


class Soccer:
    API_KEY = None
    BASE_URL = "http://api.football-data.org/v4/"
    def __call__(self, jarvis, s):
        print('\nFeature powered by football-data.org APIs')
        self.API_KEY = input('Enter an API key by registering at football-data.org/client/register: ')
        while requests.get(self.BASE_URL + 'competitions/2013/matches', headers = {'X-Auth-Token': self.API_KEY}).status_code == 403:
            self.API_KEY = input('Please enter a valid API key: ')
        end = False
        while not end:
            self.get_competitions()
            competition_id = input("Enter ID or \\0 to exit: ")
            self.get_matches(competition_id)

    def get_competitions(self):
        headers = {
            'X-Auth-Token': self.API_KEY
        }
        response = requests.get(self.BASE_URL + 'competitions', headers=headers)
        if response.status_code == 200:
            payload = response.json()
            competitions = payload['competitions']
            print(f"\033[90m{' Competitions ':—^40}")
            for competition in competitions:
                print(f"\033[0m{competition['name']:<30} (ID: \033[90m{competition['id']}\033[0m{''})")
            print()
        else:
            print('Error retrieving API based data - ' + str(response.status_code))


    def get_matches(self, competition_id: str):
        print()
        headers = {
            'X-Auth-Token': self.API_KEY
        }
        curr = dt.now()
        year_to = curr.year
        if curr.month == 12:
            year_to += 1
        day = ''+str(curr.day)
        if curr.day < 10:
            day = '0' + day
        parameters = {
            'dateFrom'  :   f'{curr.year}-{curr.month}-{day}',
            'dateTo'    :   f'{year_to}-{(curr.month + 1)%12}-{day}'
        }
        if curr.month < 10:
            parameters['dateFrom'] = f'{curr.year}-0{curr.month}-{day}'
        if curr.month < 9:
            parameters['dateTo'] = f'{year_to}-0{(curr.month + 1)%12}-{day}'
        URL = f'{self.BASE_URL}competitions/{competition_id}/matches'
        response = requests.get(URL, params=parameters, headers=headers)
        payload = response.json()
        if response.status_code == 200:
            matches = payload['matches']
            if len(matches) == 0:
                print('No match data available in the upcoming month')
                return
            count = 0
            for match in matches:
                if count == 15:
                    break
                count += 1
                home = f'{match["homeTeam"]["shortName"]} ({match["homeTeam"]["tla"]})'
                away = f'{match["awayTeam"]["shortName"]} ({match["awayTeam"]["tla"]})'
                finished = match["status"] == "FINISHED"
                home_goals = match["score"]["fullTime"]["home"]
                away_goals = match["score"]["fullTime"]["away"]
                if home_goals is None:
                    home_goals = ' '
                    away_goals = ' '
                time = match["utcDate"]
                print(f'\033[0m{time[0:10]:—^68}')
                print(f'\033[94m{home:<30}{home_goals}  \033[0m--- \033[95m{away_goals} {away:>30}\n')
        else:
            print('Error retrieving API based data - ' + str(response.status_code))


def main():
    soccer = Soccer()
    soccer("","")


if __name__ == '__main__':
    main()
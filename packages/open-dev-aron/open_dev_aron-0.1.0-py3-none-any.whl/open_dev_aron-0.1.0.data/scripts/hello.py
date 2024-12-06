#!python
import requests

def hello():
    c = requests.get('https://api.github.com/repos/insper/dev-aberto/commits')
    info = c.json()
    commit_info = info[0]['commit']['author']
    return commit_info['date'], commit_info['name']

if __name__ == "__main__":
    date, name = hello()
    print(f"Último commit feito em: {date} por: {name}")

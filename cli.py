# -*- coding: utf-8 -*-
import sys
import time
from tabulate import tabulate
import bs4 as bs
import requests
import pickle
import numpy as np


class IronMan:
    def get_characters(self):
        resp = requests.get('https://supersmashbros.fandom.com/wiki/List_of_Super_Smash_Bros._series_characters')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        ret = {}
        for row in table.findAll('tr')[1:]:
            info = row.findAll('td')
            try:
                name = info[1].find('small').text
                number = int(info[0].text)
                photo_link = info[1].find('a', {'class': 'image image-thumbnail'})['href']
                ret[number] = {'name': name, 'photo': photo_link}
            except:
                continue

        chars = []
        for (key, value) in ret.items():
            chars.append(value['name'])
        print(chars)
        return ret

    def choose_chars(self):
        ret = []
        x = np.random.randint(len(self.ALL_CHARS), size=(self.n_chars))
        x = np.sort(x)
        for i, char in enumerate(self.ALL_CHARS):
            if i in list(x):
                ret.append(char)
        p1 = ret
        p2 = p1[::-1]
        return ret, p1, p2

    def __init__(self, player1, player2, n_chars, include_dlc = False):

        # Deprecated
        # self.ALL_CHARS = self.get_characters()
        self.ALL_CHARS = ['Mario', 'Donkey Kong', 'Link', 'Samus', 'Yoshi', 'Kirby', 'Fox', 'Pikachu', 'Luigi', 'Ness', 'Captain Falcon', 'Jigglypuff', 'Peach', 'Bowser', 'Ice Climbers', 'Sheik', 'Zelda', 'Dr. Mario', 'Pichu', 'Falco', 'Marth', 'Young Link', 'Ganondorf', 'Mewtwo', 'Roy', 'Mr. Game & Watch', 'Meta Knight', 'Pit', 'Zero Suit Samus', 'Wario', 'Snake', 'Ike', 'Pokemon Trainer', 'Diddy Kong', 'Lucas', 'Sonic', 'King Dedede', 'Olimar', 'Lucario', 'R.O.B.', 'Toon Link', 'Wolf', 'Villager', 'Mega Man', 'Wii Fit Trainer', 'Rosalina & Luma', 'Little Mac', 'Greninja', 'Mii Brawler', 'Mii Swordfighter', 'Mii Gunner', 'Palutena', 'Pac-Man', 'Robin', 'Shulk', 'Bowser Jr.', 'Duck Hunt', 'Ryu', 'Cloud', 'Corrin', 'Bayonetta', 'Inkling', 'Ridley', 'Simon', 'King K. Rool', 'Isabelle', 'Incineroar', 'Piranha Plant', 'Joker', 'Hero', 'Banjo & Kazooie', 'Terry', 'Byleth', 'Min Min']
        if not include_dlc:
            self.ALL_CHARS = self.ALL_CHARS[:-7]

        self.n_chars = int(n_chars)
        self.p1 = player1
        self.p2 = player2

        self.refresh_characters()
        self.wins = [] * ((self.n_chars * 2) - 1)
        self.match = 0

        self.show_session()

    def show_session(self):
        print("---------------------------------------------------")
        print("Playing Mang0 / Axe Wednesday with {} characters".format(self.n_chars))
        print("---------------------------------------------------")
        print()

        print(tabulate({self.p1: self.p1chars, self.p2: self.p2chars}, headers='keys'))


    def refresh_characters(self):
        self.character_set, self.p1chars, self.p2chars = self.choose_chars()

    def getp1chars(self):
        return self.p1chars

    def getp2chars(self):
        return self.p2chars

    def get_charset(self):
        return self.character_set

    """ Player input is either 1 or 2, corresponding to which player won """
    def win(self, player):
        self.p1dubs[self.match] = (player == 1)
        self.p2dubs[self.match] = (player == 2)
        self.match = self.match + 1

def main(argv):
    iron_man_start = time.time()
    sesh = IronMan(argv[0], argv[1], argv[2])
    
    time.time() - iron_man_start

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Please provide the following command line arguments:")
        print("<Player 1 Name> <Player 2 Name> <Number of Characters>")
        exit()

    main(sys.argv[1:])

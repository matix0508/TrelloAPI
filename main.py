# This code sample uses the 'requests' library:
# http://docs.python-requests.org
from typing import List

import requests
import json

KEY = None
TOKEN = None


class Member:
	def __init__(self):
		self.id = None
		self.username = None
	
	def __repr__(self) -> str:
		return self.username


class Card:
	def __init__(self):
		self.id = None
		self.name = None
		self.members = []
	
	def __repr__(self) -> str:
		return self.name


def get_card_members(card_id: str) -> List[Member]:
	url = f"https://api.trello.com/1/cards/{card_id}/members"
	
	query = {
		'key': KEY,
		'token': TOKEN
	}
	
	response = requests.request(
		"GET",
		url,
		params=query
	)
	members = []
	for item in json.loads(response.text):
		member = Member()
		member.id = item['id']
		member.username = item['username']
		members.append(member)
	return members


def get_cards_from_list(list_id: str) -> List[Card]:
	url = f"https://api.trello.com/1/lists/{list_id}/cards"
	query = {
		'key': KEY,
		'token': TOKEN
	}
	response = requests.request(
		"GET",
		url,
		params=query
	)
	cards = []
	
	cards_json = json.loads(response.text)
	for item in cards_json:
		card = Card()
		card.id = item['id']
		card.name = item['name']
		
		card.members = get_card_members(card.id)
		
		cards.append(card)
	return cards


def create_card(name: str, list_id: str) -> None:
	url = "https://api.trello.com/1/cards"
	
	query = {
		'key': KEY,
		'token': TOKEN,
		'idList': list_id,
		'name': name
	}
	
	requests.request(
		"POST",
		url,
		params=query
	)


def update_card(card_id: str, key: str, value: str) -> None:
	url = f"https://api.trello.com/1/cards/{card_id}"
	
	headers = {
		"Accept": "application/json"
	}
	
	query = {
		'key': KEY,
		'token': TOKEN,
		key: value
	}
	
	requests.request(
		"PUT",
		url,
		headers=headers,
		params=query
	)
	print('done')


def move_card(card_id: str, list_id: str) -> None:
	update_card(card_id, 'idList', list_id)


def join_member(card_id: str, member_id: str) -> None:
	url = f"https://api.trello.com/1/cards/{card_id}/idMembers"
	
	query = {
		'key': KEY,
		'token': TOKEN,
		'value': member_id
	}
	
	response = requests.request(
		"POST",
		url,
		params=query
	)


def remove_member(card_id: str, member_id: str) -> None:
	url = f"https://api.trello.com/1/cards/{card_id}/idMembers/{member_id}"
	
	query = {
		'key': KEY,
		'token': TOKEN
	}
	
	response = requests.request(
		"DELETE",
		url,
		params=query
	)

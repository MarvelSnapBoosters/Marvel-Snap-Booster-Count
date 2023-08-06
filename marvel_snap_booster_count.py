import json
import os
import csv

# Get path of local JSON
path = os.path.expanduser('~/AppData/Locallow/Second Dinner/SNAP/Standalone/States/nvprod/CollectionState.json')

# Open local JSON and parse
all_cards = {}
with open(path, encoding="utf-8-sig") as json_file:
	data = json.load(json_file)

	# Get variant count
	for card in data['ServerState']['Cards']:
		card_name = card['CardDefId']
		if card_name not in all_cards:
			all_cards[card_name] = {}
			all_cards[card_name]['variants'] = []
		if 'ArtVariantDefId' in card: 
			if card['ArtVariantDefId'] not in all_cards[card_name]['variants']:
				all_cards[card_name]['variants'].append(card['ArtVariantDefId'])

	# Get booster count
	for card in data['ServerState']['CardDefStats']['Stats']:
		card_name = card

		# Either don't own card, or is non-collectible card
		if 'Boosters' not in data['ServerState']['CardDefStats']['Stats'][card]:
			continue

		current_boosters = data['ServerState']['CardDefStats']['Stats'][card]['Boosters']
		lifetime_boosters = data['ServerState']['CardDefStats']['Stats'][card]['BoostersLifetime']
		if 'InfinitySplitCount' in data['ServerState']['CardDefStats']['Stats'][card]:
			infinity_splits = data['ServerState']['CardDefStats']['Stats'][card]['InfinitySplitCount']
		else:
			infinity_splits = 0

		all_cards[card_name]['current_boosters'] = current_boosters
		all_cards[card_name]['lifetime_boosters'] = lifetime_boosters
		all_cards[card_name]['infinity_splits'] = infinity_splits

# Write to local file
with open('marvel_snap_booster_count.csv', 'w', newline='') as csv_file:
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(["Card", "Boosters", "Lifetime Boosters", "Total Variants", "Infinity Splits"])
	for card in all_cards:
		csv_writer.writerow([card, all_cards[card]['current_boosters'], all_cards[card]['lifetime_boosters'], len(all_cards[card]['variants']), all_cards[card]['infinity_splits']])

#!/user/bin/env python3
#character.py

class Character(object):

	# TODO: skills, affinity, race, condition, support, associations, biorhythm, level
	def __init__(self, name, charClass, primaryStats, secondaryStats, inventory, weaponRanks, biorhythm):
		self.name = name
		self.characterClass = charClass
		self.primaryStats = primaryStats
		self.secondaryStats = secondaryStats
		self.inventory = inventory
		self.weaponRanks = weaponRanks
		self.biorhythm = biorhythm # TODO: add class for this

	def getName(self):
		return self.name

	def getClass(self):
		return self.characterClass

	def getPrimaryStats(self):
		return self.primaryStats

	def getSecondaryStats(self):
		return self.secondaryStats

	def getStat(name):
		return self.primaryStats.getStatByName(name)

	def getInventory(self):
		return self.inventory

	def getWeaponRanks(self):
		return self.weaponRanks

	def getBiorhythm(self):
		return self.biorhythm


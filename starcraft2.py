import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, \
    CYBERNETICSCORE, STALKER 
import random

class myBot(sc2.BotAI):
    async def on_step(self, iteration):
        # what to do every step
        await self.distribute_workers()  # in sc2/bot_ai.py
        await self.build_workers() # our method to build workers
        await self.build_pylons() # our method to build pylons
        await self.expand() # our expand method
        await self.build_assimilator() # our method for getting gas
        await self.offensive_force_buildings() # prep the AIrmy
        await self.build_offensive_force() # build the AIrmy
        await self.attack() # self explanatory

    async def build_workers(self):
        # nexus is a command center in Starcraft
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE): 
                await self.do(nexus.train(PROBE))

    async def build_pylons(self): 
        # make sure a pylon is not already being built
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists: 
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=nexuses.first)

    async def expand(self):
        # expansion currently limited to only 2 nexuses, may change later
        if self.units(NEXUS).amount < 2 and self.can_afford(NEXUS):
            await self.expand_now()

    async def build_assimilator(self):
        # will build an assimilator on a geyser if it is close enough to nexus and able to afford it
        for nexus in self.units(NEXUS).ready: 
            vaspenes = self.state.vespene_geyser.closer_than(25.0, nexus)
            for vaspene in vaspenes: 
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None: 
                    break 
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(ASSIMILATOR, vaspene))

    async def offensive_force_buildings(self):
        # when able, will build CYBERNETICSCORE and GATEWAY
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random
            if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon)
            # no more than 3 GATEWAYs will be built 
            elif len(self.units(GATEWAY)) < 3:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)

    async def build_offensive_force(self):
        # trains a stalker unit when able 
        for gw in self.units(GATEWAY).ready.noqueue:
            if self.can_afford(STALKER) and self.supply_left > 0:
                await self.do(gw.train(STALKER))

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    def find_target(self, state):
        # go to where known units are
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        # go to where known structures are
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        # go to the enemy start location
        else: 
            return self.enemy_start_locations[0]

    async def attack(self):
        # attack if there's a lot of units doing nothing
        if self.units(STALKER).amount > 15:
            for s in self.units(STALKER).idle: 
                await self.do(s.attack(self.find_target(self.state)))
        # attack if there's at least 3 units and there are known enemies or enemy structures 
        elif self.units(STALKER).amount > 3: 
            if len(self.known_enemy_units) > 0 or len(self.known_enemy_structures) > 0: 
                for s in self.units(STALKER).idle: 
                    await self.do(s.attack(random.choice(self.known_enemy_units)))
            
# start the game!
run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, myBot()),
    Computer(Race.Terran, Difficulty.Medium)
], realtime=False) # realtime boolean for if you want sped up or real time

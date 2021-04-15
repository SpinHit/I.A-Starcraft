#Iliass Ben ammar 18908184 et Nithusan Sivakanthan 18905221
from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units, upgrades
from absl import app
import random, time

class TerranAgent(base_agent.BaseAgent):
    #on définie le constructeur pour la class TerraAgent
    def __init__(self):
        super(TerranAgent, self).__init__()
        self.attack_coordinates = None
        self.gas_built = False

    #permet de vérifier si l'unité a bien été séléctionner 
    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    #permet de renvoyer une liste des xxx
    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if unit.unit_type == unit_type]

    #permet de vérifier si on peu lancer l'action demander
    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    #Le Build order
    def step(self, obs):
        super(TerranAgent, self).step(obs)


        # on regarde ou on est positionner en debut de partie soit en haut soit en bas
        if obs.first():
            player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()
            #les coordonnées pour lancer l'attaque en fonction de notre position de depart
            if xmean <= 31 and ymean <= 31:
                self.attack_coordinates = (45, 42)
            else:
                self.attack_coordinates = (17, 20)

        #on selectionne nos marines et on les envoies a l'attaque 
        marines = self.get_units_by_type(obs, units.Terran.Marine)
        if len(marines) >= 15:
            if self.unit_type_is_selected(obs, units.Terran.Marine):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                    return actions.FUNCTIONS.Attack_minimap("now", self.attack_coordinates)

            if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                return actions.FUNCTIONS.select_army("select")

        mineraie = obs.observation.player.minerals

        #On forme les vcs
        scvs = self.get_units_by_type(obs, units.Terran.SCV)
        if self.unit_type_is_selected(obs, units.Terran.CommandCenter):
            if len(scvs) <= 16:
                if self.can_do(obs, actions.FUNCTIONS.Train_SCV_quick.id):
                    return actions.FUNCTIONS.Train_SCV_quick("now")

        
        ############################ 1 BUILD PREMIER DEPOT ##########################################
        #Pour construire le depot de ravitaillement il nous faut vérifier si on a les 100 minerai nécéssaire pour ca construction  + vérifier que les 14 vcs on était créer
        depot_ravitallement = self.get_units_by_type(obs, units.Terran.SupplyDepot)
        if len(scvs) <= 14:
            
            if len(depot_ravitallement) < 1 and mineraie >= 100:
                if self.unit_type_is_selected(obs, units.Terran.SCV):
                    if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                        x = random.randint(0, 83)
                        y = random.randint(0, 83)
                        return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))


        ################### 2 BUILD PREMIERE CASERNE #######################################
        #Pour construire la caserne on check si on a les 150 minerai nécéssaire + vérifier si on a  les 16 vcs
        casernes = self.get_units_by_type(obs, units.Terran.Barracks)
        if len(scvs) <= 16:
            if len(casernes) < 1 and mineraie >= 150:
                if self.unit_type_is_selected(obs, units.Terran.SCV):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                        x = random.randint(0, 83)
                        y = random.randint(0, 83)
                        return actions.FUNCTIONS.Build_Barracks_screen("now", (x, y))


        ########################## 3 BUILD PREMIERE RAFINERY #########################################
        #on va construire la raffinerie et check d'abord si on a les 16 vcs et les 100 minerai nécéssaire
        refinery = self.get_units_by_type(obs, units.Terran.Refinery)
        if len(scvs) <= 16:
            if len(refinery) < 1 and mineraie >= 100:
                if self.unit_type_is_selected(obs, units.Terran.SCV):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                        x = random.randint(0, 83)
                        y = random.randint(0, 83)             
                        return actions.FUNCTIONS.Build_Refinery_screen("now", (x, y))
        


        ########################## 4 BUILD DEUXIEME DEPOT #########################################
        if len(depot_ravitallement) == 1 and mineraie >= 100:
                if self.unit_type_is_selected(obs, units.Terran.SCV):
                    if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                        x = random.randint(0, 83)
                        y = random.randint(0, 83)
                        return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))

        ########################## 5 BUILD DEUXIEME CASERNE #########################################
        if len(scvs) <= 16:
            if len(casernes) == 1 and mineraie >= 150:
                if self.unit_type_is_selected(obs, units.Terran.SCV):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                        x = random.randint(0, 83)
                        y = random.randint(0, 83)
                        return actions.FUNCTIONS.Build_Barracks_screen("now", (x, y))
        
        ########################## 6 UPGRADE LE COMMAND CENTER  #########################################
   
        # if len(casernes) < 3 and mineraie >= 150: # on check si on peu upgrade le command center
        # return combinedActions.append(cc(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND))  


        # variables pour connaitre le nombre d'unités         
        marines = self.get_units_by_type(obs, units.Terran.Marine)
        nbrUnits = len(marines) + len(scvs)

        ########################## 8 BUILD TROISIEME CASERNE    #########################################
        if nbrUnits <= 22:
            if len(casernes) == 2 and mineraie >= 150:
                if self.unit_type_is_selected(obs, units.Terran.SCV):
                    if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                        x = random.randint(0, 83)
                        y = random.randint(0, 83)
                        return actions.FUNCTIONS.Build_Barracks_screen("now", (x, y))

        


        ########################## 9 BUILD CONSTAMENT DES MARINES ######################################
        #On commence a créer nos marines pour l'attaque
        if len(casernes) == 3:
            if self.unit_type_is_selected(obs, units.Terran.Barracks):
                marines = self.get_units_by_type(obs, units.Terran.Marine)
                if len(marines) <= 15:
                    if self.can_do(obs, actions.FUNCTIONS.Train_Marine_quick.id):
                        return actions.FUNCTIONS.Train_Marine_quick("now")

            b = random.choice(casernes)
            return actions.FUNCTIONS.select_point("select_all_type", (b.x, b.y))

        
        ######################## 10 BUILD  CONSTAMENT DES DEPOTS #######################################
        if len(casernes) > 2 and mineraie >= 100:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                    x = random.randint(0, 83)
                    y = random.randint(0, 83)
                    return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))

        

        #on séléctionne les serviteurs au cas ou les actions précédentes ne seraient pas passer.
        if len(scvs) > 0:
            scv = random.choice(scvs)
            return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

        return actions.FUNCTIONS.no_op()





#parametres de lancement de partie
def main(unused_argv):
    agent = TerranAgent()
    try:
        while True:
            with sc2_env.SC2Env(
                map_name ="Simple64",
                #terran VS l'une des trois races en mode easy.
                players=[sc2_env.Agent(sc2_env.Race.terran),
                         sc2_env.Bot(sc2_env.Race.random, sc2_env.Difficulty.very_easy)],
                agent_interface_format = features.AgentInterfaceFormat(
                    feature_dimensions = features.Dimensions(screen=84, minimap=64),
                    use_feature_units = True
                ),
                #vitesse de jeu
                step_mul = 16,
                # l'orceque on met game_steps_per_episode a 0 la partie continura jusqu'a qu'il y est une victoire ou défaite
                game_steps_per_episode = 0,
                #permet d'afficher un énorme tableau graphique 
                visualize=True
            ) as env:

                agent.setup(env.observation_spec(), env.action_spec())
                timesteps = env.reset()
                agent.reset()

                #Boucle pour toujours recevoir les actions tants que l apartie n'est pas fini
                while True:
                    step_actions = [agent.step(timesteps[0])]
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)


    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    app.run(main)
# Maplestory Helper
For the calculation of the cost of upgrading equipment in Maplestory  
_Starforce and Epic potential calculation_ 

# General Description
Maplestory is an MMORPG with a sizeable player base. To progress through the game, good equipment is crucial.  
These equipment can be bought of the player market, or "created" by the players themselves.  

Due to the difficulty in the cost calculation, it can be a daunting task deciding whether to make one's own equipment or to purchase another player's.   

I created this tool to help myself and my friends make quick decision on purchases.  
As there are many factors in cost consideration, Monte Carlo method is used to average the cost instead of an expected value calculation,   
i.e. large number of simulations and averaged, before being presented as a result.  

_Values used in calcuations originate from the following two links:_
https://strategywiki.org/wiki/MapleStory/Spell_Trace_and_Star_Force
https://strategywiki.org/wiki/MapleStory/Potential_System

# Epic Potential Calculation
In Epic Potential calculation, type and rarity of the equipment is important in calculating the probability, while the level of the equipment determines the cost.  
A commonly-used value had been filled-in in advance to assist the user. 

After which, the estimated costs to achieve the different tiers of upgrades will be shown. 

![image](https://user-images.githubusercontent.com/80518234/147252036-36e9deca-b535-4dd0-9fe7-fb68f2c97e96.png)

# Starforce Calculation 
In Starfoce calculation, there is a chance of the equipment breaking, with the chance increasing according to the starforce level.  
This calculator takes into account the chances, as well as informing the user which level the equipment is most likely to break at. 

![image](https://user-images.githubusercontent.com/80518234/147252831-9ac1f671-8f93-4fd6-bce4-e2bd7e8bd6ed.png)

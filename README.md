# DiceGame
A simple dice game

# history
2024.07.21 Create basics


2024.07.22 Added buffs / multi enemy / skill mechaniques


2024.07.23 Added skill GUI (can use skills more easier) / Added areas (store, campfire, ruin, altar) / Added map adventure


2024.07.24 Completed map logic / Implement Joker => player gets to right-click it and choose one from the shown list above => then joker changes into it


2024.07.25 Added immediate attacking feature / Reworked Mirinae's skill / Now the game is rogue-like! 


2024.07.26 Shrinkable board / width, height are now possible to change



# To do

- change skill mechanism: you may dislearn skills and learn new skill into current slots!
- Main menu: character selection(cannot change once fixed) / can see character's information (number of tiles and skills etc.)
- make a fixed tile slot (player can choose one tile to be fixed in a location - when shrinking, it is not fixed anymore)
- add health bar object that saves target value and have a shrinking animation at every update (call update instead of directly changing self.hp and drawing health bar)
- add relics (few ~ 3)
- add various enemies (few ~ 3)
- 
- options screen: see player information etc.

WARNING: There might still be a bug in character selection. (초기화되지 않은 것들이 있거나 잠재적 에러가 있을 수 있음. 특히 deep copy를 하지 않고 쓰는 변수를 사용할 경우 저번 게임에 줬던 영향이 지금 줄수도 있으니 새 게임에서 참조하는 변수들은 왠만하면 딥카피해서 가지고 있게 하기 - 상점 변수 같은거 매번 상점 클래스 새로 만드는게 안전하긴 한데, 그럴때 사용하는 리스트나 딕셔너리같은거 내부적으로 딥카피해서 가지고 있기 또는 내부에서 항상 새로 생성하기)


### beyond beta version (further implementation will use Flutter instead of python)
- add relics

- add enemy spawning logics

- add characters

- simple hit animation

- add various enemies


# Character Concepts
Attack, defence, regeneration values are exponentially proportional to the number of tiles used, so it is important to use proper tiles.

### Mirinae the slayer
"Attack is the best defence"


A deck that focuses on attack rather than defense and recovery. 
She has an ultimate ability that allows her to collect a lot of attack tiles and inflict great damage, making it advantageous against strong enemies. Vulnerability can provide synergy.
A martial art skill can withstand situations with few attack tiles. 
In addition, it has wide-area and counterattacks, so it can stably deal with multiple enemies. 
You can take advantage of the opportunity to turn the tables by using the skill to convert all defense tiles into attack tiles.

### Cinavro the gambler
"It's not manipulation, it's my skills"


A deck that exploits 'Joker' tiles that can be used as any tiles you want. 
This makes the game easy, so his skills are weakened compared to other characters.


### Narin the conservator of Karma
"???"


Karma, a substance that replicates itself, is a tile that returns as harm to you when the board is reset.
Hence you must either wait for Karma to duplicate and use them all or must eliminate from the beginning.
Use various skills to explore the synergy! The most fun deck.


### Baron the knight
TBU (To Be Updated)



### Riri the cleric
TBU (To Be Updated)



### Ato the noble
TBU (To Be Updated)



### Arisu the explorer
TBU (To Be Updated)







# Music Credits
sanctuary: EN_OKAWA


YOIYAMI: keyta


情動カタルシス: まんぼう二等兵


Morning: しゃろう


anser: KK


Summer Wind


極東の羊、テレキャスターと踊る:しゃろう
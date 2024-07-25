# DiceGame
A simple dice game

# history
2024.07.21 Create basics


2024.07.22 Added buffs / multi enemy / skill mechaniques


2024.07.23 Added skill GUI (can use skills more easier) / Added areas (store, campfire, ruin, altar) / Added map adventure


2024.07.24 Completed map logic / Implement Joker => player gets to right-click it and choose one from the shown list above => then joker changes into it


2024.07.25 Added immediate attacking feature / Revised Mirinae's excaliber skill / Now the game is rogue-like! 



# To do
- add relics (few ~ 3)
- add various enemies (few ~ 3)
- Mirinae: skill balancing 
- Main menu: character selection(cannot change once fixed) / can see character's information (number of tiles and skills etc.)
- options screen: see player informations etc.

WARNING: There might still be a bug in character selection. (초기화되지 않은 것들이 있거나 잠재적 에러가 있을 수 있음. 특히 deep copy를 하지 않고 쓰는 변수를 사용할 경우 저번 게임에 줬던 영향이 지금 줄수도 있으니 새 게임에서 참조하는 변수들은 왠만하면 딥카피해서 가지고 있게 하기 - 상점 변수 같은거 매번 상점 클래스 새로 만드는게 안전하긴 한데, 그럴때 사용하는 리스트나 딕셔너리같은거 내부적으로 딥카피해서 가지고 있기 또는 내부에서 항상 새로 생성하기)


### beyond beta version (further implementation will use Flutter instead of python)
- add relics

- add enemy spawning logics

- add characters

- simple hit animation

- add various enemies

# Music Credits
sanctuary: EN_OKAWA


YOIYAMI: keyta


情動カタルシス: まんぼう二等兵


Morning: しゃろう


anser: KK


Summer Wind


極東の羊、テレキャスターと踊る:しゃろう
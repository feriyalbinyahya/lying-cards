import random
import copy
import time

class LyingCards:
    def __init__(self, human, ai, storage, garbage, must_last_card):
        self.human = human
        self.ai = ai
        self.storage_cards = storage
        self.garbage_cards = garbage
        self.must_last_card = must_last_card

    def get_storage_cards(self):
        return self.storage_cards

    def set_storage_cards(self, list_card):
        self.storage_cards = list_card

    def get_garbage_cards(self):
        return self.garbage_cards

    def get_2last_card(self):
        return self.get_garbage_cards()[-2]

    def get_card_from_storage(self):
        if len(self.get_storage_cards()) == 0:
            self.random_storage_cards()

        storage = self.get_storage_cards()

        new_card = self.get_storage_cards()[0]
        storage.remove(new_card)

        return new_card

    def get_must_last_card(self):
        return self.must_last_card

    def set_must_last_card(self, card):
        self.must_last_card = card

    def add_must_last_card(self):
        nextcard = (self.must_last_card + 1)%10
        if nextcard == 0:
            self.must_last_card = 10
        else:
            self.must_last_card = nextcard

    def random_storage_cards(self):
        list_card = self.remove_few_card()
        new_storage_cards = []

        #KOCOK KARTU UNTUK DI TARUH DI KOTAK PENYIMPANAN
        for i in range((len(self.get_garbage_cards())//2)-1):
            number = random.choice(list_card)
            list_card.remove(number)
            new_storage_cards.append(number)

        self.set_storage_cards(new_storage_cards)

    def remove_few_card(self):
        new_list_card = []
        for i in range((len(self.get_garbage_cards())//2)-1):
            number = self.get_garbage_cards()[i]
            (self.get_garbage_cards()).remove(number)
            new_list_card.append(number)
        return new_list_card

    def throw_card_to_garbage(self, player, number):
        garbage = self.get_garbage_cards()
        player.remove_card(number)
        self.add_must_last_card()
        garbage.append(number)

    def accuse_enemy(self):
        garbage = self.get_garbage_cards()
        if len(garbage) > 0:
            accused_card = garbage[-1]
            next_card = self.get_must_last_card()

            if next_card == accused_card:
                return False
            else:
                return True
        else:
            return False
    def move_garbage_to_enemy(self, enemy):
        garbage = self.get_garbage_cards()
        last_card = garbage[-1]
        enemy_card = enemy.get_cards()

        for i in range(len(garbage)-1):
            enemy_card.append(garbage[i])

        garbage.clear()
        garbage.append(last_card)

        self.set_must_last_card(last_card)

    def wrong_accuse(self, player):
        accuse_left = player.get_accuse_left()
        accuse_left -= 1
        player.set_accuse_left(accuse_left)

        print("WRONG ACCUSATION! " + str(accuse_left) + " accuse left")

        #KALO HUKUMAN JUGA DIBERLAKUKAN BAGI PENUDUH YANG SALAH
        self.move_garbage_to_enemy(player)

    def check_accuse(self, player):
        accuse_left = player.get_accuse_left()
        if accuse_left > 0:
            return True
        else:
            return False
        
        

class HumanPlayer:
    def __init__(self, cards):
        self.cards = cards
        self.accuse_left = 2

    def get_cards(self):
        return self.cards

    def get_accuse_left(self):
        return self.accuse_left

    def set_accuse_left(self, accuse_left):
        self.accuse_left = accuse_left

    def set_cards(self, new_cards):
        self.cards = new_cards

    def add_card(self, new_card):
        list_card = self.get_cards()

        list_card.append(new_card)
        
    def remove_card(self, card):
        list_card = self.get_cards()
        list_card.remove(card)

class AIPlayer:
    def __init__(self, cards, last_card):
        self.cards = cards
        self.accuse_left = 2
        self.last_card = last_card
        self.enemy_accuse_left = 2

    def get_cards(self):
        return self.cards

    def get_accuse_left(self):
        return self.accuse_left

    def set_accuse_left(self, accuse_left):
        self.accuse_left = accuse_left

    def set_cards(self, new_cards):
        self.cards = new_cards

    def add_card(self, new_card):
        list_card = self.get_cards()

        list_card.append(new_card)

    def remove_card(self, card):
        list_card = self.get_cards()
        list_card.remove(card)

    def add_last_card(self):
        self.last_card = (self.last_card + 1)%10

    def get_last_card(self):
        return self.last_card

    def reset_last_card(self, card):
        self.last_card = card

    def decrease_enemy_accuse_left(self):
        self.enemy_accuse_left -= 1

    def get_enemy_accuse_left(self):
        return self.enemy_accuse_left

    def want_accuse(self, number_enemy_card):
        count = 0
        for card in self.get_cards():
            if card == (self.get_last_card()+1):
                count += 1

        if count == 2:
            return True

        elif number_enemy_card <= self.get_accuse_left():
            return True
        else:
            return False

    def can_throw_card(self, next_card):
        if self.get_enemy_accuse_left() == 0:
            return True
        
        for card in self.get_cards():
            if card == next_card:
                return True

        return False

def main():
    storage_cards = [1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10]

    human_cards = []
    ai_cards = []
    garbage = []

    #HUMAN CARDS RANDOM
    for i in range(5):
        number = random.choice(storage_cards)
        storage_cards.remove(number)
        human_cards.append(number)

    
    #AI CARDS RANDOM
    for i in range(5):
        number = random.choice(storage_cards)
        storage_cards.remove(number)
        ai_cards.append(number)

    first_card = random.choice(storage_cards)
    garbage.append(first_card)
    
    print("Welcome to Lying Cards Game!\n")

    human = HumanPlayer(human_cards)
    ai = AIPlayer(ai_cards, first_card)

    game = LyingCards(human, ai, storage_cards, garbage, first_card)
    print("First card in garbage: " + str(game.get_garbage_cards()[-1]))

    while (len(human.get_cards()) != 0 and len(ai.get_cards()) != 0):
        print("This is your cards: " + str(human.get_cards()))
        print("Your turn!\n")
        command = input("Press any key down below\n1: get card in storage\n2: throw card\n3: accuse enemy!\n")

        if command == "1":
            card = game.get_card_from_storage()
            print("You pick a card from storage. (New card: " + str(card) + ")\n")
            human.add_card(card)
            time.sleep(2)

        elif command == "2":
            #HUMAN PLAY
            print("This is your cards: " + str(human.get_cards()))
            number = int(input("Which card do you wanna throw?"))
            game.throw_card_to_garbage(human, number)
            print("Discard card " + str(number) + "\n")
            time.sleep(2)
            print("The Computer AI turn...\n")
            time.sleep(3)

            if len(human.get_cards()) == 0:
                break

            #THE COMPUTER AI PLAY
            jumlah_enemy_card = len(human.get_cards())
            can_accuse_ai = game.check_accuse(ai)
            if can_accuse_ai:
                want_accuse = ai.want_accuse(jumlah_enemy_card)
                if want_accuse:
                    result = game.accuse_enemy()
                    if result:
                        print("YOU HAVE LIED! THE AI COMPUTER ACCUSING YOU!")
                        game.move_garbage_to_enemy(human)
                        time.sleep(1)
                        print("All cards in garbage move to your list cards\n")
                        time.sleep(2)
                        print("Last card in garbage: " + str(game.get_garbage_cards()[-1]))
                    else:
                        print("The AI Computer accusing you, but you didn't lie")
                        game.wrong_accuse(ai)


        elif command == "3":
            can_accuse = game.check_accuse(human)
            if can_accuse == False:
                print("You can't accuse enemy")
                continue
            print("YOU ACCUSE AN ANEMY! IS IT WRONG?")
            result = game.accuse_enemy()

            if result:
                print("YOU RIGHT! ENEMY IS LYING")
                game.move_garbage_to_enemy(ai)
            else:
                print("The Computer AI didn't lie!")
                print("Move all cards in garbage to your list card...")
                game.wrong_accuse(human)
                ai.decrease_enemy_accuse_left()
                time.sleep(1)
            time.sleep(2)

        else:
            print("Wrong key!")
            continue

        

        next_card = ((game.get_must_last_card())+1) % 10
        isThrow = ai.can_throw_card(next_card)
        if isThrow:
            game.throw_card_to_garbage(ai, next_card)
            print("The Computer AI discard card " + str(next_card) + " to garbage...\n")
        else:
            card = game.get_card_from_storage()
            print("The Computer AI pick a card from storage...\n")
            ai.add_card(card)
        time.sleep(3)

    if len(human.get_cards()) == 0:
        print("\nYOU WIN!!!\n")
    else:
        print("YOU LOSE!! All the enemy's cards is thrown")
                    

if __name__ == "__main__":
    main()


ult = 0;
xult = 0;
gold = 0;
pdamage = 20;
pdmg = 30;
import random;
import time;
from punch_type_menu import run_main_menu;
from punch_type_shop import run_map_select, run_shop;
from punch_type_difficulty import run_difficulty_menu;

crit = random.randint(1, 100);
player = 100;
7
pult = 1.5;
ehit = 0;
phit = 0;
x = 1;
a = 0;
b = 0;
c = 0;
next = 0;
cheat = 0;
crits = 0;
map2 = 0;
map3 = 0;
choice4 = 0;


def retry():
    global gold;
    global gol;
    global gg;
    global x;
    global player;
    global enemy;
    global ult;
    global pdmg;
    global next;
    global map2;
    global map3;

    if enemy <= 0:
        if choice2 == 1:
            gol = 500;
            gold += 500;

        elif choice2 == 2:
            gol = 800;
            gold += 800;
        elif choice2 == 3:
            gol = 1000;
            gold += 1000;

        print("");
        print("YOU WIN!");
        print("1.RETRY  HITS TAKEN: ", ehit);
        print("2.MENU   HITS GAVE: ", phit);
        if choice2 == 1:
            print("YOU'VE EARNED 500 GOLD", "CRITS: ", crits);
        if choice2 == 2:
            print("YOU'VE EARNED 800 GOLD", "CRITS: ", crits);
        if choice2 == 3:
            print("YOU'VE EARNED 1000 GOLD", "CRITS: ", crits);
            if choice4 == 1:
                map2 = 1;
                print("CONGRATULATIONS, YOU'VE UNLOCKED UNDERGROUND MAP");
            elif choice4 == 2:
                map3 = 1;
                print("CONGRATULATIONS, YOU'VE UNLOCKED BOXING RING MAP");
            elif choice4 == 3:
                print("CONGRATULATIONS, YOU ARE THE CHAMPION!!!");

        lamon = int(input("ENTER CHOICE: "));
        match lamon:
            case 1:
                gg = 1;
                player = 100;
                enemy = hp;
                pdmg = 30;

            case 2:
                x = 1;
                gg = 0;
                return;

    if player <= 0:
        if choice2 == 1:
            gol=150;
            gold += 150;
        elif choice2 == 2:
            gol = 300;
            gold += 300;
        elif choice2 == 3:
            gol = 450;
            gold += 450;
        print("YOU LOSE!");
        print("1.RETRY  HITS TAKEN: ", ehit);
        print("2. MENU   HITS GAVE: ", phit);
        gold += 50;
        print("YOU'VE EARNED ", gol, " GOLD       CRITS: ", crits);
        ulit = int(input("ENTER CHOICE: "));
        match ulit:
            case 1:
                gg = 1;
                player = 100;
                enemy = hp;
                pdmg = 30;
            case 2:
                x = 1;
                gg = 0;
                return;


def owned_set():
    owned = {"none"};
    if a == 1:
        owned.add("spiked");
    if b == 1:
        owned.add("bomb");
    if c == 1:
        owned.add("lava");
    return owned;


def shop():
    global gold;
    global a;
    global b;
    global c;
    _, gold, owned = run_shop(gold, owned_set(), "none", mode="shop");
    a = 1 if "spiked" in owned else 0;
    b = 1 if "bomb" in owned else 0;
    c = 1 if "lava" in owned else 0;


GLOVE_NUMBER = {"none": 1, "spiked": 2, "bomb": 3, "lava": 4};
DIFFICULTY_STATS = {1: (500, 10), 2: (1000, 25), 3: (1500, 50)};


def prepare_fight():
    global gg;
    global x;
    global choice4;
    global choice6;
    while True:
        picked_map = run_map_select(gold, (1, map2, map3));
        if picked_map == 0:
            return False;
        choice4 = picked_map;
        picked, _, _ = run_shop(gold, owned_set(), "none", mode="pick");
        if picked is not None:
            choice6 = GLOVE_NUMBER[picked];
            gg = 1;
            x = 0;
            return True;


def gamemenu():
    global x;
    global enemy;
    global hp;
    global dmg;
    global edmg;
    global choice2;
    global gg;

    gg = 0;
    if choice1 != 1:
        return;
    while True:
        choice2 = run_difficulty_menu();
        if choice2 not in (1, 2, 3):
            return;
        hp, dmg = DIFFICULTY_STATS[choice2];
        enemy = hp;
        edmg = dmg;
        if prepare_fight():
            return;


def fight():
    global player;
    global enemy;
    global ult;
    global gold;
    global phit;
    global ehit;
    global pdamage;
    global pdmg;
    global crits;

    ult = 0;
    ehit = 0;
    phit = 0
    while player > 0 and enemy > 0 and gg == 1:
        crit = random.randint(1, 100);

        if choice6 == 1:
            pdamage = 20;
            if ult >= 3:
                print("ULT ACTIVATED-TWIN PUNCH");
                pdamage *= 2;

        if choice6 == 2:
            pdamage = 20;
            if crit <= 25:
                pdamage *= 3;
                crits += 1;
            while ult >= 3:
                print("ULT ACTIVATED-BERSERK!!!!!!")
                pdamage *= 2.5;
                ult = 2;

        elif choice6 == 3:
            pdamage = 20 * 2;
            if ult >= 3:
                print("ULTIMATE ACTIVATED-BLOODLUST BANG!")
                pdamage *= 5;
                ult = 0;
                player += 5;

        elif choice6 == 4:
            pdamage = 20 * 1.5;

            if crit <= 30:
                pdamage = pdmg * 3;
                crits += 1;

            while ult >= 5:
                print("ULT ACTIVATED-LAVA MULTXXXX");
                pdmg += 30 * .30;
                phit += 1;
                ult = 4;

        letter = random.choice("QWERTY");
        letter2 = random.choice("QWERTYASDFGH");
        letter3 = random.choice("QWERTYASDFGHZXCVB");
        g = random.choice(["NICE!", "GOOD JOB", "WELL TIMED"]);
        say = random.choice(["WOOOOOOW!!!!", "WHOOOOOOOOHOOOO!!", "UNSTOPPABLE!!!", "UY BAGSAK!!"]);
        esay = random.choice(["AYAAAAAN NAAAA", "NGAWNGAW", "ARAYKUPOOOOO", "MAMAAAAAAA"]);
        print("ENEMY: ", enemy, "| PLAYER: ", player);
        if choice2 == 1:
            dmg = 10;
            print("EASY");
            print(letter);
            start = time.time();
            answer = input().upper();
            end = time.time();
            wrong = end - start;

            if enemy <= hp * 0.25:
                dmg = edmg * 2;

            if wrong <= 3:
                if answer == letter:
                    ult += 1;

                    print(ult);
                    if choice6 == 4:

                        if ult >= 5:

                            if crit <= 30:
                                print("CRITICAL!!!!");
                                print(say, " -", pdamage);
                                enemy -= pdamage;



                            elif crit > 30:

                                enemy -= pdmg;

                                print(say, " -", pdmg);



                        elif ult < 5:
                            if crit <= 30:

                                enemy -= pdamage;
                                print("CRITICAL!!!");
                                print(g, " -", pdamage);
                                phit += 1;
                            else:
                                enemy -= pdamage;
                                print(g, " -", pdamage);
                                phit += 1;



                        else:
                            enemy -= pdamage;
                            print(g, "-", pdamage);

                            phit += 1;
                    else:
                        enemy -= pdamage;
                        if choice6 == 2:
                            if crit <= 25:
                                print("CRITICAL!!!");
                                if ult <= 3:
                                    print(say, " -", pdamage);
                                else:
                                    print(g, " -", pdamage);
                            else:
                                print(g, " -", pdamage);
                        else:
                            print(g, " -", pdamage);

                        phit += 1;


                else:
                    player -= dmg;
                    if enemy <= hp * .25:

                        print(esay, "  -", dmg);
                        ehit += 1;
                    else:
                        print("WROOONG -", dmg);
                        ehit += 1;

                    ult = 0;
                    pdmg = 30;

            else:
                player -= dmg;

                if enemy <= hp * .25:

                    print(esay, "  -", dmg);
                    ehit += 1;
                else:
                    print("TOO SLOW  -", dmg);
                    ehit += 1;
                ult = 0;
                pdmg = 30;
            print("");

        elif choice2 == 2:
            dmg = 25;
            print("MEDIUM")
            print(letter2);
            start = time.time();
            answer = input().upper();
            end = time.time();
            wrong = end - start;
            if enemy <= hp * 0.25:
                dmg = edmg * 2;
            if wrong <= 2:
                if answer == letter2:
                    ult += 1;
                    print(ult);

                    if choice6 == 4:

                        if ult >= 5:
                            if crit <= 30:
                                print("CRITICAL!!!!");

                                print(say, "-", pdamage);
                                enemy -= pdamage;


                            elif crit > 30:

                                enemy -= pdmg;

                                print(say, "-", pdmg);







                        elif ult < 5:
                            if crit <= 30:

                                enemy -= pdamage;
                                print("CRITICAL!!!");
                                print(g, " -", pdamage);
                                phit += 1;
                            else:
                                enemy -= pdamage;
                                print(g, " -", pdamage);
                                phit += 1;



                        else:
                            enemy -= pdamage;
                            print(g, "-", pdamage);

                            phit += 1;
                    else:
                        enemy -= pdamage;
                        if choice6 == 2:
                            if crit <= 25:
                                print("CRITICAL!!!");
                                if ult <= 3:
                                    print(say, " -", pdamage);
                                else:
                                    print(g, " -", pdamage);
                            else:
                                print(g, " -", pdamage);
                        else:
                            print(g, " -", pdamage);

                        phit += 1;




                else:
                    player -= dmg;
                    if enemy <= hp * .25:

                        print(esay, "  -", dmg);
                        ehit += 1;
                    else:
                        print("WROOONG -", dmg);
                        ehit += 1;

                    ult = 0;
                    pdmg = 30;


            else:
                player -= dmg;

                if enemy <= hp * .25:

                    print(esay, "  -", dmg);
                    ehit += 1;
                else:
                    print("TOO SLOW  -", dmg);
                    ehit += 1;
                ult = 0;
                pdmg = 30;
            print("");

        elif choice2 == 3:
            dmg = 50;
            print("HARD");
            print(letter3);
            start = time.time();
            answer = input().upper();
            end = time.time();
            wrong = end - start;

            if enemy <= hp * 0.25:
                dmg = edmg * 2;

            if wrong <= 1.5:
                if answer == letter3:
                    ult += 1;
                    print(ult);
                    print(ult);

                    if choice6 == 4:
                        if ult >= 5:

                            if crit <= 30:
                                print("CRITICAL!!!!");
                                print(say, "-", pdamage);
                                enemy -= pdamage;

                            elif crit > 30:
                                enemy -= pdmg;
                                print(say, "-", pdmg);

                        elif ult < 5:
                            if crit <= 30:
                                enemy -= pdamage;
                                print("CRITICAL!!!");
                                print(g, " -", pdamage);
                                phit += 1;

                            else:
                                enemy -= pdamage;
                                print(g, " -", pdamage);
                                phit += 1;

                        else:
                            enemy -= pdamage;
                            print(g, "-", pdamage);
                            phit += 1;

                    else:
                        enemy -= pdamage;

                        if choice6 == 2:
                            if crit <= 25:
                                print("CRITICAL!!!");

                                if ult <= 3:
                                    print(say, " -", pdamage);

                                else:
                                    print(g, " -", pdamage);

                            else:
                                print(g, " -", pdamage);

                        else:
                            print(g, " -", pdamage);

                        phit += 1;

                else:

                    player -= dmg;

                    if enemy <= hp * .25:
                        print(esay, "  -", dmg);
                        ehit += 1;

                    else:
                        print("WROOONG -", dmg);
                        ehit += 1;

                    ult = 0;
                    pdmg = 30;

            else:

                player -= dmg;

                if enemy <= hp * .25:
                    print(esay, "  -", dmg);
                    ehit += 1;

                else:
                    print("TOO SLOW  -", dmg);
                    ehit += 1;

                ult = 0;
                pdmg = 30;
            print("");


while x == 1:
    choice1 = run_main_menu(gold);
    if choice1 == 2:
        shop();
    if choice1 == 1:

        gamemenu();
        while gg == 1:
            print("FIGHT!");
            fight();
            retry();
            while next == 1:
                print("FIGHT!");
                fight2();
                retry2();

    if choice1 == 3:
        print("THANK YOU!");
        exit();
    if choice1 == 110:
        print("YOU'VE UNLOCKED ALL GLOVES AND MAPS!")
        a = 1
        b = 1
        c = 1
        map2 = 1
        map3 = 1

        map3 = 1



import time
from colorama import Fore, Style, init

# Inicializa o colorama para cores no terminal
init(autoreset=True)


def display_intro():
    print(Fore.CYAN + Style.BRIGHT + "\n### O Enigma de Ravenscroft Manor ###")
    time.sleep(1)
    print(
        Fore.YELLOW
        + "\nEm uma noite fria e tempestuosa, cinco estranhos são convidados para a misteriosa Ravenscroft Manor..."
    )
    time.sleep(2)
    print(
        Fore.YELLOW
        + "\nVocês receberam cartas anônimas, prometendo revelações que mudarão suas vidas. Ao chegarem, as portas se fecham abruptamente atrás de vocês."
    )
    time.sleep(2)
    print(
        Fore.YELLOW
        + "\nUma voz ecoa pela mansão: 'Bem-vindos, desafiantes. Unam suas mentes e descubram os segredos que aqui repousam. Apenas os dignos escaparão.'"
    )
    time.sleep(3)


def explore_room():
    explored_estante = False
    explored_candelabro = False
    found_diary = False
    found_key_piece = False

    while True:
        print(Fore.GREEN + "\n=== Explorando o Saguão Principal ===")
        time.sleep(1)
        print(
            Fore.YELLOW
            + "\nA mansão é opulenta, mas há algo sombrio no ar. O chão de madeira range sob seus pés, e sombras dançam nas paredes à luz bruxuleante das velas."
        )
        time.sleep(2)
        print(Fore.YELLOW + "Escolham um ponto para explorar:")
        print(Fore.LIGHTMAGENTA_EX + "1. Investigar o retrato rasgado na parede.")
        print(Fore.LIGHTMAGENTA_EX + "2. Vasculhar a estante de livros antiga.")
        print(Fore.LIGHTMAGENTA_EX + "3. Examinar o candelabro deslocado.")
        print(Fore.LIGHTMAGENTA_EX + "4. Finalizar exploração e prosseguir.")

        choice = input(Fore.CYAN + "\nDigite o número da sua escolha: ").strip()
        if choice == "1":
            print(
                Fore.YELLOW
                + "\nO retrato parece ser de Lord Edmund Ravenscroft. Há marcas de arranhões, como se alguém tivesse tentado destruí-lo. Atrás da pintura, vocês encontram um cofre embutido na parede, mas sem combinação."
            )
            time.sleep(2)
            print(Fore.YELLOW + "Talvez haja pistas pela sala para abrir esse cofre.")
            time.sleep(2)
        elif choice == "2":
            print(
                Fore.YELLOW
                + "\nA estante está repleta de livros empoeirados. Um deles chama a atenção: um diário de Lord Ravenscroft. Nas páginas, ele menciona sua obsessão por lógica e paradoxos. Uma passagem destaca uma expressão: 'A porta que nunca se abre está sempre fechada ou prestes a se abrir.'"
            )
            found_diary = True
            explored_estante = True
            time.sleep(3)
        elif choice == "3":
            print(
                Fore.YELLOW
                + "\nO candelabro parece fora do lugar. Ao puxá-lo, uma porta secreta se abre, revelando uma pequena sala. Dentro, há metade de uma chave antiga."
            )
            found_key_piece = True
            explored_candelabro = True
            time.sleep(2)
        elif choice == "4":
            if found_diary and found_key_piece:
                print(
                    Fore.YELLOW
                    + "\nCom as pistas encontradas, vocês sentem que podem desvendar o enigma do cofre."
                )
                time.sleep(2)
                break
            else:
                print(Fore.RED + "\nVocês sentem que ainda há mais a descobrir aqui.")
                time.sleep(2)
        else:
            print(Fore.RED + "\nEscolha inválida. Tente novamente.")
    return puzzle_1(found_diary, found_key_piece)


def puzzle_1(found_diary, found_key_piece):
    print(Fore.BLUE + "\n=== Puzzle 1: O Cofre de Ravenscroft ===")
    time.sleep(1)
    if found_diary and found_key_piece:
        print(
            Fore.YELLOW
            + "Utilizando as pistas do diário e a metade da chave, vocês se aproximam do cofre. Há um painel com diferentes expressões lógicas. Lembrando das anotações de Lord Ravenscroft, vocês devem escolher a expressão correta para abrir o cofre.\n"
        )
    else:
        print(
            Fore.RED
            + "Sem as pistas necessárias, vocês não conseguem entender como abrir o cofre."
        )
        return False

    print(Fore.LIGHTMAGENTA_EX + "1. 'Está chovendo e não está chovendo.'")
    print(Fore.LIGHTMAGENTA_EX + "2. 'Ou está chovendo ou não está chovendo.'")
    print(
        Fore.LIGHTMAGENTA_EX + "3. 'Se hoje é domingo, então amanhã é segunda-feira.'"
    )
    print(
        Fore.LIGHTMAGENTA_EX + "4. 'Está chovendo se, e somente se, não está chovendo.'"
    )

    choice = input(Fore.CYAN + "\nDigite o número da sua escolha: ")
    if choice == "2":
        print(
            Fore.GREEN
            + "\nCorreto! O cofre se abre com um clique. Dentro, vocês encontram a outra metade da chave e um mapa antigo indicando um caminho pelo labirinto dos fundos da mansão.\n"
        )
        return True
    else:
        print(
            Fore.RED
            + "\nIncorreto. Um mecanismo é acionado, e o cofre se tranca ainda mais. Talvez devam revisitar as pistas.\n"
        )
        return False


def puzzle_2():
    explored_statue = False
    explored_fountain = False
    found_compass = False
    found_inscription = False

    print(Fore.BLUE + "\n=== Puzzle 2: O Labirinto dos Segredos ===")
    time.sleep(1)
    print(
        Fore.YELLOW
        + "Seguindo o mapa, vocês chegam a um labirinto coberto pela névoa. O silêncio é perturbador, quebrado apenas pelo som distante de água corrente."
    )
    time.sleep(3)

    while True:
        print(Fore.GREEN + "\n=== Explorando o Labirinto ===")
        time.sleep(1)
        print(Fore.YELLOW + "Escolham um ponto para explorar:")
        print(Fore.LIGHTMAGENTA_EX + "1. Examinar a estátua no cruzamento.")
        print(Fore.LIGHTMAGENTA_EX + "2. Investigar a fonte no centro do labirinto.")
        print(Fore.LIGHTMAGENTA_EX + "3. Procurar inscrições nas paredes.")
        print(Fore.LIGHTMAGENTA_EX + "4. Finalizar exploração e escolher uma porta.")

        choice = input(Fore.CYAN + "\nDigite o número da sua escolha: ").strip()
        if choice == "1":
            print(
                Fore.YELLOW
                + "\nA estátua representa um cavaleiro apontando para o leste. Na base, há uma inscrição: 'A verdade ilumina o caminho.'"
            )
            explored_statue = True
            time.sleep(2)
        elif choice == "2":
            print(
                Fore.YELLOW
                + "\nNa fonte, a água reflete estranhamente o céu. Ao tocar a água, uma bússola aparece flutuando. Ela aponta consistentemente para o norte, mesmo quando vocês a giram."
            )
            found_compass = True
            explored_fountain = True
            time.sleep(2)
        elif choice == "3":
            print(
                Fore.YELLOW
                + "\nNas paredes do labirinto, vocês encontram várias inscrições. Uma delas diz: 'Contradições levam a becos sem saída.'"
            )
            found_inscription = True
            time.sleep(2)
        elif choice == "4":
            if found_compass and found_inscription:
                print(
                    Fore.YELLOW
                    + "\nMunidos das pistas, vocês se sentem prontos para escolher a porta correta."
                )
                time.sleep(2)
                break
            else:
                print(
                    Fore.RED
                    + "\nTalvez seja melhor explorar um pouco mais antes de decidir."
                )
                time.sleep(2)
        else:
            print(Fore.RED + "\nEscolha inválida. Tente novamente.")

    print(
        Fore.YELLOW + "Três portas estão diante de vocês, cada uma com uma inscrição:"
    )
    time.sleep(2)
    print(Fore.LIGHTMAGENTA_EX + "1. 'Hoje é segunda-feira e hoje é sexta-feira.'")
    print(Fore.LIGHTMAGENTA_EX + "2. 'Se eu estou sonhando, então estou acordado.'")
    print(Fore.LIGHTMAGENTA_EX + "3. 'Ou o sol está brilhando ou a lua está no céu.'")

    choice = input(Fore.CYAN + "\nDigite o número da porta que desejam abrir: ")
    if choice == "1":
        print(
            Fore.RED
            + "\nVocês entram em um corredor que termina em uma parede. Um beco sem saída."
        )
        return False
    elif choice == "2":
        print(
            Fore.RED
            + "\nA porta se tranca atrás de vocês, e o chão começa a ceder. Vocês correm de volta para a entrada."
        )
        return False
    elif choice == "3":
        print(
            Fore.GREEN
            + "\nCorreto! A porta leva a uma passagem iluminada que os guia para fora do labirinto. As pistas sobre evitar contradições ajudaram vocês a escolher corretamente.\n"
        )
        return True
    else:
        print(
            Fore.RED
            + "\nEscolha inválida. O labirinto parece mudar à sua volta, confundindo-os ainda mais."
        )
        return False


def puzzle_3():
    explored_library = False
    explored_globe = False
    found_scroll = False
    found_tool = False

    print(Fore.BLUE + "\n=== Puzzle 3: A Biblioteca Perdida ===")
    time.sleep(1)
    print(
        Fore.YELLOW
        + "Vocês entram em uma biblioteca oculta, com estantes que se perdem de vista. O cheiro de livros antigos é reconfortante, mas há pouco tempo para apreciar."
    )
    time.sleep(3)

    while True:
        print(Fore.GREEN + "\n=== Explorando a Biblioteca ===")
        time.sleep(1)
        print(Fore.YELLOW + "Escolham um ponto para explorar:")
        print(Fore.LIGHTMAGENTA_EX + "1. Inspecionar o globo terrestre antigo.")
        print(Fore.LIGHTMAGENTA_EX + "2. Vasculhar os pergaminhos na mesa.")
        print(Fore.LIGHTMAGENTA_EX + "3. Examinar o mecanismo estranho no canto.")
        print(
            Fore.LIGHTMAGENTA_EX
            + "4. Finalizar exploração e interagir com o mecanismo."
        )

        choice = input(Fore.CYAN + "\nDigite o número da sua escolha: ").strip()
        if choice == "1":
            print(
                Fore.YELLOW
                + "\nO globo tem marcas em lugares específicos, formando uma sequência. Ao alinhá-los, uma gaveta secreta se abre, revelando uma ferramenta peculiar."
            )
            found_tool = True
            explored_globe = True
            time.sleep(2)
        elif choice == "2":
            print(
                Fore.YELLOW
                + "\nOs pergaminhos contêm escritos sobre antigos filósofos e suas teorias lógicas. Um deles detalha sobre proposições contingentes e como elas se aplicam em certas situações."
            )
            found_scroll = True
            time.sleep(2)
        elif choice == "3":
            if found_tool:
                print(
                    Fore.YELLOW
                    + "\nCom a ferramenta encontrada, vocês conseguem ativar o mecanismo. Ele parece ser um relógio astronômico, com símbolos representando diferentes proposições lógicas."
                )
                explored_library = True
                time.sleep(2)
            else:
                print(
                    Fore.RED
                    + "\nO mecanismo está travado. Talvez haja algo que possa ajudar a operá-lo."
                )
                time.sleep(2)
        elif choice == "4":
            if explored_library and found_scroll:
                print(
                    Fore.YELLOW
                    + "\nVocês se sentem confiantes para resolver o enigma do mecanismo."
                )
                time.sleep(2)
                break
            else:
                print(Fore.RED + "\nAinda há mais a descobrir antes de prosseguir.")
                time.sleep(2)
        else:
            print(Fore.RED + "\nEscolha inválida. Tente novamente.")

    print(
        Fore.YELLOW
        + "Para ativar o mecanismo, vocês devem selecionar a proposição correta:"
    )
    time.sleep(2)
    print(
        Fore.LIGHTMAGENTA_EX
        + "1. 'Se chover, então molharei, e se não chover, não molharei.'"
    )
    print(Fore.LIGHTMAGENTA_EX + "2. 'Hoje é terça-feira e não é terça-feira.'")
    print(
        Fore.LIGHTMAGENTA_EX + "3. 'Está ensolarado ou está chovendo, mas não ambos.'"
    )
    print(Fore.LIGHTMAGENTA_EX + "4. 'Se estou feliz, então estou sorrindo.'")

    choice = input(Fore.CYAN + "\nDigite o número da sua escolha: ")
    if choice == "3":
        print(
            Fore.GREEN
            + "\nCorreto! O mecanismo se ativa, e uma passagem se revela atrás de uma estante.\n"
        )
        return True
    else:
        print(
            Fore.RED
            + "\nIncorreto. O mecanismo trava e as luzes diminuem. Talvez devam reconsiderar as pistas.\n"
        )
        return False


def puzzle_4():
    print(Fore.BLUE + "\n=== Puzzle 4: O Salão dos Espelhos ===")
    time.sleep(1)
    print(
        Fore.YELLOW
        + "Vocês entram em um salão repleto de espelhos. Suas reflexões parecem observá-los atentamente. No centro, há um pedestal com um enigma final."
    )
    time.sleep(3)
    print(
        Fore.YELLOW
        + "Uma voz ecoa: 'A última verdade está diante de vocês. Escolham sabiamente e a liberdade será sua.'"
    )
    time.sleep(2)

    print(
        Fore.LIGHTMAGENTA_EX + "1. 'Se estou mentindo, então esta frase é verdadeira.'"
    )
    print(
        Fore.LIGHTMAGENTA_EX + "2. 'Apenas a verdade liberta, e a mentira aprisiona.'"
    )
    print(Fore.LIGHTMAGENTA_EX + "3. 'Esta frase é falsa.'")
    print(Fore.LIGHTMAGENTA_EX + "4. 'Tudo que digo é mentira.'")

    choice = input(Fore.CYAN + "\nDigite o número da sua escolha: ")
    if choice == "2":
        print(
            Fore.GREEN
            + "\nCorreto! Os espelhos se retraem, revelando a saída da mansão. A luz do sol invade o salão, iluminando seus rostos.\n"
        )
        return True
    else:
        print(
            Fore.RED
            + "\nIncorreto. Os espelhos se fecham, e vocês ficam presos em um labirinto de reflexões.\n"
        )
        return False


def main():
    display_intro()
    explore = (
        input(Fore.CYAN + "\nDesejam explorar a mansão? (sim/não): ").strip().lower()
    )
    if explore == "sim":
        if explore_room():
            if puzzle_2():
                if puzzle_3():
                    if puzzle_4():
                        print(
                            Fore.GREEN
                            + "\nParabéns! Vocês desvendaram todos os enigmas de Ravenscroft Manor e conquistaram sua liberdade!\n"
                        )
                    else:
                        print(
                            Fore.RED
                            + "\nO salão dos espelhos tornou-se seu cárcere. O mistério permanece...\n"
                        )
                else:
                    print(
                        Fore.RED
                        + "\nSem desvendar o mecanismo, vocês ficam presos na biblioteca eterna.\n"
                    )
            else:
                print(
                    Fore.RED + "\nPerdidos no labirinto, vocês não encontram saída.\n"
                )
        else:
            print(
                Fore.RED
                + "\nIncapazes de abrir o cofre, vocês não conseguem avançar. A aventura termina aqui.\n"
            )
    else:
        print(
            Fore.RED
            + "\nVocês decidiram não explorar a mansão. As portas permanecem fechadas. A aventura termina antes mesmo de começar.\n"
        )


if __name__ == "__main__":
    main()

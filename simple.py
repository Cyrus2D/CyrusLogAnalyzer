from BaseCode.Game import Game


def main(path):
    g = Game.read_log(path)
    g.analyse()
    g.print_analyse()
    return g.get_dictionary()


if __name__ == "__main__":
    path = 'Data/20190314135110-CYRUS_0-vs-HELIOS2018_1.rcg'
    main(path)

from BaseCode.Game import Game


def main(path):
    g = Game.read_log(path)
    g.analyse()
    g.print_analyse()
    return g.get_dictionary()


if __name__ == "__main__":
    path = 'Data'
    main(path)

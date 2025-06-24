
import Platform


class SubBotExample(Platform.Platform):

    # ctor
    def __init__(self):

        # call parent ctor
        super().__init__()

        self.counter = 0

    #
    # the user-defined logic for how this SubBot listens, navigates, and shoots
    #
    def command_and_control(self) -> None:
        """
        the user-defined logic for how this SubBot listens, navigates, and shoots
        """
        self.counter += 1
        print(f'Just chillin out, round {self.counter}!')




def main():

    # create an instance of our SubBot, and start it running
    myBot = SubBotExample()
    myBot.run()


if __name__ == '__main__':
    main()

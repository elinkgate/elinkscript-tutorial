from eLinkTaskMnger.TaskManager import *

app = ELinkApp("test")


@app.add_action
def hello_world():
    print("hello world")


def main():
    app.run()


if __name__ == '__main__':
    main()

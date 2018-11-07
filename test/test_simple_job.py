from eLinkTaskMnger.TaskManager import *
from eLinkTaskMnger.eLink import ActionStatus

app = ELinkApp("test")


@app.add_action(id="001")
def hello_world1():
    print("hello world ")
    time.sleep(5)
    print("test 1")


@app.add_action(id="002")
def test1():
    print("this is test 2")
    time.sleep(2)
    print("complete => remove test 2")
    # return ActionStatus.ACTION_COMPLETE


@app.add_action(id="003")
def test1():
    print("this is test 3")
    time.sleep(2)
    print("complete => remove test 3")
    # return ActionStatus.ACTION_COMPLETE


@app.add_action(id="004")
def test1():
    print("this is test 4")
    time.sleep(2)
    print("complete => remove test 4")
    return ActionStatus.ACTION_COMPLETE


def main():
    # hello_world()
    app.run()


if __name__ == '__main__':
    main()

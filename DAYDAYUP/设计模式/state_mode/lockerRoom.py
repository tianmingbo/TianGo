from template import Context, State
from myTeamView import MyTeamView
from footballView import FootBallView


class LockerRoom(Context):
    """
    管理lockerRoom下的状态
    """

    def __init__(self):
        super().__init__()
        self.add_state(MyTeamView("my team view"))
        self.add_state(FootBallView("football view"))
        self.set_view("my team view")

    def set_view(self, view):
        self._set_state_info(view)

    def get_view(self):
        return self._get_state_info()

    def show(self):
        state = self.get_state()
        if isinstance(state, State):
            state.show(self)


if __name__ == '__main__':
    locker_room = LockerRoom()
    locker_room.show()
    locker_room.set_view('football view')
    locker_room.show()

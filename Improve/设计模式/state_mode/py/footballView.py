from template import State, singleton


# 足球页面状态
@singleton
class FootBallView(State):

    def __init__(self, name):
        super().__init__(name)

    def show(self, context):
        print(f'{context.get_view()}')

    def is_match(self, state_info):
        return state_info == 'football view'

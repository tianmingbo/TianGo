from werkzeug.routing import Map, Rule

url_map = Map()  # 关键依赖: werkzeug.routing.Map
static_path = '/static'
# todo: 待深入 关键依赖: werkzeug.routing.Rule
url_map.add(Rule(static_path + '/<filename>',
                 build_only=True, endpoint='static'))

print(url_map)

from werkzeug.routing import Map,Rule
url_map = Map()    # 关键依赖: werkzeug.routing.Map

        if static_path is not None:    # 处理静态资源
            #
            # todo: 待深入 关键依赖: werkzeug.routing.Rule
            url_map.add(Rule(static_path + '/<filename>',
                                  build_only=True, endpoint='static'))
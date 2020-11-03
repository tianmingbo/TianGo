"""
conduct command message

@summary: provide the message handlers
@author: zoufei@witcomm.net
@date: 20200508
"""
import json
import time

from service.cloud.plan import PlanDeal
from service.device import DeviceMonitorThread
from service.tactics.emergency_control import EmergencyControlTactics
from traffic.das import TacticsDas, PlanDas, RoadDas, LaneDas, EquipmentDas
from traffic.das.phase import PhaseDas
from traffic.util.format import mqtt_command_list, tactics_number_mapping, road_status_teleseme_map, tactics_id_mapping
from util.log import loger
from util.share import SharedMemory
from util.util import list2maplist, listmap2newlistmap, zmq_request, zmq_push, get_device_status_report_info, \
    get_ip_addr_info
from settings import Config


class CommandConduct(object):
    """指令处理类"""

    emqx_config = None
    emqx_client = None

    @staticmethod
    def receive_command_handler(message):
        """接收云端指令消息

        Args:
            message: 消息体
        """
        msg = json.loads(str(message, encoding='utf8'))
        if isinstance(msg, dict) and 'info_type' in msg.keys() and 'request_id' in msg.keys() and \
                msg['info_type'] in mqtt_command_list:
            if msg['request_id'] in SharedMemory.request_ids:
                return

            loger.info('receive_command_handler {}'.format(msg), 'msg')

            SharedMemory.request_ids.append(msg['request_id'])

            # source 1:本地 2:云端 3:APP
            if msg.get('source', None) in [1, 2, 3] and msg.get('conductor', None):
                try:
                    zmq_push('mqtt_report', {
                        'topic': 'command',
                        'data': getattr(CommandConduct, msg['info_type'] + '_command')(msg)
                    })
                except Exception as e:
                    print(e)
            else:
                try:
                    zmq_push('mqtt_report', {
                        'topic': 'command',
                        'data': {
                            'info_type': msg['info_type'],
                            'request_id': msg['request_id'],
                            'code': 4007,
                            'msg': '权限错误',
                        }
                    })
                except Exception as e:
                    print(e)

    @staticmethod
    def get_update_info_handler(message):
        """固件升级消息

        Args:
            message: 消息体
        """
        # TODO 增加消息处理逻辑

    @staticmethod
    def get_road_status_handler(message):
        """路口设备禁用/删除消息

        Args:
            message: 消息体
        """
        # TODO 增加消息处理逻辑

    @staticmethod
    def get_road_info_command(msg):
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id']
        }
        try:
            with SharedMemory.app.app_context():
                road_info = SharedMemory.road_info
                control_detail = road_info['control_detail']
                if control_detail and 'gw_status' in control_detail.keys() \
                        and control_detail['gw_status'] in [1, 2]:
                    control_model = 2
                elif control_detail and 'cdn_status' in control_detail.keys() \
                        and control_detail['cdn_status'] in [0, 1, 2]:
                    control_model = 3
                elif control_detail and 'secret_status' in control_detail.keys() \
                        and control_detail['secret_status'] in [0, 1, 2]:
                    control_model = 4
                else:
                    control_model = 1
                lanes = LaneDas.get_lanes()
                PlanDas.get_plan_list()

                current_plan_info = SharedMemory.current_plan_info
                if current_plan_info and isinstance(current_plan_info, dict):
                    current_plan = {
                        'id': current_plan_info.get('id', 1),
                        'name': current_plan_info.get('name', '系统方案'),
                    }
                else:
                    current_plan = {
                        'id': 1,
                        'name': '系统方案',
                    }
                if msg.get('flag', None) == 1:
                    bubble, content = CommandConduct.get_road_info_bubble_content(control_model)
                else:
                    bubble, content = '', {}

                device_info = get_device_status_report_info(DeviceMonitorThread.status)

                ret = {
                    'area': road_info['region'],
                    'cross_num': road_info['number'],
                    'cross_name': road_info['name'],
                    'equipment_type': 1,
                    'longitude': road_info['longitude'],
                    'latitude': road_info['latitude'],
                    'cross_type': road_info['type'],
                    'phases_num': PhaseDas.get_phase_nums(),
                    'lane': list2maplist(lanes, 'phase_num', 'number'),
                    'abnormal_status': 1 if device_info['teleseme']['status'] == 1 else 3,
                    'abnormal_content': road_status_teleseme_map[device_info['teleseme']['status']],
                    'content': content,
                    'bubble': bubble,
                    'camera_status': CommandConduct.get_camera_status(),
                    'camera_info': CommandConduct.get_camera_info(),
                    'rarda_status': CommandConduct.get_radar_status(),
                    'radar_info': CommandConduct.get_radar_info(),
                    'signal_source': road_info['car_collect_type'],
                    'control_model': control_model,
                    'control_type': road_info['control_type'],
                    'control_plan': current_plan['id'],
                    'plan_info': listmap2newlistmap(PlanDas.get_plan_list(), 'number', 'name'),
                    'tactics_info': listmap2newlistmap(TacticsDas.get_tactics_base_info_list(), 'number', 'name'),
                    'device_info': device_info,
                    'emergency_status': road_info['control_detail']['emergency_status'],
                    'wsb_host': get_ip_addr_info(nic_name=Config.NIC_NAME)[0],
                    'wsb_port': Config.HTTP_PORT
                }
                data.update({'code': 200, 'msg': '成功', 'data': ret})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def control_emergency_command(msg):
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        try:

            res = zmq_request('tactics_control', {
                'action': 'start',
                'tactics': 'emergency_control',
                'params': {
                    'source': msg['source'],
                    'conductor': msg['conductor'],
                    'status': msg['control_emergency'],
                }
            })

            if res and 'error' in res and not res['error']:
                data.update({'code': 200, 'msg': '成功'})
            else:
                data.update({'code': 4001, 'msg': res['msg']})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})
        return data

    @staticmethod
    def edit_control_command(msg):
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        try:
            with SharedMemory.app.app_context():

                control_type = msg['control_type']
                resource_id = msg['control_plan']

                if resource_id and control_type == 1:  # 固定方案
                    from traffic.views.center import fixedplan_control
                    ok, message = fixedplan_control(resource_id, msg['source'], msg['conductor'])
                elif resource_id and control_type == 2:  # 策略控制
                    from traffic.views.center import tactics_control
                    ok, message = tactics_control(resource_id, msg['source'], msg['conductor'])
                else:
                    data.update({'code': 4005, 'msg': '参数错误'})
                    return data

                if not ok:
                    data.update({'code': 4009, 'msg': message})
                    return data

                SharedMemory.next_control_info = {
                    'control_model': 1,
                    'control_type': control_type,
                    'next_plan_id': resource_id,
                }
                data.update({'code': 200, 'msg': message})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def greenwave_origin_command(msg):
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
            'product_key': CommandConduct.emqx_config['PRODUCT_KEY'],
            'device_key': CommandConduct.emqx_config['DEVICE_KEY'],
        }
        try:
            request_data = {
                'action': 'start',
                'tactics': 'green_wave',
                'params': msg
            }
            if msg['greenwave_status'] == 1:
                action = 'start'
            elif msg['greenwave_status'] == 2:
                action = 'stop'
            elif msg['greenwave_status'] == 3:
                action = 'get_plan'
            else:
                raise Exception('greenwave_status: {}'.format(msg['data']['greenwave_status']))

            request_data['action'] = action
            ret = zmq_request('tactics_control', request_data)
            if not ret['error']:
                data.update({'code': 200, 'msg': '成功'})
            else:
                data.update({'code': 4001, 'msg': ret['msg']})

        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def greenwave_between_command(msg):
        """绿波方案下发指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
            'product_key': CommandConduct.emqx_config['PRODUCT_KEY'],
            'device_key': CommandConduct.emqx_config['DEVICE_KEY'],
        }
        try:
            request_data = {
                'action': 'setup',
                'tactics': 'green_wave',
                'params': msg
            }

            ret = zmq_request('tactics_control', request_data)
            if not ret['error']:
                data.update({'code': 200, 'msg': '成功'})
            else:
                data.update({'code': 4001, 'msg': ret['msg']})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def secret_service_command(msg):
        """特勤通行指令开始/结束/切换"""
        '''
        {
            "request_id":"qwertyuiop",
            "switch_status": 1,
            "direction":1,
            "info_type":"secret_service",
            "device_key":"",
            "product_key": "",
            "source":2,
            "conductor":"admin"
        }
        '''
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
            'product_key': CommandConduct.emqx_config['PRODUCT_KEY'],
            'device_key': CommandConduct.emqx_config['DEVICE_KEY'],
        }
        try:
            request_data = {
                'action': 'start',
                'tactics': 'secret_service',
                'params': msg
            }
            if msg['switch_status'] == 1:
                action = 'start'
            elif msg['switch_status'] == 2:
                action = 'stop'
            elif msg['switch_status'] == 3:  # 切换单方向放行方向
                action = 'switch'
            else:
                raise Exception('switch_status: {}'.format(msg['switch_status']))

            request_data['action'] = action
            ret = zmq_request('tactics_control', request_data)
            if not ret['error']:
                data.update({'execution_status': 1, 'error_reason': '成功'})
            else:
                data.update({'execution_status': 2, 'error_reason': ret['msg']})

        except Exception as e:
            data.update({'execution_status': 2, 'error_reason': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def coordinate_command(msg):
        """区域协调指令开始/停止
        :param msg:指令数据
        :return:
        """
        data = {
            'info_type': 'coordinate_resp',
            'request_id': msg['request_id'],
            'product_key': CommandConduct.emqx_config['PRODUCT_KEY'],
            'device_key': CommandConduct.emqx_config['DEVICE_KEY'],
        }
        try:
            request_data = {
                'action': 'start',
                'tactics': 'coordinate',
                'params': msg
            }
            if msg['data']['action'] == 'start':
                action = 'start'
            elif msg['data']['action'] == 'stop':
                action = 'stop'
            elif msg['data']['action'] == 'set_plan':
                action = 'setup'
            elif msg['data']['action'] == 'get_plan':
                action = 'get_plan'
            else:
                raise Exception('coordinate_status: {}'.format(msg['data']['action']))

            request_data['action'] = action

            if msg['data']['action'] in ['start', 'stop', 'set_plan']:
                ret = zmq_request('tactics_control', request_data)

                other_info = {'action': msg['data']['action'],
                              'coordinate_plan_id': msg['data']['coordinate_plan_info']['id']}
            else:
                ret, other_info = CommandConduct.get_plan_coordinate_tactics(msg)  # 获取相位、红绿灯信息

            if not ret['error']:
                data.update({'code': 200, 'msg': '成功'})
                data['data'] = other_info
            else:
                data.update({'code': 4001, 'msg': ret['message']})

        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def get_plan_coordinate_tactics(msg):
        """区域协调get_plan
        :param params: 参数列表
        :return:
        """
        try:
            ret = {'error': False, 'msg': '成功'}
            plan = SharedMemory.current_plan_info
            plan_info = []
            plan_phase_info = {}
            for i in range(len(plan['parts'])):
                plan_info.append(
                    [i + 1,
                     [plan['parts'][i]['green_time'], plan['parts'][i]['yellow_time'], plan['parts'][i]['red_time']]])
                plan_phase_info[i + 1] = plan['parts'][i]['phase_nums']
            data = {
                'action': 'get_plan',
                'plan_phase_info': plan_phase_info,  # 方案通行相位信息
                'plan_info': plan_info,  # 红绿灯信息
                'coordinate_plan_id': msg['data']['coordinate_plan_info']['id']
            }
            return ret, data
        except Exception as e:
            ret = {'error': True, 'msg': '失败'}
            loger.error('get plan coordinate tactics error {}'.format(e), 'tactics')
            return ret, None

    @staticmethod
    def plan_read_command(msg):
        """获取方案信息指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        try:
            with SharedMemory.app.app_context():
                plan_info = PlanDas.get_plan_part_by_id(msg['plan_id'])
                if plan_info:
                    data.update({'code': 200, 'msg': '成功', 'data': plan_info})
                else:
                    data.update({'code': 4002, 'msg': '方案不存在'})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def plan_list_command(msg):
        """获取方案列表指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        try:
            with SharedMemory.app.app_context():

                plans = PlanDas.get_plan_part_list()

                if not SharedMemory.road_info:
                    SharedMemory.road_info = RoadDas.get_road_info()

                related_plans = TacticsDas.get_tactics_related_plans()
                for index, plan in enumerate(plans):
                    # 固定方案控制模式
                    if SharedMemory.road_info:
                        plans[index]['status'] = 1 if 'plan_num' in SharedMemory.road_info['control_detail'].keys(
                        ) and SharedMemory.road_info['control_detail']['plan_num'] == plan['number'] else 0
                    plans[index]['relate_status'] = 1 if plan['id'] in related_plans else 0

                data.update({'code': 200, 'msg': '成功', 'data': plans})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def led_conn_command(msg):
        """获取led列表指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        try:
            with SharedMemory.app.app_context():
                data.update({'code': 200, 'msg': '成功', 'data': EquipmentDas.get_leds_list()})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def led_plan_info_command(msg):
        """获取led方案信息指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        try:
            with SharedMemory.app.app_context():
                led_plan_info = EquipmentDas.get_led_plan_by_id(msg['led_plan_id'])
                if led_plan_info:
                    data.update({'code': 200, 'msg': '成功', 'data': led_plan_info})
                else:
                    data.update({'code': 4002, 'msg': '方案不存在'})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def tactics_list_command(msg):
        """获取策略列表指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        try:
            with SharedMemory.app.app_context():
                data.update({'code': 200, 'msg': '成功', 'data': TacticsDas.get_tactics_list() or []})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def get_phase_info_command(msg):
        """获取相位信息列表指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        try:
            with SharedMemory.app.app_context():
                phases = PlanDas.get_phases_list()

                conflict_phases = {}
                if len(phases.keys()) > 0:
                    conflict_phases = PlanDas.get_conflict_phases_list(phases.keys())
                phase_list = []
                for phase in phases.values():
                    phase['conflict_phases'] = []
                    for conflict_phase in conflict_phases.get(phase['id'], []):
                        conflict_phase_info = phases.get(conflict_phase, None)
                        if conflict_phase_info:
                            phase['conflict_phases'].append({
                                'id': conflict_phase,
                                'name': conflict_phase_info['name'],
                                'number': conflict_phase_info['number']
                            })
                    phase_list.append(phase)
                data.update({'code': 200, 'msg': '成功', 'data': phase_list})
        except Exception as e:
            data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def plan_new_command(msg):
        """新增方案指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        if 'data' not in msg.keys() or not isinstance(msg['data'], dict):
            data.update({'code': 4005, 'msg': '参数错误'})
        else:
            try:
                ret = PlanDeal.add_plan(msg['data'])
                data.update(ret)
            except Exception as e:
                data.update({'code': 4001, 'msg': '服务异常 {}'.format(e)})

        return data

    @staticmethod
    def plan_edit_command(msg):
        """编辑方案指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        if 'data' not in msg.keys() or not isinstance(msg['data'], dict):
            data.update({'code': 4005, 'msg': '参数错误'})
        else:
            try:
                ret = PlanDeal.edit_plan(msg['data'])
                data.update(ret)
            except Exception as e:
                data.update({'code': 4001, 'msg': '服务异常'})

        return data

    @staticmethod
    def plan_del_command(msg):
        """删除方案指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        if 'data' not in msg.keys() or not isinstance(msg['data'], dict):
            data.update({'code': 4005, 'msg': '参数错误'})
        else:
            try:
                ret = PlanDeal.del_plan(msg['data'])
                data.update(ret)
            except Exception as e:
                data.update({'code': 4001, 'msg': '服务异常'})

        return data

    @staticmethod
    def tactics_edit_command(msg):
        """修改策略指令处理
        :param msg: 指令内容
        :return: map
        """
        data = {
            'info_type': msg['info_type'],
            'request_id': msg['request_id'],
        }
        if 'data' not in msg.keys():
            data.update({'code': 4005, 'msg': '参数错误'})
        else:
            try:
                ret = PlanDeal.tactics_edit(msg['data'])
                data.update(ret)
            except Exception as e:
                data.update({'code': 4001, 'msg': '服务异常'})

        return data

    @staticmethod
    def get_camera_info():
        try:
            with SharedMemory.app.app_context():
                cameras = EquipmentDas.get_cameras_list(status=1, return_type='list')

                camera_info = [{
                    'id': camera['id'],
                    'type': camera['type'],
                    'direction': camera['direction'],
                    'number': camera['number'],
                    'camera_url': {**camera['stream']['rtmp'], 'ip': SharedMemory.ip_addr_info[0]},
                    'status': camera['status'],
                } for camera in cameras]
                return camera_info
        except Exception as e:
            return []

    @staticmethod
    def get_camera_status():
        try:
            with SharedMemory.app.app_context():
                camera_id_status = DeviceMonitorThread.status.get('camera', {})
                cameras = EquipmentDas.get_cameras_list(return_type='list')
                camera_status = [{
                    'id': camera['id'],
                    'type': camera['type'],
                    'direction': camera['direction'],
                    'number': camera['number'],
                    'status': camera_id_status.get(camera['id'], 0),
                } for camera in cameras]
                return camera_status
        except Exception as e:
            return []

    @staticmethod
    def get_radar_info():
        try:
            with SharedMemory.app.app_context():
                radars = EquipmentDas.get_radars_list(status=1)
                radar_info = [{
                    'id': radar['id'],
                    'type': radar['type'],
                    'direction': radar['direction'],
                    'number': radar['number'],
                    'status': radar['status'],
                } for radar in radars]
                return radar_info
        except Exception as e:
            return []

    @staticmethod
    def get_radar_status():
        try:
            with SharedMemory.app.app_context():
                radar_id_status = DeviceMonitorThread.status.get('radar', {})
                radars = EquipmentDas.get_radars_list()
                radar_status = [{
                    'id': radar['id'],
                    'type': radar['type'],
                    'direction': radar['direction'],
                    'number': radar['number'],
                    'status': radar_id_status.get(radar['id'], 0),
                } for radar in radars]
                return radar_status
        except Exception as e:
            return []

    @staticmethod
    def get_road_info_bubble_content(control_model):
        try:
            with SharedMemory.app.app_context():
                plan_info = SharedMemory.current_plan_info
                road_info = SharedMemory.road_info
                bubble = ''
                for part in plan_info['parts']:
                    bubble += '{}阶段绿灯时间{}秒,'.format(part['number'], part['green_time'])
                bubble = bubble.rstrip(',')
                content = {
                    'type': '添加路口',
                    'cross_num': road_info['number'],
                    'control_info': {
                        'control_model': control_model,
                        'control_type': road_info['control_type'],
                        'current_plan': plan_info,
                    },
                }
                if road_info['control_type'] == 2:
                    content['control_info']['tactics_id'] = road_info.get('control_detail', {}).get('tactics_id', None)
                    content['control_info']['tactics_model'] = road_info.get('control_detail', {}).get('model', None)

                return bubble, content
        except Exception as e:
            return '', {}


# receive message topic templates

RECEIVE_MESSAGE_TOPICS = {
    '/sys/${ProductKey}/${DeviceKey}/thing/service/set': CommandConduct.receive_command_handler,
    '/sys/${ProductKey}/${DeviceKey}/SetUp': CommandConduct.get_update_info_handler,
    '/sys/${ProductKey}/${DeviceKey}/status/report': CommandConduct.get_road_status_handler,
}

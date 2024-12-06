import asyncio
from typing import Dict, List
import httpx
from datetime import datetime, timedelta
import json
from nonebot import on_command,logger
from nonebot.permission import SUPERUSER
from .util import UniMessage, get_template, template_to_pic,get_activities,scheduler
from nonebot_plugin_alconna import on_alconna,Target,Match
from nonebot_plugin_alconna.uniseg import MsgTarget
from arclet.alconna import Alconna, Option,Args
from aiofiles import open as aio_open
from .config import group_data
lock = asyncio.Lock()






 
url = 'https://api.kurobbs.com/wiki/core/homepage/getPage'

data = {

}


headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://wiki.kurobbs.com/',
    'Upgrade-Insecure-Requests' : '1',
    'Sec-Ch-Ua-Platform' : '"Windows"',
    'Sec-Ch-Ua' : '"Microsoft Edge";v="125", "Chromium";v="125", "Not=A?Brand";v="24"',
    'Sec-Ch-Ua-Mobile' : '?0',
    'Wiki_type' : '9'

}



if group_data.exists():
    with open(group_data, "r", encoding="utf8") as f:
        CONFIG: Dict[str, List] = json.load(f)
else:
    CONFIG: Dict[str, List] = {"opened_groups": []}
    with open(group_data, "w", encoding="utf8") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=4)


#��������
async def get_data():
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, data=data, headers=headers)

    dw = resp.json()

    activities_dict = {}

    rw_dict = {}
    rwtime = dw['data']['contentJson']['sideModules'][0]['content']['tabs'][0]['countDown']['dateRange']
    rw_dict['dateRange'] = rwtime


    role_dict = {}

    ra_name = dw['data']['contentJson']['sideModules'][0]['content']['tabs'][0]['description']

    roleimglist = []
    for i in range(0,4):
        roleimgs = dw['data']['contentJson']['sideModules'][0]['content']['tabs'][0]['imgs'][i]['img']
        roleimglist.append(roleimgs)

    role_dict["contentUrl"] = roleimglist
    role_dict["title"] = ra_name



    weapon_dict = {}

    wa_name = dw['data']['contentJson']['sideModules'][1]['content']['tabs'][0]['description']

    weaponimglist = []
    for i in range(0,4):
        weaponimgs = dw['data']['contentJson']['sideModules'][1]['content']['tabs'][0]['imgs'][i]['img']
        weaponimglist.append(weaponimgs)

    weapon_dict["contentUrl"] = weaponimglist
    weapon_dict["title"] = wa_name


    ac_list = []
    ac_list.append(role_dict)
    ac_list.append(weapon_dict)


    rw_dict['activities'] = ac_list


    activities = dw['data']['contentJson']['sideModules'][2]['content']

    activities_with_countdown = [activity for activity in activities if 'countDown' in activity]




    result = []

    result.append(rw_dict)
    seen_date_ranges = set()

    for activity in activities_with_countdown:
        date_range_str = activity.get("countDown", {}).get("dateRange")
        if date_range_str:
            # ֱ��ʹ���ַ�����ʽ�����ڷ�Χ��Ϊ��
            key = tuple(date_range_str)
        else:
            key = None

        if key not in seen_date_ranges:
            seen_date_ranges.add(key)
            result.append({"dateRange": key, "activities": []})

        index = next(i for i, item in enumerate(result) if item["dateRange"] == key)
        result[index]["activities"].append({
            "contentUrl": activity["contentUrl"],
            "title": activity["title"]
        })




    activities_dict['ac'] = result
    return activities_dict




def is_current_time_in_range(time_list):
    # ��������ʱ���ʽ
    date_format = "%Y-%m-%d %H:%M"

    start_str = time_list[0]
    # end_str = time_list[1] + timedelta(days=1)

    end_datetime = datetime.strptime(time_list[1], date_format) + timedelta(days=1)

# �����ת�����ַ���
    end_str = end_datetime.strftime(date_format)
    
    # ���ַ���ת��Ϊdatetime����
    start_time = datetime.strptime(start_str, date_format).date()
    end_time = datetime.strptime(end_str, date_format).date()
    
    # ��ȡ��ǰʱ��
    current_time = datetime.now().date()
    
    # �жϵ�ǰʱ���Ƿ��ڷ�Χ��
    if start_time <= current_time <= end_time:
        return True
    else:
        return False
    

# 2�ж��Ƿ���ڷ��������Ļ
def check_activities(data):
    is_start_previous_day = False
    is_end_previous_day = False

    current_date = datetime.now().date()

    for item in data:
        start_date_str, end_date_str = item["dateRange"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M").date()

        # �жϿ�ʼǰһ��
        if start_date - timedelta(days=1) == current_date:
            is_start_previous_day = True

        # �жϽ���ǰһ��
        if end_date - timedelta(days=1) == current_date:
            is_end_previous_day = True

    # ����ǿ�ʼǰһ������ǰһ���򷵻�True�����򷵻�False
    return is_start_previous_day or is_end_previous_day


#3������������Ļ
def get_activities_before_and_after_today(data):

    ac_dict = {}


    # ��ǰʱ��
    current_date = datetime.now().date()  

    # �����б�
    start_previous_day = []
    end_previous_day = []

    # ��������
    for item in data:
        start_date_str, end_date_str = item["dateRange"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M").date()

        # �жϿ�ʼǰһ��
        if start_date - timedelta(days=1) == current_date:
            start_previous_day.extend(item["activities"])

        # �жϽ���ǰһ��
        if end_date - timedelta(days=1) == current_date:
            end_previous_day.extend(item["activities"])

    # ������
    before = []
    for activity in start_previous_day:
        before.append(activity)

    ac_dict["before"] = before

    after = []
    for activity in end_previous_day:
        after.append(activity)

    ac_dict["after"] = after

    return ac_dict


# ����һ������������ʱ���
def calculate_time_difference(end_time):
    if end_time < current_time:
        return "�ѽ���"
    
    delta = end_time - current_time
    
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60
    
    return f"ʣ�ࣺ{days}�� {hours}Сʱ {minutes}����"

def compare_time_ranges(time_ranges):
    # ��ȡ��ǰʱ��
    current_time = datetime.now()
    current_time_date = current_time.date()
    
    # ���������ʱ�䷶Χ
    start_time = datetime.strptime(time_ranges[0], "%Y-%m-%d %H:%M")
    start_time_date = start_time.date()
    end_time = datetime.strptime(time_ranges[1], "%Y-%m-%d %H:%M")
    end_time_date = end_time.date()

    # �Ƚϲ�������
    if current_time_date < start_time_date:
        return "δ��ʼ"
    elif current_time_date > end_time_date:
        return "�ѽ���"
    else:
        # ���������ʱ��Ĳ�
        delta = end_time - current_time
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        
        return f"{days}�� {hours}Сʱ {minutes}����"


#����
def role_data(data):
    role = data['ac'][0]['activities'][0]
    weapon = data['ac'][0]['activities'][1]
    time = data['ac'][0]['dateRange']
    # end_time = datetime.strptime(time[1], "%Y-%m-%d %H:%M")

    Data = {
        "time1" : time[0],
        "time2" : time[1],
        "timeperiod" : compare_time_ranges(time),
        "rolename" : role['title'],
        "fivestarsimg" : role['contentUrl'][0],
        "fourstarsimg1" : role['contentUrl'][1],
        "fourstarsimg2" : role['contentUrl'][2],
        "fourstarsimg3" : role['contentUrl'][3],
        "weaponname" : weapon['title'],
        "fiveswi" : weapon['contentUrl'][0],
        "fourswi1" : weapon['contentUrl'][1],
        "fourswi2" : weapon['contentUrl'][2],
        "fourswi3" : weapon['contentUrl'][3]
    }


    return Data



current_time = datetime.now()

# �������ڸ�ʽ
date_format = "%Y-%m-%d %H:%M"

# ����HTMLģ��
template = '''
<div class="ot">
    <div class="img">
        <img src="{img}" class="aimg">
    </div>
    <div class="atitle">
        <h1 class="at">{title}</h1>
        <h1 class="time">{start_time} - {end_time}</h1>
        <h1 class="tp">{time_diff}</h1>
    </div>
</div>
'''




#��б�
def ac(data):
    html_content = ""
    for item in data[1:]:  # �ӵڶ����ֵ俪ʼ
        date_range = item["dateRange"]
        activities = item["activities"]
        
        # ת�������ַ���Ϊdatetime����
        start_time, end_time = [datetime.strptime(date, date_format) for date in date_range]
        
        
        # ����ʱ���
        time_diff = compare_time_ranges(date_range)
        
        for activity in activities:
            if isinstance(activity["contentUrl"], list):
                img_url = activity["contentUrl"][0]  # ʹ�õ�һ��ͼƬURL
            else:
                img_url = activity["contentUrl"]
            title = activity["title"]
            
            html_content += template.format(img=img_url, title=title, start_time=start_time, end_time=end_time, time_diff=time_diff)


    return html_content


def get_end(data):
    before_template = """
    <div class="t">
    <div class="ot">
    <div class="img">
        <img src="{img}" class="aimg"> </div>
    <div class="atitle">
        <h1 class="at">{title}</h1></div></div></div>
    """
    before_htmls = """
    <div class="oo">
        <h1 class="title">���»�������쿪ʼ</h1></div>
    """
    for item in data['before']:
        if isinstance(item["contentUrl"], list):
            img_url = item["contentUrl"][0]  # ʹ�õ�һ��ͼƬURL
        else:
            img_url = item["contentUrl"]
        before_htmls += before_template.format(img=img_url, title=item['title'])
        
    # output_dict['before'] = before_htmls

    # Process 'after'
    after_template = """
    <div class="t">
    <div class="ot">
    <div class="img">
        <img src="{img}" class="aimg"> </div>
    <div class="atitle">
        <h1 class="at">{title}</h1></div></div></div>
    """
    after_htmls = """
    <div class="oo">
        <h1 class="title">���»�����������</h1></div>
    """
    

    for item in data['after']:
        if isinstance(item["contentUrl"], list):
            img_url = item["contentUrl"][0]  # ʹ�õ�һ��ͼƬURL
        else:
            img_url = item["contentUrl"]
        after_htmls += after_template.format(img=img_url, title=item['title'])

        

    return after_htmls + before_htmls

card_pools = on_command('��������')

card_pool_spath = get_template("card_pool")
activity_spath = get_template("activity")
data_spath = get_activities()




@card_pools.handle()
async def cardpools():
    old_data = await get_data()

    Data = role_data(old_data)


    img = await template_to_pic(
        card_pool_spath.parent.as_posix(),
        card_pool_spath.name,
        Data,
        
    )

    await UniMessage.image(raw=img).finish()



activities = on_command('������б�')


@activities.handle()
async def activity():
    old_data = await get_data()


    Data = {
        "div" : ac(old_data['ac'])
    }


    img = await template_to_pic(
        activity_spath.parent.as_posix(),
        activity_spath.name,
        Data,
        
    )


    await UniMessage.image(raw=img).finish()


timing_activity = get_template("timing")


@scheduler.scheduled_job('cron',hour='18',jitter=600)
async def scheduled_tasks():
        old_data = await get_data()


        if check_activities(old_data['ac']) is True:
            ac_dict_data = get_activities_before_and_after_today(old_data['ac'])
            ac_dica = get_end(ac_dict_data)

            Data = {
                "div" : ac_dica
            }

            img = await template_to_pic(
                timing_activity.parent.as_posix(),
                timing_activity.name,
                Data,
                
            )

            for group_id in CONFIG['opened_groups']:

                target = Target(group_id)
                logger.info(f'�ɹ����ͻ')
                await UniMessage.image(raw=img,).send(target=target)


        else:
            return



alc = Alconna("���������", Args["group_id?", int], Option("-o|--����"), Option("-c|--�ر�"))

reminder = on_alconna(alc,permission=SUPERUSER)
@reminder.assign("����")
async def open(target: MsgTarget):
    if not target.private:
        groupid = target.id
        if groupid in CONFIG["opened_groups"]:
            await reminder.finish("��Ⱥ�ѿ��������")
        else:
            CONFIG["opened_groups"].append(groupid)
    async with lock:
        async with aio_open(group_data, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(CONFIG, ensure_ascii=False, indent=4))
    await reminder.finish("�����ɹ�")


@reminder.assign("�ر�")
async def close(target: MsgTarget): 
    if not target.private:
        groupid = target.id
        if groupid in CONFIG["opened_groups"]:
            CONFIG["opened_groups"].remove(groupid)
            async with lock:
                async with aio_open(group_data, 'w', encoding='utf-8') as f:
                        await f.write(json.dumps(CONFIG, ensure_ascii=False, indent=4))
            await reminder.finish("�رճɹ�")
        else:
            await reminder.finish("��Ⱥδ���������")
    
    

        
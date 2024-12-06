from requests import post
import time
import signal, sys
from concurrent.futures import ThreadPoolExecutor
from itertools import batched
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from pycas import __version__
import pycas.config
from pycas.logger import log

# 参考 README.md "获取 cookie 和 access_token"
# access_token 需要替换
access_token = ""
page = 1
size = 100


def signal_handler(sig, frame):
    print("\nProgram interrupted by user. Exiting...")
    sys.exit(0)


def get_headers():
    global access_token
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "2",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "www.casmooc.cn",
        "Origin": "https://www.casmooc.cn",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "x-access-browser-info": "chrome 130.0.0.0",
        "x-access-device-mac": "",
        "x-access-device-name": "",
        "x-access-device-system": "Win10",
        "x-access-device-type": "WEB",
        "x-access-location-info": "",
        "x-access-origin": "aHR0cHM6Ly93d3cuY2FzbW9vYy5jbg==",
        "x-access-token": access_token,
    }


progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeRemainingColumn(),
)


def getMyList():
    url = "https://www.casmooc.cn/server/api/course/myList"
    data = '{"formData":{"courseName":"","isCompleted":0,"year":"2023"},"pageData":{"currentPage":1,"pageSize":5,"sortName":"","sortOrder":""}}'
    r = post(url, headers=get_headers(), data=data)
    d = r.json()
    if d and d["code"] and d["code"] == "0":
        print(
            "\n".join(
                [
                    v["courseId"] + "_" + v["courseName"]
                    for v in r.json()["data"]["list"]
                ]
            )
        )


def option(id):
    url = "https://www.casmooc.cn/server/api/course/option"
    data = '{"id":"%s"}' % id
    r = post(url, headers=get_headers(), data=data).json()
    if r["code"] and r["code"] == "0":
        log.info("option successfully")
        return False
    else:
        log.info(r)
        return False


def detail(id):
    url = "https://www.casmooc.cn/server/api/course/detail"
    data = '{"id":"%s","firstCourseId":""}' % id
    return post(url, headers=get_headers(), data=data).json()["data"]


# get lock
def lock(id):
    url = "https://www.casmooc.cn/server/api/study/submitLock"
    # 1700546763393
    ts = int(time.time() * 1000)
    data = (
        '{"belongCourseId":"","courseId":"%s","source":"courseVideoComponent","lockIndex":%d,"is1Lock":1}'
        % (id, ts)
    )
    r = post(url, headers=get_headers(), data=data).json()
    if r["code"] and r["code"] == "0":
        return r["data"]
    log.error("lock failed")
    return ""


def submit(id, lockId, llt):
    url = "https://www.casmooc.cn/server/api/study/submit"
    data = (
        '{"belongCourseId":"","courseId":"%s","isRecordAudio":0,"lastLearnTime": %d,"recordDuration":"10","studyLockUUID":"%s"}'
        % (id, llt, lockId)
    )
    r = post(url, headers=get_headers(), data=data).json()
    # print(r['data'])


def learn(task_id, id):
    # option
    if option(id):
        return
    lockId = lock(id)
    if not lockId:
        return
    d = detail(id)
    duration = int(d["classHour"] * 3600)
    llt = int(d["lastLearnTime"])
    if abs(duration - llt) < 20:
        progress.update(task_id, completed=duration, visible=False)
        return
    progress.console.log(f"开始学习: {d["courseName"]} [{llt}/{duration}]")
    # print("%d: %s %d/%d" % (no, d["courseName"], llt, duration))
    step = 10  # 10s / request
    progress.update(task_id, total=duration, completed=llt)
    progress.start_task(task_id)
    # bar = progressbar.ProgressBar(min_value=llt, max_value=duration)
    for i in range(llt, duration, step):
        submit(id, lockId, i)
        time.sleep(0.1)
        # bar.update(i)
        progress.update(task_id, advance=step)
    progress.update(task_id, visible=False)


def clist(page, size):
    url = "https://www.casmooc.cn/server/api/course/list"
    req = (
        '{"formData":{"classfication":0,"courseName":"","createDateRange":[],"customTypeId":0,"expertAreaId":302,"orderByType":1,"orgSource":"","searchKey":"","teacherId":"","orgId":0},"pageData":{"currentPage":%d,"pageSize":%d,"sortName":"","sortOrder":""}}'
        % (page, size)
    )
    res = post(url, headers=get_headers(), data=req).json()
    list = res["data"]["list"]
    data = [(v["courseId"], v["courseName"]) for v in list]
    return data


def main():
    signal.signal(signal.SIGINT, signal_handler)  # Register the signal handler
    try:
        print(f"pycas \033[32mv{__version__}\033[0m")
        args = pycas.config.parse_cli()
        if args.log_level:
            log.setLevel(args.log_level)

        if args.version:
            return
        global cookie
        cookie = args.cookie
        global access_token
        access_token = args.token
        global page
        page = args.page
        global size
        size = args.size
        log.debug(f"access_token: {access_token}")
        if not access_token:
            log.error("cookie or access_token is required")
            return

        with progress:
            futures = []
            with ThreadPoolExecutor(max_workers=1) as pool:
                for g in batched(clist(page, size), 1):
                    for id, name in g:
                        task_id = progress.add_task(
                            "automatic-task",
                            start=False,
                            filename=name[: min(20, len(name))],
                        )
                        fu = pool.submit(learn, task_id, id)
                        futures.append(fu)

                pool.shutdown(wait=True)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()

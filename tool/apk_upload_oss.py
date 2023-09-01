import os
import time

client_dir = r"C:\Users\libm\WebstormProjects\client\unpackage\release\apk"
store_dir = r"C:\Users\libm\WebstormProjects\store\unpackage\release\apk"
rider_dir = r"C:\Users\libm\WebstormProjects\rider\unpackage\release\apk"

ls = [client_dir, store_dir, rider_dir]
# ls = [rider_dir]

pkg_client = "__UNI__C94C897"
pkg_store = "__UNI__EC851A8"
pkg_rider = "__UNI__ECB29E7"

oss_url = f"https://jiushuixiangfeng.oss-cn-beijing.aliyuncs.com/{pkg_rider}"


def fmt_apk(raw_apk: str):
    # 文件路径提取文件名
    raw_apk = os.path.basename(raw_apk)
    now = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    if raw_apk.startswith(pkg_client):
        return fr"client_{now}.apk"
    if raw_apk.startswith(pkg_store):
        return fr"store_{now}.apk"
    if raw_apk.startswith(pkg_rider):
        return fr"rider_{now}.apk"
    return raw_apk


def get_latest_apk(path):
    global files
    try:
        files = os.listdir(path)
    except Exception as e:
        return
    if files == []:
        print(f"目录下无文件：{path}")
        return
    files.sort(key=lambda i: os.path.getmtime(f"{path}/{i}"))
    return os.path.join(path, files[-1])


def upload_oss(path):
    cmd = fr"ossutil64 cp -f {path} oss://jiushuixiangfeng/{fmt_apk(path)}"
    print(cmd)
    result = os.system(cmd)
    if result == 0:
        dir_name = os.path.dirname(path)
        try:
            os.rename(path, fr"{os.path.join(dir_name, fmt_apk(path))}")
        except Exception as e:
            print(e)
    return result


def print_qrcode(url_ls: list):
    url = url_ls[0]
    client_url = f"https://cli.im/api/qrcode/code?text=https://jiushuixiangfeng.oss-cn-beijing.aliyuncs.com/{url}&mhid=4EXCCQzmzs8hMHYoI9dWOqs"
    url = url_ls[1]
    store_url = f"https://cli.im/api/qrcode/code?text=https://jiushuixiangfeng.oss-cn-beijing.aliyuncs.com/{url}&mhid=4EbAX13qk80hMHYoI9dWOaM"
    url = url_ls[2]
    rider_url = f"https://cli.im/api/qrcode/code?text=https://jiushuixiangfeng.oss-cn-beijing.aliyuncs.com/{url}&mhid=sEfADF6/mZ8hMHYoI9dWOqo"

    print(fr"客户端二维码：{client_url}")
    print(fr"商家端二维码：{store_url}")
    print(fr"骑手端二维码：{rider_url}")


# print_qrcode([666,777,999])

if __name__ == '__main__':
    fail_msg = ""
    fmt_ls = []
    for i in ls:
        latest_path = get_latest_apk(i)
        fmt = fmt_apk(latest_path)
        apk = fmt.split("_")[0]
        print(f"上传中: {apk}\n")
        flag = upload_oss(latest_path)
        if flag == 1:
            print(f"\n{i}上传失败: {apk}\n")
            fail_msg += f"上传oss失败：{apk}\n"
        else:
            print(f"{apk}上传成功")
            fmt_ls.append(fmt)
    if fail_msg == "":
        print("全部上传成功")
        print_qrcode(fmt_ls)
    else:
        print(fail_msg)

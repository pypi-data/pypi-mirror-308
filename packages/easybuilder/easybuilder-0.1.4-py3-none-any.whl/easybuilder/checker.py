import os


def check_clean():
    # 检查git仓库是否有未提交的更改
    result = os.system("git status --porcelain")
    if result != 0:
        print("错误: 无法获取git状态")
        exit(1)
    if result:
        print("错误: git仓库不干净,请先提交所有更改")
        exit(1)
    print("git仓库状态检查通过")

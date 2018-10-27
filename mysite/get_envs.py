import os
def if_online_env():
    username = os.path.abspath(__file__).split("/")[2]
    if username=="webapp":
        if_online = True
    else:
        if_online = False
    return if_online


if __name__ =="__main__":
    if_online = if_online_env()
    print(if_online)


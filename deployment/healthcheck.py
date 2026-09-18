import os
import socket

def check_redis():
    url=os.environ.get("REDIS_URL","")
    if not url:
        return {"status":"not_configured"}
    host=url.split("://",1)[-1].split("@")[-1].split(":")[0].split("/")[0]
    port=int(url.rsplit(":",1)[-1].split("/")[0]) if ":" in url else 6379
    sock=socket.create_connection((host,port),timeout=2)
    sock.close()
    return {"status":"ok","host":host,"port":port}

if __name__=="__main__":
    print(check_redis())

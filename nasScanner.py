
import subprocess
import platform


def nasScanner(user:str,path:str,folder:str):
    path = path.replace('*','')
    #cmd = "echo 'ls "+path+"' | sftp "+user
    cmd = "echo 'ls "+'"'+path+folder+'"'+"' | sftp "+user
    fileList = []
    print(cmd)
    try:
        
        if(platform.system()=='Windows'):
            p =runWindows(cmd)
        else:
            p =runUnix(cmd)
        
        out = p.communicate()
        if not p.poll() or out[1]:
            results = out[0]+out[1]
            results = results.splitlines()
        print(results)
        for r in results:
            if path in r and not 'sftp' in r:
                s = r.replace(path+folder+"/",'')
                
                fileList.append(s.strip())
          
        
    except:
        print('Path Error')
    return fileList
    
def runUnix(cmd):
    return subprocess.Popen([cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True,shell=True)

def runWindows(cmd):
    return subprocess.Popen(['powershell',cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True, shell=True)
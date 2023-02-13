
import subprocess
import platform


def nasScanner(user:str,path:str,folder:str):
    path = path.replace('*','')
    #cmd = "echo 'ls "+path+"' | sftp "+user
    cmd = "echo 'ls "+'"'+path+folder+'"'+"' | sftp "+user
    fileList = []

    try:
        print(cmd)
        if(platform.system()=='Windows'):
            p =runWindows(cmd)
        else:
            p =runUnix(cmd)
        
        out = p.communicate()
        if not p.poll() or out[1]:
            results = out[0]+out[1]
            print(repr(results))
            if(not results or results.find('sftp [-46AaCfNpqrv]')>-1):
                results = 'Command Error' 
            if(results.find('debug1: Exit status 0')>-1 or results.find('Executing: cp --')>-1):
                results = 'Failed Transfer'
            if(results.find('scp: ambiguous target')>-1):
                results = 'SCP Ambiguous Target'
            if(results.find('No space left on device')>-1):
                results = 'Target Disk Full'
    
            results = results.splitlines()
            
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
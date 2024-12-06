try:
    from .common import *
except Exception as e:
    if 'unable to open database file' in str(e):
        print('该命令仅支持运行kcwebplus项目')
        exit()
    else:
        print('e',e)
from kcweb import kcweb
def cill_start(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr='kcwebplus'):
        "脚本入口"
        cmd_par=kcweb.kcw.get_cmd_par()
        cmd_par['project']='kcwebplus'
        if cmd_par and cmd_par['server']:#启动web服务
            #执行kcwebplus自启项
            try:
                Queues.delwhere("code in (2,3)")
            except:pass
            startdata=sqlite().connect(model_app_path).where("types='kcwebplus'").table("start").order("id asc").select()
            for teml in startdata:
                os.system(teml['value'])
            if get_sysinfo()['uname'][0]=='Linux':
                system_start.insert_Boot_up(cmd='cd /kcwebplus && bash server.sh',name='kcwebplus自启',icon='https://img.kwebapp.cn/icon/kcweb.png')
                os.system('nohup kcwebplus index/index/pub/clistartplan --cli > app/runtime/log/server.log 2>&1 &')
        if cmd_par:
            t=kcweb.cill_start(fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr=fdgrsgrsegsrsgrsbsdbftbrsbfdrtrtbdfsrsgr)
            if cmd_par['install']:#插入 应用、模块、插件
                if cmd_par['appname'] and cmd_par['modular']:
                    if not cmd_par['plug']:
                        if t[0]:
                            if os.path.exists(cmd_par['project']):
                                remppath=os.path.split(os.path.realpath(__file__))[0]
                                if get_sysinfo()['uname'][0]=='Linux':
                                    # if not os.path.isfile("./"+cmd_par['project']+"/server"):
                                    #     shutil.copy(remppath+'/server',cmd_par['project'])
                                    if not os.path.isfile("./"+cmd_par['project']+"/tempfile/server.sh"):
                                        shutil.copy(remppath+'/tempfile/server.sh',cmd_par['project'])
                                elif get_sysinfo()['uname'][0]=='Windows':
                                    if not os.path.isfile("./"+cmd_par['project']+"/tempfile/server.bat"):
                                        shutil.copy(remppath+'/tempfile/server.bat',cmd_par['project'])
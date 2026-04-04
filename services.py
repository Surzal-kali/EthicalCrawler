import psutil
from theatrics import clear, dev_comment, speak, test


def prog(store, session_id, me, user_name, consent_form=None, autosave=None):
    """Enumerate running services. Scans currently running processes against a list of common applications and registers new ones with the session store. takes store, session_id, me, user_name, optional consent_form, and optional autosave manager as parameters. Returns a list of newly detected services."""
    common_services = [
        "steam", "spotify", "discord", "slack", "teams", "zoom", "skype", "dropbox", "google drive", "onedrive",
        "chrome", "firefox", "edge", "opera", "brave", "vivaldi", "thunderbird", "outlook", "evolution",
        "calibre", "vlc", "itunes", "gimp", "photoshop", "illustrator", "blender", "autocad", "visual studio",
        "code", "notepad++", "pycharm", "firefox", "postman", "vmware", "wireshark", "virtualbox", "vmware", "hyper-v", "docker", "kubernetes", "ansible", "terraform", "jenkins", "git", "github desktop", "bitbucket", "gitlab", "aws cli", "azure cli", "gcloud sdk", "tailscale", "ollama", "lm studio", "obs",  "xbox", "epic", "gog", "origin", "uplay", "battle.net", "riot client", "blizzard app", "nvidia geforce experience", "amd radeon software", "intel graphics command center"
    ]
    running_process_names = set()
    for proc in psutil.process_iter(['name']):
        try:
            proc_name = (proc.info.get('name') or '').lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        if proc_name:
            running_process_names.add(proc_name)

    services_list = []
    for service in common_services:
        service_name = service.lower()
        if any(service_name in proc_name for proc_name in running_process_names):
            if store.add_service(service):  # True if not already seen this session
                services_list.append(service)

    return services_list

# NOTE: matching is substring-based against a known list — not exhaustive.
# Some processes run under different names; false positives possible.
# Refinement planned for Act II alongside out_of_scope enforcement.

#example
# running_process_names = {'audiodg.exe', 'conhost.exe', 'systemsettingsadminflows.exe', 'hwinfo64.exe', 'lsass.exe', 'svchost.exe', 'onedrive.sync.service.exe', 'intelcphdcpsvc.exe', 'sshd.exe', 'services.exe', 'spoolsv.exe', 'discord.exe', 'powertoys.powerlauncher.exe', 'fontdrvhost.exe', 'crossdeviceservice.exe', 'sunshine.exe', 'memcompression', 'tailscaled.exe', 'microsoft.cmdpal.ui.exe', 'spotify.exe', 'ctfmon.exe', 'dllhost.exe', 'nissrv.exe', 'microsoftedgeupdate.exe', 'icue.exe', 'steamservice.exe', 'searchindexer.exe', 'powertoys.awake.exe', 'phoneexperiencehost.exe', 'powertoys.peek.ui.exe', 'wmiprvse.exe', 'textinputhost.exe', 'backgroundtaskhost.exe', 'wslservice.exe', 'shellhost.exe', 'crossdeviceresume.exe', 'db browser for sqlite.exe', 'agent_ovpnconnect.exe', 'ovpnhelper_service.exe', 'mpdefendercoreservice.exe', 'presentmonservice.exe', 'wlanext.exe', 'ngciso.exe', 'taskhostw.exe', 'discordsystemhelper.exe', 'widgetservice.exe', 'securityhealthsystray.exe', 'node.exe', 'wudfhost.exe', 'microsoft.cmdpal.ext.powertoys.exe', 'wmiapsrv.exe', 'startmenuexperiencehost.exe', 'pet.exe', 'gamingservices.exe', 'powertoys.advancedpaste.exe', 'olkbg.exe', 'steamwebhelper.exe', 'wininit.exe', 'widgets.exe', ...}

#this is amazing!!!!!!!!!!!!!!!!!!! note to self, run in debug often
###ok so so the services keyword calls aren't working for edge, this is my problem with theatrics keyword matching, we need to have a more robust way to match services. maybe we should have a mapping of known process names to service keywords? #i wanna take a break from quips and do web crawling #yeth

#ok whats a good endpoint? #for the crawl silly #
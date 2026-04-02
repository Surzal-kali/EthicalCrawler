import psutil
from theatrics import pprint, clear, dev_comment, test


def prog(conn, cursor, session_id, me, user_name, autosave=None):
    pprint(me, message="..............................................")
    pprint(me, message=" ⚙️   SERVICES DETECTED")  
    pprint(me, message="..............................................")     
    cursor.execute("SELECT DISTINCT name FROM services WHERE session_id = ?", (session_id,))
    services_list = [row[0] for row in cursor.fetchall()]
    if not services_list:
        common_services = [
            "steam", "spotify", "discord", "slack", "teams", "zoom", "skype", "dropbox", "google drive", "onedrive",
            "chrome", "firefox", "edge", "opera", "brave", "vivaldi", "tor", "thunderbird", "outlook", "evolution",
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

        detected_services = []
        for service in common_services:
            service_name = service.lower()
            if any(service_name in proc_name for proc_name in running_process_names):
                detected_services.append(service)

        if detected_services:
            for service in detected_services:
                cursor.execute(
                    "INSERT OR IGNORE INTO services (session_id, name) VALUES (?, ?)",
                    (session_id, service),
                )
            conn.commit()
            cursor.execute("SELECT DISTINCT name FROM services WHERE session_id = ?", (session_id,))
            services_list = [row[0] for row in cursor.fetchall()]

    for service in services_list:
        dev_comment(f"Services enumerator collected: {service}")    
    return services_list

import psutil
from theatrics import pprint, clear, dev_comment, test


def prog(conn, cursor, session_id, me, user_name, autosave=None):
    pprint(me, message="..............................................")
    pprint(me, message=" ⚙️   SERVICES DETECTED") #this logic is pretty basic. We can make it more robust by looking for specific process names and correlating them to services. But for now, this is a start. li understood the file this time. .. progress!
    #shouldn't equip go through value of key? not key? 
    pprint(me, message="..............................................")     
    cursor.execute("SELECT DISTINCT name FROM services WHERE session_id = ?", (session_id,))
    services_list = [row[0] for row in cursor.fetchall()]
    if not services_list:
        common_services = [
            "steam", "spotify", "discord", "slack", "teams", "zoom", "skype", "dropbox", "google drive", "onedrive",
            "chrome", "firefox", "edge", "opera", "brave", "vivaldi", "tor", "thunderbird", "outlook", "evolution",
            "calibre", "vlc", "itunes", "gimp", "photoshop", "illustrator", "blender", "autocad", "visual studio",
            "code", "notepad++", "pycharm",
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
##brainbreaking: we want to be able to detect services that are running, but we also want to be able to detect services that have been used in the past. maybe we can look for artifacts of those services? like config files, logs, etc? this is where the ioc knowledge could come in handy. if we know what to look for, we can find evidence of past usage even if the service isn't currently running. this would be a more comprehensive approach to enumeration. it would give us a better picture of the user's habits and potential attack surface.
        if detected_services:
            for service in detected_services:
                cursor.execute(
                    "INSERT OR IGNORE INTO services (session_id, name) VALUES (?, ?)",
                    (session_id, service),
                )
            conn.commit()
            cursor.execute("SELECT DISTINCT name FROM services WHERE session_id = ?", (session_id,))
            services_list = [row[0] for row in cursor.fetchall()]

    return services_list


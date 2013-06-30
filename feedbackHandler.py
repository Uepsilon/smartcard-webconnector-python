SUCCESS = "Success"
POWER = "Power"
ERROR = "Error"
CONNECTION = "Connection"

ACTIVE = "Active"
INACTIVE = "Inactive"

def setup():
    setFeedback(POWER, ACTIVE)

def setFeedback(channel, status):
    print "Set Channel '" + str(channel) + "' to '" + str(status) + "'"

def shutdown():
    setFeedback(SUCCESS, INACTIVE)
    setFeedback(POWER, INACTIVE)
    setFeedback(ERROR, INACTIVE)
    setFeedback(CONNECTION, INACTIVE)


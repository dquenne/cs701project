import math


# def pitchToNoteName(pitch):


class Note:

    # initialize
    def __init__(self, midi_message):
        data = midi_message.split(", ")
        self.track = int(data[0])
        self.time = int(data[1])
        self.channel = int(data[3])
        self.pitch = int(data[4])
        self.duration = 4 # 4 16th notes
        self.instrument = ""


    def measure(self, num, denom, clocksperbeat):
        clockspermeasure = num*clocksperbeat
        return math.floor(self.time/clockspermeasure)

    def timeInMeasure(self, num, denom, clocksperbeat):
        clockspermeasure = num*clocksperbeat
        return round((self.time % clockspermeasure)/clocksperbeat*4)


    def getTrainingDataNote(self, num, denom, clocksperbeat):
        # output = ("@" + str(self.timeInMeasure(num, denom, clocksperbeat)) + "[" +
        # '(%03d)' % self.pitch
        # + "]"
        return '{inst}@{time:02d}[({pitch:03d}):{duration:02d}]'.format(
            inst=self.instrument,
            time=self.timeInMeasure(num, denom, clocksperbeat),
            pitch=self.pitch,
            duration=self.duration)

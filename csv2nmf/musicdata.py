import math


# def pitchToNoteName(pitch):


class Note:

    # initialize
    def __init__(self, midi_message, ppq):
        data = midi_message.split(", ")
        self.track = int(data[0])
        self.time = int(data[1])
        self.channel = int(data[3])
        self.pitch = int(data[4])
        self.duration = 4 # 4 16th notes
        self.instrument = ""
        # self.num = int(time_signature[3])
        # self.denom = int(time_signature[4])
        self.clocksperbeat = ppq#int(time_signature[5])
        self.clockspermeasure = ppq*4#self.num*self.clocksperbeat


    def measure(self):
        return math.floor(self.time/self.clockspermeasure)

    def timeInMeasure(self):
        return round((self.time % self.clockspermeasure)/self.clocksperbeat*4)


    def getTrainingDataNote(self):
        # output = ("@" + str(self.timeInMeasure(num, denom, clocksperbeat)) + "[" +
        # '(%03d)' % self.pitch
        # + "]"
        return '{inst}@{pitch:03d}'.format(
            inst=self.instrument,
            pitch=self.pitch)
        # return '{inst}@{time:02d}[({pitch:03d}):{duration:02d}]'.format(
        #     inst=self.instrument,
        #     time=self.timeInMeasure(),
        #     pitch=self.pitch,
        #     duration=self.duration)

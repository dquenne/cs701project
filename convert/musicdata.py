import math


# def pitchToNoteName(pitch):

QUARTER_SUBDIVISION = 12

class Note:

    # initialize
    def __init__(self, midi_message, ppq):
        data = midi_message.split(", ")
        self.track = int(data[0])
        self.time = int(data[1])
        self.channel = int(data[3])
        self.pitch = int(data[4])
        self.velocity = int(data[5])
        self.duration = 4 # 4 16th notes
        self.instrument = ""
        # self.num = int(time_signature[3])
        # self.denom = int(time_signature[4])
        self.clocksperbeat = ppq#int(time_signature[5])
        self.clockspermeasure = ppq*4#self.num*self.clocksperbeat

    # def __init__(self, instrument, pitch, duration, measure, submeasure, ppq):
    #     self.track = -1
    #     self.channel = -1
    #     self.time = measure*ppq*4 + submeasure*ppq/QUARTER_SUBDIVISION
    #     self.pitch = pitch
    #     self.duration = duration
    #     self.instrument = instrument
    #     self.clocksperbeat = ppq
    #     self.clockspermeasure = ppq*4

    def getPitch(self):
        return self.pitch

    def measure(self):
        return math.floor(self.time/self.clockspermeasure)

    def timeInMeasure(self):
        return math.floor((self.time % self.clockspermeasure)/self.clocksperbeat*QUARTER_SUBDIVISION)


    def getTrainingDataNote(self, use_velocity, last_pitch = -1):
        if last_pitch >= 0:
            pitch_output = self.pitch - last_pitch
            if pitch_output < 0:
                pitch_output = '~' + '{0:02d}'.format(pitch_output*-1)
            else:
                pitch_output = '+' + '{0:02d}'.format(pitch_output)
        else:
            pitch_output = '{0:03d}'.format(self.pitch)

        if (use_velocity):
            return '{inst}{pitch}!{power}-{duration:02d}'.format(
                inst=self.instrument,
                pitch=pitch_output,
                power=math.floor(self.velocity/15),
                duration=math.ceil(self.duration))
        else:
            return '{inst}{pitch}-{duration:02d}'.format(
                inst=self.instrument,
                pitch=pitch_output,
                duration=math.ceil(self.duration))

    def setEndTime(self, endtime):
        self.duration = (int(endtime) - self.time)/self.clocksperbeat*QUARTER_SUBDIVISION

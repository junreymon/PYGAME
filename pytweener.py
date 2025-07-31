import math

class Tweener:
    def __init__(self, duration=0.5, tween=None):
        self.currentTweens = []
        self.defaultTweenType = tween or Easing.Cubic.easeInOut
        self.defaultDuration = duration or 1.0

    def hasTweens(self):
        return len(self.currentTweens) > 0

    def addTween(self, obj, **kwargs):
        if "tweenTime" in kwargs:
            t_time = kwargs.pop("tweenTime")
        else:
            t_time = self.defaultDuration

        if "tweenType" in kwargs:
            t_type = kwargs.pop("tweenType")
        else:
            t_type = self.defaultTweenType

        if "onCompleteFunction" in kwargs:
            t_completeFunc = kwargs.pop("onCompleteFunction")
        else:
            t_completeFunc = None

        if "onUpdateFunction" in kwargs:
            t_updateFunc = kwargs.pop("onUpdateFunction")
        else:
            t_updateFunc = None

        if "tweenDelay" in kwargs:
            t_delay = kwargs.pop("tweenDelay")
        else:
            t_delay = 0

        tw = Tween(obj, t_time, t_type, t_completeFunc, t_updateFunc, t_delay, **kwargs)
        if tw:
            self.currentTweens.append(tw)
        return tw

    def removeTween(self, tweenObj):
        if tweenObj in self.currentTweens:
            tweenObj.complete = True

    def getTweensAffectingObject(self, obj):
        return [t for t in self.currentTweens if t.target is obj]

    def removeTweeningFrom(self, obj):
        for t in self.currentTweens:
            if t.target is obj:
                t.complete = True

    def finish(self):
        for t in self.currentTweens:
            t.update(t.duration)
        self.currentTweens = []

    def update(self, timeSinceLastFrame):
        removable = []
        for t in self.currentTweens:
            t.update(timeSinceLastFrame)
            if t.complete:
                removable.append(t)
        for t in removable:
            self.currentTweens.remove(t)

class Tween(object):
    def __init__(self, obj, tduration, tweenType, completeFunction, updateFunction, delay, **kwargs):
        self.duration = tduration
        self.delay = delay
        self.target = obj
        self.tween = tweenType
        self.tweenables = kwargs
        self.delta = 0
        self.completeFunction = completeFunction
        self.updateFunction = updateFunction
        self.complete = False
        self.tProps = []
        self.tFuncs = []
        self.paused = self.delay > 0
        self.decodeArguments()

    def decodeArguments(self):
        if len(self.tweenables) == 0:
            print("TWEEN ERROR: No Tweenable properties or functions defined")
            self.complete = True
            return

        for k, v in self.tweenables.items():
            if not hasattr(self.target, k):
                print("TWEEN ERROR: " + str(self.target) + " has no function " + k)
                self.complete = True
                break

            prop = func = False
            startVal = 0
            newVal = v

            try:
                startVal = self.target.__dict__[k]
                prop = k
                propName = k
            except:
                func = getattr(self.target, k)
                funcName = k

            if func:
                try:
                    getFunc = getattr(self.target, funcName.replace("set", "get"))
                    startVal = getFunc()
                except:
                    startVal = newVal * 0
                tweenable = Tweenable(startVal, newVal - startVal)
                newFunc = [k, func, tweenable]
                self.tFuncs.append(newFunc)

            if prop:
                tweenable = Tweenable(startVal, newVal - startVal)
                newProp = [k, prop, tweenable]
                self.tProps.append(newProp)

    def pause(self, numSeconds=-1):
        self.paused = True
        self.delay = numSeconds

    def resume(self):
        if self.paused:
            self.paused = False

    def update(self, ptime):
        if self.complete:
            return

        if self.paused:
            if self.delay > 0:
                self.delay = max(0, self.delay - ptime)
                if self.delay == 0:
                    self.paused = False
                    self.delay = -1
                if self.updateFunction:
                    self.updateFunction()
            return

        self.delta = min(self.delta + ptime, self.duration)

        for propName, prop, tweenable in self.tProps:
            self.target.__dict__[prop] = self.tween(self.delta, tweenable.startValue, tweenable.change, self.duration)
        for funcName, func, tweenable in self.tFuncs:
            func(self.tween(self.delta, tweenable.startValue, tweenable.change, self.duration))

        if self.delta == self.duration:
            self.complete = True
            if self.completeFunction:
                self.completeFunction()

        if self.updateFunction:
            self.updateFunction()

    def getTweenable(self, name):
        ret = None
        for n, f, t in self.tFuncs:
            if n == name:
                ret = t
                return ret
        for n, p, t in self.tProps:
            if n == name:
                ret = t
                return ret
        return ret

    def Remove(self):
        self.complete = True

class Tweenable:
    def __init__(self, start, change):
        self.startValue = start
        self.change = change

# ------------------- EASING COMPLETE ---------------------

class Easing:
    class Back:
        @staticmethod
        def easeIn(t, b, c, d, s=1.70158):
            t = t / d
            return c * t**2 * ((s+1) * t - s) + b

        @staticmethod
        def easeOut(t, b, c, d, s=1.70158):
            t = t / d - 1
            return c * (t**2 * ((s + 1) * t + s) + 1) + b

        @staticmethod
        def easeInOut(t, b, c, d, s=1.70158):
            t = t / (d * 0.5)
            s = s * 1.525
            if t < 1:
                return c * 0.5 * (t**2 * ((s + 1) * t - s)) + b
            t = t - 2
            return c / 2 * (t**2 * ((s + 1) * t + s) + 2) + b

    class Bounce:
        @staticmethod
        def easeOut(t, b, c, d):
            t = t / d
            if t < 1 / 2.75:
                return c * (7.5625 * t**2) + b
            elif t < 2 / 2.75:
                t = t - 1.5 / 2.75
                return c * (7.5625 * t**2 + 0.75) + b
            elif t < 2.5 / 2.75:
                t = t - 2.25 / 2.75
                return c * (7.5625 * t**2 + .9375) + b
            else:
                t = t - 2.625 / 2.75
                return c * (7.5625 * t**2 + 0.984375) + b

        @staticmethod
        def easeIn(t, b, c, d):
            return c - Easing.Bounce.easeOut(d-t, 0, c, d) + b

        @staticmethod
        def easeInOut(t, b, c, d):
            if t < d * 0.5:
                return Easing.Bounce.easeIn(t * 2, 0, c, d) * .5 + b
            return Easing.Bounce.easeOut(t * 2 - d, 0, c, d) * .5 + c * .5 + b

    class Cubic:
        @staticmethod
        def easeIn(t, b, c, d):
            t = t / d
            return c * t**3 + b

        @staticmethod
        def easeOut(t, b, c, d):
            t = t / d - 1
            return c * (t**3 + 1) + b

        @staticmethod
        def easeInOut(t, b, c, d):
            t = t / (d * 0.5)
            if t < 1:
                return c * 0.5 * t**3 + b
            t = t - 2
            return c * 0.5 * (t**3 + 2) + b

    class Elastic:
        @staticmethod
        def easeIn(t, b, c, d, a=0, p=0):
            if t == 0: return b
            t = t / d
            if t == 1: return b + c
            if not p: p = d * .3
            if not a or a < abs(c):
                a = c
                s = p / 4
            else:
                s = p / (2 * math.pi) * math.asin(c / a)
            t = t - 1
            return -(a * math.pow(2, 10 * t) * math.sin((t * d - s) * (2 * math.pi) / p)) + b

        @staticmethod
        def easeOut(t, b, c, d, a=0, p=0):
            if t == 0: return b
            t = t / d
            if t == 1: return b + c
            if not p: p = d * .3
            if not a or a < abs(c):
                a = c
                s = p / 4
            else:
                s = p / (2 * math.pi) * math.asin(c / a)
            return a * math.pow(2, -10 * t) * math.sin((t * d - s) * (2 * math.pi) / p) + c + b

        @staticmethod
        def easeInOut(t, b, c, d, a=0, p=0):
            if t == 0: return b
            t = t / (d * 0.5)
            if t == 2: return b + c
            if not p: p = d * (.3 * 1.5)
            if not a or a < abs(c):
                a = c
                s = p / 4
            else:
                s = p / (2 * math.pi) * math.asin(c / a)
            if t < 1:
                t = t - 1
                return -.5 * (a * math.pow(2, 10 * t) * math.sin((t * d - s) * (2 * math.pi) / p)) + b
            t = t - 1
            return a * math.pow(2, -10 * t) * math.sin((t * d - s) * (2 * math.pi) / p) * .5 + c + b

    class Circ:
        @staticmethod
        def easeIn(t, b, c, d):
            t = t / d
            return -c * (math.sqrt(1 - t**2) - 1) + b

        @staticmethod
        def easeOut(t, b, c, d):
            t = t / d - 1
            return c * math.sqrt(1 - t**2) + b

        @staticmethod
        def easeInOut(t, b, c, d):
            t = t / (d * 0.5)
            if t < 1:
                return -c * 0.5 * (math.sqrt(1 - t**2) - 1) + b
            t = t - 2
            return c * 0.5 * (math.sqrt(1 - t**2) + 1) + b

    class Linear:
        @staticmethod
        def easeNone(t, b, c, d):
            return c * t / d + b

        @staticmethod
        def easeIn(t, b, c, d):
            return c * t / d + b

        @staticmethod
        def easeOut(t, b, c, d):
            return c * t / d + b

        @staticmethod
        def easeInOut(t, b, c, d):
            return c * t / d + b

    class Quad:
        @staticmethod
        def easeIn(t, b, c, d):
            t = t / d
            return c * t**2 + b

        @staticmethod
        def easeOut(t, b, c, d):
            t = t / d
            return -c * t * (t - 2) + b

        @staticmethod
        def easeInOut(t, b, c, d):
            t = t / (d * 0.5)
            if t < 1:
                return c * 0.5 * t**2 + b
            t = t - 1
            return -c * 0.5 * (t * (t - 2) - 1) + b

    class Quart:
        @staticmethod
        def easeIn(t, b, c, d):
            t = t / d
            return c * t**4 + b

        @staticmethod
        def easeOut(t, b, c, d):
            t = t / d - 1
            return -c * (t**4 - 1) + b

        @staticmethod
        def easeInOut(t, b, c, d):
            t = t / (d * 0.5)
            if t < 1:
                return c * 0.5 * t**4 + b
            t = t - 2
            return -c * 0.5 * (t**4 - 2) + b

    class Quint:
        @staticmethod
        def easeIn(t, b, c, d):
            t = t / d
            return c * t**5 + b

        @staticmethod
        def easeOut(t, b, c, d):
            t = t / d - 1
            return c * (t**5 + 1) + b

        @staticmethod
        def easeInOut(t, b, c, d):
            t = t / (d * 0.5)
            if t < 1:
                return c * 0.5 * t**5 + b
            t = t - 2
            return c * 0.5 * (t**5 + 2) + b

    class Sine:
        @staticmethod
        def easeIn(t, b, c, d):
            return -c * math.cos(t / d * (math.pi / 2)) + c + b

        @staticmethod
        def easeOut(t, b, c, d):
            return c * math.sin(t / d * (math.pi / 2)) + b

        @staticmethod
        def easeInOut(t, b, c, d):
            return -c * 0.5 * (math.cos(math.pi * t / d) - 1) + b

    class Strong:
        @staticmethod
        def easeIn(t, b, c, d):
            return c * (t / d) ** 5 + b

        @staticmethod
        def easeOut(t, b, c, d):
            return c * ((t / d - 1) ** 5 + 1) + b

        @staticmethod
        def easeInOut(t, b, c, d):
            t = t / (d * 0.5)
            if t < 1:
                return c * 0.5 * t**5 + b
            t = t - 2
            return c * 0.5 * (t**5 + 2) + b

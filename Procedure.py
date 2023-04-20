class Procedure:
    def __init__(self, name, chatid, endProcedure):
        self.name = name
        self.actions = []
        self.chatid = chatid
        self.endProcedure = endProcedure

    def StartProcedure(self):
        self.actions[0].BeginInvoke(self.chatid)

    def ContinueProcedure(self, args):
        action = self.GetCurrentAction()

        if action is not None:
            action.EndInvoke(args)
            nextAction = self.GetNextAction(action)
            if nextAction is not None:
                nextAction.BeginInvoke(self.chatid)
                return True
        self.endProcedure(self.actions, self.chatid)
        return False

    def GetCurrentAction(self):
        for action in self.actions:
            if not action.isDone:
                return action
        return None

    def GetNextAction(self, action):
        for i in range(len(self.actions)):
            if self.actions[i].name == action.name:
                if len(self.actions) - 1 >= i + 1:
                    return self.actions[i+1]
                else:
                    return None


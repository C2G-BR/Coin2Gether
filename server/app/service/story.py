class Step:
    def __init__(self, text):
        self.text = text
        self.is_complete = False

    def _complete(self):
        self.is_complete = True 

class FinalStep(Step):
    def __init__(self, on_success, on_fail):
        super().__init__(on_success)
        self.on_success = on_success
        self.on_fail = on_fail

class QuestionStep(Step):
    def __init__(self, text, field):
        super().__init__(text)
        self.field = field
        self.response = None
        self.dtype = str
    
    def respond(self, response):
        if (self.dtype is not None):
            response = self.dtype(response)
            if type(response) is self.dtype:
                self.response = response
                self._complete()
            else:
                raise TypeError('Different data type expected.')

class CheckStep(QuestionStep):
    def __init__(self, generate_text, field='check'):
        super().__init__(text='', field=field)
        self.dtype = bool
        self.generate_text = generate_text
    
class Story:
    def __init__(self, steps, on_final, token):
        self.steps = steps
        self.on_final = on_final
        self.is_complete = False
        self.token = token
    
    def answer_current_step(self, answer):
        idx = self.current_step_idx()
        self.steps[idx].respond(answer)
        message = self.get_next_step(idx+1)
        return message
    
    def current_step_idx(self):
        for idx, step in enumerate(self.steps):
            if not (step.is_complete):
                return idx
        return None
    
    def get_next_step(self, idx=0):
        step = self.steps[idx]
        dtype = type(step)
        if dtype is FinalStep:
            answers = self._get_answers()
            result = self.on_final(**answers)
            self._complete()
            message = step.on_success if result else step.on_fail
        elif dtype is CheckStep:
            answers = self._get_answers()
            message = step.generate_text(**answers)
        else:
            message = step.text
        return message

    def is_confirmation_step(self):
        step = self.steps[self.current_step_idx()]
        dtype = type(step)
        return dtype is CheckStep
    
    def _complete(self):
        self.is_complete = True
    
    def _get_answers(self):
        answers = {}
        answers['token'] = self.token
        for step in self.steps:
            if (step.is_complete):
                answers[step.field] = step.response
            else:
                break
        return answers
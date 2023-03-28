from app.service.post_service import new_post
from app.service.story import Story, QuestionStep, CheckStep, FinalStep

def post_story(token):
    def on_final(**kwargs):
        _token = kwargs.get('token')
        data = {
            'title': kwargs.get('title'),
            'content': kwargs.get('content')
        }
        is_successful = False
        if (kwargs.get('check')):
            try:
                new_post(_token, data)
                is_successful = True
            except:
                is_successful = False
        else:
            is_successful = False
        return is_successful
    
    def generate_text(**kwargs):
        title = kwargs.get('title')
        content = kwargs.get('content')
        text = f"Is the title \'{title}\' and the content \'{content}\' right?"
        return text

    steps = [
        QuestionStep('What will be the title?', 'title'),
        QuestionStep('What will be the content?', 'content'),
        CheckStep(generate_text),
        FinalStep('Post was sucessfully created', 'Post was not created.')
    ]
    story = Story(steps, on_final, token)
    return story
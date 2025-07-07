import mattermost_python as mp


def demo() -> mp.MattermostMessage:
    message = mp.MattermostMessage(
        icon_url='https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg',
        priority='important',
        message_info='Markdown message info here',
        colour='#FF0000',
        pretext='Markdown pretext',
        text='Markdown text',
        author_name='author',
        title='title',
        footer='footer',
        fields=[
            mp.MattermostField(False, 'Long title 1', 'value 1'),
            mp.MattermostField(True, 'Short title 2', 'value 2'),
            mp.MattermostField(True, 'Short title 3', 'value 3'),
            mp.MattermostField(True, 'Short title 4', 'value 4'),
            mp.MattermostField(False, 'Long title 6', 'value 6'),
            mp.MattermostField(True, 'Short title 5', 'value 5'),
        ]
    )
    return message

def demo_exception() -> mp.MattermostMessage:
    try:
        print(1/0)
    except Exception as e:
        message = mp.MattermostMessage.create_message_from_exception(e)
        return message
    return None

def main():
    m = mp.MattermostInterface('.mattermost_url.txt')

    message = demo()
    if not m.post(message):
        print("DEMO FAILED")
    
    # message = demo_exception()
    # if not m.post(message):
    #     print("EXCEPTION FAILED")


if __name__ == "__main__":
    main()
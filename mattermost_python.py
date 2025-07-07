import os
import re
import requests
import traceback
import validators

####################################################################################################
class MattermostField:
    """
    POD class for holding field information for the Mattermost message
    """
    def __init__(self, short : bool = False, title : str = '', value : str = ''):
        self.short = short
        self.title = title
        self.value = value
        return

####################################################################################################
class MattermostMessage:
    """
    Takes in information from the user which can theb be passed to the MattermostInterface class to
    send the Mattermost message to the desired incoming webhook. Note that this uses some Linux/macos
    only functionality to generate a default username
    """
    def __init__(self,
                 username : str = os.environ.get("USER") + "@" + os.uname()[1] + " " + __file__,
                 icon_url : str = '',
                 priority : str = 'standard',
                 message_info : str = '',
                 colour : str = '',
                 pretext : str = '',
                 text : str = '',
                 footer : str = '',
                 footer_icon : str = '',
                 author_name : str = '',
                 author_link : str = '',
                 author_icon : str = '',
                 title : str = '',
                 title_link : str = '',
                 fields : list = [],
                 **kwargs
        ):
        # Construct script + hostname (for Linux and macos only!!)
        self.username = username

        self.icon_url = icon_url

        if priority in ('standard', 'important', 'urgent'):
            self.priority = priority
        else:
            self.priority = ''

        self.message_info = message_info

        # Attachments
        pattern = re.match('#([0-9A-Fa-f]){6}$', colour)
        if pattern != None:
            self.colour = colour
        else:
            self.colour = ''

        self.pretext = pretext
        self.text = text
        self.footer = footer
        self.footer_icon = footer_icon
        self.author_name = author_name
        self.author_link = author_link
        self.author_icon = author_icon
        self.title = title
        self.title_link = title_link
        self.fields = fields

        # Ensure notification has something useful!
        self.notification_message = kwargs.get('notification_message', '')
        if self.notification_message == '':
            if self.title != '':
                self.notification_message = self.title
            elif self.pretext != '':
                self.notification_message = self.pretext
            elif self.text != '':
                self.notification_message = self.text
            else:
                self.notification_message = 'ALERT!'
    

        # Create message dictionary
        self._make_dict()
        return

    ####################################################################################################
    """
    This dictionary is passed to the POSTS request to send to Mattermost
    """
    def _make_dict(self):
        # Create dict based on certain items
        data = {}
        if self.username != '':
            data['username'] = self.username

        if self.icon_url != '':
            data['icon_url'] = self.icon_url

        if self.message_info != '':
            data['props'] = { "card" : self.message_info}

        if self.priority != '':
            data['priority'] = { "priority" : self.priority }
            
        # "Attachments"
        attachments = {}
        if self.notification_message != '':
            attachments['fallback'] = self.notification_message
        
        if self.colour != '':
            attachments['color'] = self.colour
        
        if self.pretext != '':
            attachments['pretext'] = self.pretext
        
        if self.text != '':
            attachments['text'] = self.text
        
        if self.footer != '':
            attachments['footer'] = self.footer

        if self.author_name != '':
            attachments['author_name'] = self.author_name

        if self.author_link != '':
            attachments['author_link'] = self.author_link

        if self.author_icon != '':
            attachments['author_icon'] = self.author_icon # NOTE THIS MUST BE A URL

        if self.title != '':
            attachments['title'] = self.title

        if self.title_link != '':
            attachments['title_link'] = self.title_link

        if self.footer_icon != '':
            attachments['footer_icon'] = self.footer_icon # NOTE THIS MUST BE A URL
        
        if self.fields != None:
            fields = []
            for field in self.fields:
                if type(field) == MattermostField:
                    fields.append({"short" : field.short, "title" : field.title, "value" : field.value})
                else:
                    print(f"WARNING - unauthorised use of fields field!")
            
            attachments['fields'] = fields

        data['attachments'] = [attachments]

        self.dict = data
        return

    ####################################################################################################
    """
    A nice static method to package up an exception and post as a message
    """
    @staticmethod
    def create_message_from_exception(exception : Exception):
        message = MattermostMessage(
            title=type(exception).__name__,
            text="```python\n" + traceback.format_exc() + "\n```"
        )
        return message
    
    ####################################################################################################
    """
    A getter for the dictionary
    """
    def get_dict(self) -> dict:
        self._make_dict()
        return self.dict


####################################################################################################
class MattermostInterface:
    """
    See https://developers.mattermost.com/integrate/webhooks/incoming/ for details, but this just
    sends the request to mattermost, and, provided your webhook URL is valid, we can start posting
    messages!
    """
    def __init__(self, incomingwebhook : str, timeout : float = 2.5):
        # Store timeout
        if timeout > 0:
            self.timeout = timeout
        else:
            self.timeout = 2.5


        # Check if incomingwebhook is a URL or a file path
        if os.path.exists(incomingwebhook):
            # It's a file path, open the file and get the URL
            lines = []
            with open(incomingwebhook, 'r') as file:
                # Grab first URL it can
                for line in file:
                    if validators.url(line.strip()):
                        self.url = line.strip()
                        break
        
        elif validators.url(incomingwebhook):
            # It's a URL
            self.url = incomingwebhook
        
        else:
            # No idea what it is
            raise ValueError("Must be a file path containing a valid URL or a URL itself. Exiting...")

    ####################################################################################################
    """
    Post the message, and return true or false if it worked!
    """
    def post( self, message : MattermostMessage ) -> bool:
        # Get the message
        data = message.get_dict()

        # Send the data
        x = requests.post(self.url, json=data, timeout=self.timeout)

        # Check if the message sent
        if x.status_code == 200:
            return True
        return False



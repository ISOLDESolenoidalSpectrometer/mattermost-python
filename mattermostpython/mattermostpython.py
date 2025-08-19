import enum
import os
import re
import requests
import traceback
import validators

####################################################################################################
class MattermostMessagePriority(enum.Enum):
    """
    Enum for holding mattermost message priority
    """
    STANDARD = 0
    IMPORTANT = 1
    URGENT = 2

    def __str__(self):
        if self.value == 0:
            return 'standard'
        if self.value == 1:
            return 'important'
        if self.value == 2:
            return 'urgent'
        return ''
        

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
    Takes in information from the user which can then be passed to the MattermostInterface class to
    send the Mattermost message to the desired incoming webhook. Note that this uses some Linux/macos
    only functionality to generate a default username
    """
    def __init__(self,
                 username : str = '',
                 icon_url : str = '',
                 priority : MattermostMessagePriority = MattermostMessagePriority.STANDARD,
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
        # Start storing member variables
        self.username = username
        self.icon_url = icon_url
        self.priority = priority
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

        return
    
    ####################################################################################################
    # GETTERS
    def get_username(self) -> str:
        return self.username
    
    def get_icon_url(self) -> str:
        return self.icon_url
    
    def get_priority(self) -> MattermostMessagePriority:
        return self.priority
    
    def get_message_info(self) -> str:
        return self.message_info
    
    def get_colour(self) -> str:
        return self.colour
    
    def get_pretext(self) -> str:
        return self.pretext
    
    def get_text(self) -> str:
        return self.text
    
    def get_footer(self) -> str:
        return self.footer
    
    def get_footer_icon(self) -> str:
        return self.footer_icon
    
    def get_author_name(self) -> str:
        return self.author_name
    
    def get_author_link(self) -> str:
        return self.author_link
    
    def get_author_icon(self) -> str:
        return self.author_icon
    
    def get_title(self) -> str:
        return self.title
    
    def get_title_link(self) -> str:
        return self.title_link
    
    def get_fields(self) -> list[MattermostField]:
        return self.fields
    
    ####################################################################################################
    # SETTERS
    def set_username(self, x : str) -> None:
        self.username = x
        return
    
    def set_icon_url(self, x : str) -> None:
        self.icon_url = x
        return
    
    def set_priority(self, x : MattermostMessagePriority) -> None:
        self.priority = x
        return
    
    def set_message_info(self, x : str) -> None:
        self.message_info = x
        return
    
    def set_colour(self, x : str) -> None:
        self.colour = x
        return
    
    def set_pretext(self, x : str) -> None:
        self.pretext = x
        return
    
    def set_text(self, x : str) -> None:
        self.text = x
        return
    
    def set_footer(self, x : str) -> None:
        self.footer = x
        return
    
    def set_footer_icon(self, x : str) -> None:
        self.footer_icon = x
        return
    
    def set_author_name(self, x : str) -> None:
        self.author_name = x
        return
    
    def set_author_link(self, x : str) -> None:
        self.author_link = x
        return
    
    def set_author_icon(self, x : str) -> None:
        self.author_icon = x
        return
    
    def set_title(self, x : str) -> None:
        self.title = x
        return
    
    def set_title_link(self, x : str) -> None:
        self.title_link = x
        return
    
    def set_fields(self, x : list[MattermostField]) -> None:
        self.fields = x
        return
    
    def add_field( self, x : MattermostField) -> None:
        self.fields.append(x)
        return
    

    ####################################################################################################
    def _make_dict(self):
        """
        This dictionary is passed to the POSTS request to send to Mattermost
        """
        # Create dict based on certain items
        data = {}
        if self.username != '':
            data['username'] = self.username

        if self.icon_url != '':
            data['icon_url'] = self.icon_url

        if self.message_info != '':
            data['props'] = { "card" : self.message_info}

        if self.priority != '':
            data['priority'] = { "priority" : str( self.priority ) }
            
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
    @staticmethod
    def create_message_from_exception(exception : Exception):
        """
        A nice static method to package up an exception and post as a message
        """
        message = MattermostMessage(
            title=type(exception).__name__,
            text="```python\n" + traceback.format_exc() + "\n```"
        )
        return message
    
    ####################################################################################################
    def get_message_data(self) -> dict:
        """
        A getter for the dictionary
        """
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
            # No idea what has been passed as a webhook
            raise ValueError("Must be a file path containing a valid URL or a URL itself. Exiting...")

    ####################################################################################################
    def post( self, message : MattermostMessage ) -> bool:
        """
        Post the message, and return true or false if it worked!
        """
        # Get the message
        data = message.get_message_data()

        # Send the data
        x = requests.post(self.url, json=data, timeout=self.timeout)

        # Check if the message sent
        if x.status_code == 200:
            return True
        return False



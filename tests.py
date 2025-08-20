import unittest
import mattermostpython as mp

ICON_URL = 'https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg'

class MattermostPythonTest( unittest.TestCase ):
    def setUp(self):
        self.interface = mp.MattermostInterface('.mattermost_url.txt')
        mp.MattermostMessage.set_default_title('DEFAULT TITLE')
    
    def test_empty_message(self):
        message = mp.MattermostMessage()
        self.assertTrue( self.interface.post(message) )

    def test_username(self):
        message = mp.MattermostMessage()
        message.set_username('TEST USERNAME')
        self.assertTrue( self.interface.post(message) ) 

    def test_icon_url(self):
        message = mp.MattermostMessage()
        message.set_icon_url(ICON_URL)
        self.assertTrue( self.interface.post(message) )

    def test_priority_important(self):
        message = mp.MattermostMessage()
        message.set_priority(mp.MattermostMessagePriority.IMPORTANT)
        self.assertTrue( self.interface.post(message) )
    
    def test_priority_urgent(self):
        message = mp.MattermostMessage()
        message.set_priority(mp.MattermostMessagePriority.URGENT)
        self.assertTrue( self.interface.post(message) )

    def test_message_info(self):
        message = mp.MattermostMessage()
        message.set_message_info('TEST MESSAGE INFO')
        self.assertTrue( self.interface.post(message) )
    
    def test_message_colour(self):
        message = mp.MattermostMessage()
        message.set_colour('#999999')
        self.assertTrue( self.interface.post(message) )

    def test_message_pretext(self):
        message = mp.MattermostMessage()
        message.set_pretext('TEST MESSAGE PRETEXT')
        self.assertTrue( self.interface.post(message) )

    def test_message_text(self):
        message = mp.MattermostMessage()
        message.set_text('TEST MESSAGE TEXT')
        self.assertTrue( self.interface.post(message) )

    def test_footer(self):
        message = mp.MattermostMessage()
        message.set_footer('TEST MESSAGE FOOTER')
        self.assertTrue( self.interface.post(message) )

    def test_footer_icon(self):
        message = mp.MattermostMessage()
        message.set_message_info(ICON_URL)
        self.assertTrue( self.interface.post(message) )

    def test_author_name(self):
        message = mp.MattermostMessage()
        message.set_author_name('TEST MESSAGE AUTHOR NAME')
        self.assertTrue( self.interface.post(message) )

    def test_author_icon(self):
        message = mp.MattermostMessage()
        message.set_author_icon(ICON_URL)
        self.assertTrue( self.interface.post(message) )

    def test_author_link(self):
        message = mp.MattermostMessage()
        message.set_author_link(ICON_URL)
        self.assertTrue( self.interface.post(message) )

    def test_title(self):
        message = mp.MattermostMessage()
        message.set_title('TEST MESSAGE TITLE')
        self.assertTrue( self.interface.post(message) )

    def test_title_link(self):
        message = mp.MattermostMessage()
        message.set_title_link(ICON_URL)
        self.assertTrue( self.interface.post(message) )

    def test_fields(self):
        message = mp.MattermostMessage()
        message.add_field( mp.MattermostField( True, 'Title 1', 'Value 1' ) )
        message.add_field( mp.MattermostField( True, 'Title 2', 'Value 2' ) )
        message.add_field( mp.MattermostField( False, 'Title 3', 'Value 3' ) )
        self.assertTrue( self.interface.post(message) )
    
    def test_fields2(self):
        message = mp.MattermostMessage()
        message.set_fields( [
            mp.MattermostField( True, 'Title 1', 'Value 1' ),
            mp.MattermostField( True, 'Title 2', 'Value 2' ),
            mp.MattermostField( False, 'Title 3', 'Value 3' )
        ] )
        self.assertTrue( self.interface.post(message) )
    
    def test_full_message(self):
        message = mp.MattermostMessage()
        message.set_username('TEST USERNAME')
        message.set_icon_url(ICON_URL)
        message.set_priority(mp.MattermostMessagePriority.IMPORTANT)
        message.set_message_info('TEST MESSAGE INFO')
        message.set_colour('#999999')
        message.set_pretext('TEST MESSAGE PRETEXT')
        message.set_text('TEST MESSAGE TEXT')
        message.set_footer('TEST MESSAGE FOOTER')
        message.set_message_info(ICON_URL)
        message.set_author_name('TEST MESSAGE AUTHOR NAME')
        message.set_author_icon(ICON_URL)
        message.set_author_link(ICON_URL)
        message.set_title('TEST MESSAGE TITLE')
        message.set_title_link(ICON_URL)
        message.add_field( mp.MattermostField( True, 'Title 1', 'Value 1' ) )
        message.add_field( mp.MattermostField( True, 'Title 2', 'Value 2' ) )
        message.add_field( mp.MattermostField( False, 'Title 3', 'Value 3' ) )
        self.assertTrue( self.interface.post(message) )
    
    def test_exception(self):
        try:
            print(1/0)
            self.assertFalse(True, "This should have failed already")
        except Exception as e:
            message = mp.MattermostMessage.create_message_from_exception(e)
            self.assertTrue( self.interface.post(message) )

if __name__ == "__main__":
    unittest.main()
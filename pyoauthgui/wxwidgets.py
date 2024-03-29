'''
This module I made to be easy to auth user in oauth2
Require:
wx
Created on Nov 24, 2011

@author: hugosenari
part of code from:
http://www.learningpython.com/2007/01/29/creating-a-gui-using-python-wxwidgets-and-wxpython/
'''

import re, urlparse, wx
from wx.html import HtmlWindow, HTML_OPEN


class OauthGuid(object):
    '''
    Easy python oauth2 authentication interface with wxWidgets
    '''

    def __init__(self, uri, callback, oauthCallback=None, app=None, 
                 title='Authentication', 
                 label='If redirect doesn\'t work, type code on input then click in ok.', 
                 bt_label='ok'):
        '''
        params:
            uri: string url to open in browser for user get oauth verifier
            callback: callable function that receives as unique param oauth verifiers (str)
            oauthCallback: pattern of redirect url with oauth verifier
            app: wxApp
            title: window title
            label: input label
            bt_label: ok button label
        '''
        #try to use user pattern
        if oauthCallback:
            self._oauth_callback = oauthCallback
        #try to use common pattern 
        elif re.match('oauth_callback=', uri):
            params = uri.split('oauth_callback=')
            self._oauth_callback = params[1].split('&')[0]
        #try to use default pattern
        else:
            sep = "&" if re.match('.+\?.+', uri) else "?"
            self._oauth_callback = 'https%3A%2F%2Flocalhost%2Foauth_callback'
            uri = "%s%soauth_callback=%s" % (uri, sep, self._oauth_callback) 
            
        self.uri = uri
        self.callback = callback
        self.window = None
        self.app = app if app else wx.App()
        self.entry = None
        self.tx_label = label
        self.tx_title = title
        self.tx_bt_label = bt_label
        self._show()

    def _show(self):
        ##draw window
        window = wx.Frame(None, title=self.tx_title)
        self.app.SetTopWindow(window)
        self.window = window
        root_box = wx.BoxSizer(wx.VERTICAL)
        window.SetSizer(root_box)
        
        #draw uri information
        uri_bar = wx.BoxSizer(wx.HORIZONTAL)
        uri_field = wx.TextCtrl(window, size=wx.Size(570, -1))
        uri_field.SetValue(self.uri)
        uri_bar.Add(uri_field, 1, wx.EXPAND)
        root_box.Add(uri_bar, 0)
        
        ##draw browser
        _self = self
        class Html_Window(HtmlWindow):
            def OnOpeningURL(self, *args, **kwargs):
                if _self._callback(*args):
                    return super(HtmlWindow, self).OnOpeningURL(*args, **kwargs)
                return HTML_OPEN

        browser = Html_Window(window)
        browser.LoadPage(self.uri)
        browse_box = wx.BoxSizer(wx.HORIZONTAL)
        browse_box.Add(browser, 1, wx.EXPAND)
        root_box.Add(browse_box, 1, wx.EXPAND)
        
        ##draw form fields
        form_bar = wx.BoxSizer(wx.VERTICAL)
        #label
        label = wx.StaticText(window, label=self.tx_label)
        form_bar.Add(label, 0)
        #input and button
        field_box = wx.BoxSizer(wx.HORIZONTAL)
        entry = wx.TextCtrl(window, size=wx.Size(370, -1))
        self.entry = entry
        field_box.Add(entry, 1)
        btn = wx.Button(window, label=self.tx_bt_label)
        def clicked(*args): self._ok(*args)
        btn.Bind(wx.EVT_BUTTON, clicked)
        field_box.Add(btn, 0)
        form_bar.Add(field_box, 0)
        root_box.Add(form_bar, 0)
        
        #fit windows boxes
        root_box.Fit(window)
        window.SetMinSize(root_box.GetMinSize())
        window.Show()
    
    def _callback(self, url_type, uri, redir=None):
        if url_type == 0 \
                and re.match(self._oauth_callback, uri):
            callback = self.callback
            self.window.Close()
            if callback and callable(callback):
                return callback(uri)
            return uri
    
    def _ok(self, *args):
        code = self.entry.GetValue()
        callback = self.callback 
        if callback and callable(callback):
            self.window.Close()
            return callback(code)
        return code
    
    def main(self, *args, **kw):
        self.app.MainLoop()

class OauthGui(OauthGuid):
    def __init__(self, uri, callback, paramName='oauth_token', *args, **kwargs):
        '''
        params:
            uri: string url to open in browser for user get oauth verifier
            callback: callable function that receives as unique param oauth verifiers (str)
            oauthCallback: pattern of redirect url with oauth verifier
            paramName: param name in callback result
        '''
        def _callback(url):
            if paramName:
                for param in urlparse.urlparse(url).query.split('&'):
                    keyValue = param.split('=')
                    if len(keyValue) > 1 and keyValue[0] == paramName:
                        if callback and callable(callback):
                            return callback(keyValue[1])
            if callback and callable(callback):
                return callback(url)
            return url

        super(OauthGui, self).__init__(uri, _callback, *args, **kwargs)

if __name__ == "__main__":
    def callback(code):
        print 'callback: ', code
    app = OauthGui('http://localhost/', callback)
    app.main()
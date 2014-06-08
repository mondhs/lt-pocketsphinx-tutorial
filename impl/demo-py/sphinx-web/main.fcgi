#!/home/myuser/public_html/myenv/bin/python
# -*- coding: utf-8 -*-



import sys, os
import re
import cgi
import subprocess

MODELDIR = "/home/myuser/tmp/pocketsphinx-bin/impl/models"



def recognize(environ, start_response):
    """This function will be mounted on "/" and display a link
    to the hello world page."""
    contentType='text/html; charset=utf8'
    output = ""
    if environ['REQUEST_METHOD'] == 'POST' or environ['REQUEST_METHOD'] == 'PUT':
        post = cgi.FieldStorage(
                fp=environ['wsgi.input'],
                environ=environ,
                keep_blank_values=True
            )
        fileitem = post["wavfile"]
        if fileitem.file:
            filename = fileitem.filename.decode('utf8').replace('\\','/').split('/')[-1].strip()
            if not filename:
                raise Exception('No valid filename specified')
            file_path = os.path.join("/tmp", filename + ".wav")
            # Using with makes Python automatically close the file for you
            counter = 0
            with open(file_path, 'wb') as output_file:
                # In practice, sending these messages doesn't work
                # environ['wsgi.errors'].write('Receiving upload ...\n')
                # environ['wsgi.errors'].flush()
                # print 'Receiving upload ...\n'
                while 1:
                    data = fileitem.file.read(1024)
                    # End of file
                    if not data:
                        break
                    output_file.write(data)
                    counter += 1
                    if counter == 100:
                        counter = 0
                        # environ['wsgi.errors'].write('.')
                        # environ['wsgi.errors'].flush()
                        # print '.',
            # Injection attack possible on the filename - should escape!
            #body = u"File uploaded successfully to <tt>%s</tt>. Its filename is <tt>%s</tt>"%(
            #    filename,
            #    cgi.escape(fileitem.filename),
            #)
            file_path_sox = os.path.join("/tmp", filename + "_16.wav")
            result, err = subprocess.Popen(["/home/myuser/bin/sox  "+file_path+" -b16 " +file_path_sox+ " rate 16000 dither -s" ], shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
            if not err:
               output = subprocess.Popen(["/home/myuser/bin/external-sphinx.sh " + file_path_sox], shell=True, stdout=subprocess.PIPE).communicate()[0]
            contentType='application/json; charset=utf8'
            recognitionResult = re.compile('(<.*>)').sub('',output).strip(' \t\n\r')
            body = '{ "result" : "%s"}\n\n\n\n' %(recognitionResult)
            body = body.decode('utf8') 
    else:
        body = u"""
<html>
<head><title>Upload</title></head>
<body>
<form name="test" method="post" action="" enctype="multipart/form-data">
File: <input type="file" name="wavfile" />
<input type="submit" name="submit" value="Submit" />
</form>
<p>Note: files with the same name with overwrite any existing files.</p>
</body>
</html>
"""
    start_response(
        '200 OK',
         [
             ('Content-type', contentType),
             ('Content-Length', str(len(body))),
         ]
    )
    return [body.encode('utf8')]

    
def index(environ, start_response):
    """This function will be mounted on "/" and display a link
    to the hello world page."""
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['''Sveiki.

''']



def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

# map urls to functions
urls = [
    (r'^$', index),
    (r'recognize/?$', recognize),
    
]

def application(environ, start_response):
    """
    The main WSGI application. Dispatch the current request to
    the functions from above and store the regular expression
    captures in the WSGI environment as  `myapp.url_args` so that
    the functions from above can access the url placeholders.

    If nothing matches call the `not_found` function.
    """
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['myapp.url_args'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)



# FastCGI link: Apache/mod_fcgid <-> Python (WSGI server)
# (odd enough for the first time: FastCGI<->WSGI wrapper/gateway)
if __name__ == '__main__':
    from flup.server.fcgi import WSGIServer
    WSGIServer(application).run()


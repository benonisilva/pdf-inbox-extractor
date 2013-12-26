# -*- coding: utf-8 -*-
import mailbox, pickle, os
from email.header import decode_header
import string_util

INBOX = r'C:\Users\jamesli\AppData\Roaming\Thunderbird\Profiles\fgvkk9zc.default\ImapMail\imap.googlemail.com\INBOX'
prefs_path = r'config'
save_to = r'.'

try:
    with open(prefs_path, 'rb') as f:
        prefs = pickle.load(f)
except:
    prefs = dict(start=0)
    prefs.update(dict(path=INBOX))
    prefs.update(dict(dir=save_to))

print prefs
mb = mailbox.mbox(prefs['path'])
def save_attachments(mid):
    
    msg = mb.get_message(mid)
    #print msg 
    if msg.is_multipart():
        #print msg
        for part in msg.get_payload():
            if part.get_content_type() != 'application/pdf':
                continue
            file_name = part.get_filename()
            sender_name = msg['from'].split()[0]
            #print file_name

            try:
                encoding = decode_header(file_name)
            except UnicodeEncodeError:
                file_name = string_util.strip_diacriticals(file_name)
                encoding = decode_header(file_name)
                #print "fail"
            bytes = encoding[0][0]
            enc = encoding[0][1]
            #print encoding[0]
            if(enc==None):
                enc = 'utf-8'
            f = bytes.decode(enc)
            #notify('Saving' % part.get_filename())
            directory = creat_userDir(prefs['dir'],sender_name)
            with open(directory +'\\'+f, 'wb') as f:
                f.write(part.get_payload(decode=True))
            
def run_script():
    print 'running...\n'
    for i in range(prefs['start'], 1000000):
        try:
            #print i
            save_attachments(i)
        except KeyError:
            break
    save_prefs('start',i)

def creat_userDir(path,user):
    directory = path+'\\'+user  
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory    
    
def save_prefs(key,value):
    prefs[key] = value
    with open(prefs_path, 'wb') as f:
        pickle.dump(prefs, f)

if __name__ == "__main__":
    #run_script()
    pass

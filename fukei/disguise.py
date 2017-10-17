#coding=utf-8
__author__ = 'easton'
import unittest, os, random, string, re

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

http_request_payload_template = '''GET /{1}.png HTTP/1.1\r
Host: s1.hao123img.com\r
Referer: http://www.hao123.com/\r
Accept-Encoding: gzip, deflate, sdch\r
Cookie: previous_pic={2}'''

'''GET {}.png HTTP/1.1
Host: s1.hao123img.com
Connection: keep-alive
Accept: image/webp,*/*;q=0.8
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36
DNT: 1
Referer: http://www.hao123.com/
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2

'''

http_responce_payload_template = '''HTTP/1.1 200 OK\r
Content-Type: image/png\r
Connection: keep-alive\r
\r
\x89PNG\r\n\x1a\x0a{1}\x00\x00\x00\x00IEND\xaeB\x60\x82
'''

'''HTTP/1.1 200 OK
Server: JSP3/2.0.6
Date: Mon, 20 Apr 2015 05:28:02 GMT
Content-Type: image/png
Content-Length: 3373
Connection: keep-alive
ETag: "3659221251"
Last-Modified: Fri, 30 Aug 2013 03:31:33 GMT
Expires: Sun, 01 Nov 2015 08:05:08 GMT
Age: 14246574
Cache-Control: max-age=31104000
LFY: cq02.i3
Accept-Ranges: bytes

‰PNG
{}

'''

disguise_count = 0
extract_count = 0
extract_success = 0

def replace_LF_with_CRLF(string):
    """
    :type string: str
    :rtype: str
    """
    return string.replace('\n', '\r\n')

def disguise_as_http_request(data):
    global disguise_count
    disguise_count += 1
    #print 'disguising', disguise_count
    return (
        http_request_payload_template.replace('{1}', id_generator()).replace('{2}', data))

def extract_from_fake_http_request(request_str):
    """
    :type request_str: bytearray
    """
    #print 'extracting'
    global extract_count, extract_success
    extract_count += 1
    #print id(extract_count)
    if re.search('(^GET.*?=|\r\n\r\n$)', request_str, flags=re.DOTALL):
        extract_success += 1
    #return str(re.sub('(^GET.*?=|\r\n\r\n$)', '', request_str, flags=re.DOTALL))
    print extract_success, '/', extract_count
    striped = re.sub('(^GET.*?previous_pic=)', '', request_str, flags=re.DOTALL)
    return striped

def disguise_as_http_responce(data):
    return http_responce_payload_template.replace('{1}', data)

def extract_from_fake_http_responce(responce_str):
    return str(re.sub('(^\x89PNG\r\n\x1a\x0a|\x00\x00\x00\x00IEND\xaeB\x60\x82$)', '', responce_str, flags=re.DOTALL))

class Test(unittest.TestCase):
    def est_replace_LF_with_CRLF(self):
        for i in bytearray(replace_LF_with_CRLF(http_responce_payload_template)):
            print hex(i),

    def est_disguise_as_http_request(self):
        ba = bytearray((disguise_as_http_request('\x88ciphertext\n')))
        for i in ba:
            print hex(i),
        print
        print str(ba)

    def est_disguise_as_http_responce(self):
        for i in bytearray(disguise_as_http_responce('ciphertext\n')):
            print hex(i),

    def est_extract_from_fake_http_request(self):
        print extract_from_fake_http_request(disguise_as_http_request('\x99'))

    def est_extract_from_fake_http_responce(self):
        print repr(extract_from_fake_http_responce(disguise_as_http_responce('\x99')))

    def test_bytearray_replace(self):
        ba = bytearray('get\r\n=\x98\x50\r\n')
        print repr(re.sub('(^g.*?=|\r\n$)', '', ba, flags=re.DOTALL))

    def est_str_replace(self):
        print '{}'.replace('{}', '\x41')

    def est_unicode_reg(self):
        print len(u'\x88aa'.encode('utf-8'))
        #print repr(re.search(u'(\x88)', u'\x88adfasdf').group(1))

if __file__ == '__main__':
    unittest.main()
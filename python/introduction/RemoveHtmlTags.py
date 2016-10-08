#coding:utf-8

import re

def removeHtmlTags(htmlContent):
    print "Hello World!"
    abc = re.sub(r'\<fieldset.*\</fieldset\>', '', htmlContent)
    print htmlContent
    print abc

if __name__ == '__main__':
    htmlContent = r'<fieldset class="fieldset fieldset-mask"><legend>mask \u533a\u57df</legend><pre><mask><br></p><fieldset class="fieldset fieldset-code"><legend>code 区域</legend><pre><code>http://**.**.**.**/</code></pre></fieldset><p class="detail"><br><br></p></mask></fieldset>zhang'
    removeHtmlTags(htmlContent)

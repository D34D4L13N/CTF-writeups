# 📝 CTF Web Exploitation – Server Source Checklist (Resourceful Edition)

---

## 1️⃣ First Check – How do I get the source?
- [ ] Source given in challenge files (`.zip`, `.tar`, `.rar`, `.py`, `.php`)
- [ ] Hidden/leaked on server:
  - Try hidden paths:
    - `/.git/`, `/.svn/`, `/.DS_Store`, `.env`, `.bak`, `~`, `.old`
    - `index.php.bak`, `config.php.old`, `app.py~`
  - Try **PHP wrappers**:
    ```http
    ?file=php://filter/convert.base64-encode/resource=index.php
    ```
  - Try **path traversal**:
    ```http
    ?page=../../../../etc/passwd
    ```
- 🔧 **Tools**:
  - [git-dumper](https://github.com/arthaud/git-dumper) – dump exposed `.git` repos  
  - [DVCS-Pillage](https://github.com/evilpacket/DVCS-Pillage) – `.svn` & `.hg` leaks  

---

## 2️⃣ Recon the Code
- [ ] Identify **entry points** (routes, controllers, main files)
- [ ] Locate **user input** (`$_GET`, `$_POST`, `req.body`, query params)
- [ ] Search for **dangerous functions**:
  - PHP → `eval`, `exec`, `system`, `include`, `unserialize`
  - Python → `eval`, `exec`, `pickle.load`, `os.system`
  - Node → `child_process.exec`, `eval`, unsafe `require`
- 🔎 **Trick**: Use `grep`/`ripgrep` for fast scanning
  ```bash
  grep -R "exec(" .
  rg "eval"
  ```

---

## 3️⃣ Common Vulnerabilities in Server Source
- **SQL Injection**
  - Look for raw query strings (`"SELECT * FROM users WHERE id = " . $_GET['id']`)
  - Tools: [sqlmap](http://sqlmap.org/)
- **Command Injection**
  - Input passed to `system/exec`
  - Test payloads: `; id`, `&& cat /flag.txt`
- **File Inclusion (LFI/RFI)**
  - Input passed to `include` or `open`
  - Test: `?page=../../../../flag`
- **Auth Bypass**
  - Weak login conditions (`if($user == "admin")`)
- **Insecure Deserialization**
  - PHP `unserialize()`, Python `pickle.loads()`
  - Tools: [PHPGGC](https://github.com/ambionics/phpggc), [ysoserial](https://github.com/frohoff/ysoserial)
- **Hardcoded Secrets**
  - Check `.env`, `config.php`, `settings.py`
- **Logic Flaws**
  - Misused operators (`==` vs `===`)
  - Wrong order of checks

---

## 4️⃣ Exploitation Flow
- [ ] Confirm vulnerable input (GET/POST/header)
- [ ] Craft minimal payloads
  - SQLi → `' OR 1=1--`
  - Command injection → `; ls`
  - LFI → `../../flag.txt`
- [ ] If filters exist, try **bypass payloads**
  - SQLi → `' OR '1'='1`, `UNION SELECT NULL,NULL`
  - LFI → `....//....//flag`
- [ ] Search for **flag locations**
  - `/flag`, `/flag.txt`, `/var/www/flag`, `/home/ctf/flag.txt`
  - Database → `users`, `flags`, `secrets` tables
  - Hidden routes in code (e.g. `/admin`, `/debug`, `/secret`)

---

## 5️⃣ Quick Payload Reminders
- **SQLi Test:**  
  ```sql
  ' OR 1=1--
  ```
- **Command Injection:**  
  ```bash
  ; cat /flag.txt
  ```
- **File Inclusion:**  
  ```http
  ?page=../../../../flag
  ```
- **PHP Filter Read:**  
  ```http
  ?file=php://filter/convert.base64-encode/resource=index.php
  ```

---

✅ **Flag Hunting Checklist**  
- [ ] Search for `FLAG{` in source files  
- [ ] Check `.env`, `config`, `.git/config`, `db.sql`  
- [ ] Exploit vuln → read `/flag.txt` or DB  

---

⚡ **Pro Tip**: In “server source” challenges, the **answer is almost always in the code itself** — either a hidden route, weak filter, or hardcoded secret. Don’t just run the app, **read line by line**.

📚 **More Resources**
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)  
- [HackTricks](https://book.hacktricks.xyz/)  
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)  

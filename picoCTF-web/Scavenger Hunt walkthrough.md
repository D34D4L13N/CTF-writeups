### Step 1: Initial Recon
I loaded up the URL and clicked every visible button, but it was just a blank canvas. My gut said **“check DevTools”** so I right-clicked → Inspect and dove into the Elements panel. 
I hovered over the header and body <div>s, poked around, and—boom—stumbled on the first fragment buried in the HTML:
```
<!-- Here's the first part of the flag: picoCTF{t -->
```
Which is revealed the 1st part of the flag:`picoCTF{t`

### Step 2: The CSS Clue
Feeling emboldened, I switched to the Sources tab. There it was: a strangely named file `mycss.css`. Inside, in a commented-out rule:
```
/* CSS makes the page look nice, and yes, it also has part of the flag. Here's part 2: h4ts_4_l0 */
```
In the bottom has 2nd part: `h4ts_4_l0`

### Step 3: Robots.txt Revelation
Next, I turned to `myjs.js`, expecting another snippet. Instead, I found a cryptic comment:

*“How do I prevent Google from indexing my site?”*

My SEO background clicked — robots.txt was the answer. I typed `…/robots.txt` into the address bar and hit Enter. Fragment 3rd part: `t_0f_pl4c`

And there a line hinted something *# I think this is an apache server... can you Access the next flag?*

### Step 4: The Apache Hunt
Inside `robots.txt` was a note: “Built with Apache.” I’d never configured Apache, so I googled **“common Apache hidden files”** and wrote down a list of slugs to try:
```
/.htaccess, /.htpasswd, /server-status, /error.log, /conf/
```
`.htaccess`. A plaintext file appeared, and there it was 4th part: `3s_2_lO0k`

### Step 5: The macOS “Store” Twist
The final hint read: *“I love making websites on my Mac. I can Store a lot of information there.”*

I paused at the **“Store”** hint — its capitalization felt deliberate, but my first thought was Apple’s Mac App Store. 
I typed in mac store in google and got the App Store homepage—definitely not what I needed. 
I spent days Googling every variation (“mac store hack,” “mac web dev store,” etc.) and kept hitting dead ends.

**.DS_Store** —the hidden macOS metadata file.Rather than just grab the answer, I dove into researching .
DS_Store itself and learned that it exposes file metadata and directory listings—an easy way for attackers to gather information.

With that lesson under my belt, I visited /.DS_Store and uncovered the final flag fragment: 
`Congrats! You completed the scavenger hunt. Part 5: _7a46d25d}`

Full Flag Revealed: **picoCTF{th4ts_4_l0t_0f_pl4c3s_2_lO0k_d375c750}**

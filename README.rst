njaXt
^^^^^
A GUI tool for finding XSS

Installation
------------
``$ pip3 install njaxt``

Usage
-----

Development Setup
-----------------
.. code-block::

  git clone https://github.com/ujjwal96/njaXt.git
  cd njaXt
  ./setup.sh
  source venv/bin/activate

FAQ
---
*What is XSS?*
Cross-site scripting attacks (XSS) are a type of web based attack where malicious scripts are injected into a trusted website and run client side without the user knowing.
The end user's browser has no idea that an attack is taking place since it runs all the code being sent by the compromised website, which makes the attack extremely powerful.
Because the browser thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained and used within that site.

*How does XSS work?*
Cross-site scripting attacks may occur anywhere that possibly malicious users are allowed to post unregulated material to a trusted web site for the consumption of other valid users.
They come in two main forms, stored and reflected:
Stored attacks, or persistent attacks, are where the malicious code is stored on the target server via a DB or log and retrieved automatically.
This form is rather intuitive. Whenever the user requests data from the server that includes the stored information they are exposed to the malicious code.

Reflected XSS attacks, or non-persistent, occur when the code is executed when the malicious script is "reflected" off the server and back to the client as part of an input request by the user.
For example, if a user clicks on a malicious link, the reflected XSS code is sent alongside the client requested to the server, which is then reflected back to the client browser. Since the server is trusted the client browser executes the script.

*Oh no! What can be done to prevent XSS type attacks?*
Finding XSS flaws can be difficult since attacks can be inserted anywhere input from an HTTP requested is introduced.
One key step is to only allow untrusted data inputs in allowed locations and use escape clauses elsewhere. Also being sure to sanitize user inputs via special libraries is a good idea.
A comprehensive list can be found at [owasp.org](https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet).

*What is njaXt?*
njaXt (notjustanotherXSStool) is a tool designed to detect XSS vulnerabilities in websites. It comes with a GUI to allow everyone access to its features.
njaXt leverages PyQt5 to fuzz test websites against common XSS attack vectors. Fuzzing is the process of providing unexpected or invalid inputs into a computer program to test for bugs and other issues.
njaXt uses a list of expressions as a payload to use during the fuzzing process. These expressions show up as a "Wordlist" in the GUI and can be read and edited by the user. More advanced fuzzing options exists as well.
njaXt determines if an XSS vulnerability exists on a particular website using GET/POST requests, and if it does, returns the details of the particular vulnerability.

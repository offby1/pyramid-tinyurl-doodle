Not as hard as I thought!

https://go-acme.github.io/lego/ was genuinely easy to use.

It's one of about a bazillion options listed [here](https://letsencrypt.org/docs/client-options/); I can't remember how I chose it.

    # 2019-03-31T01:48:26+0000
    $ curl -Ls https://api.github.com/repos/xenolf/lego/releases/latest | grep browser_download_url | grep linux_amd64 | cut -d '"' -f 4 | wget -i -
    $ tar xf lego_v2.4.0_linux_amd64.tar.gz
    $ sudo mv lego /usr/local/bin/lego

    $ sudo lego --tls --email="eric.hanchrow@gmail.com" --domains="teensy.info" --path="/etc/lego" run

did what it's sposed to.

The certs expire quickly: currently the cert looks like

    Certificate:
        Data:
            Version: 3 (0x2)
            Serial Number:
                03:6a:02:0b:17:0e:da:7c:9b:f5:87:f0:3f:08:0f:22:89:e3
        Signature Algorithm: sha256WithRSAEncryption
            Issuer: C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
            Validity
                Not Before: Mar 31 04:09:55 2019 GMT
                Not After : Jun 29 04:09:55 2019 GMT

To renew (I did this once) I think it's something like

    $ sudo -s
    # cd /etc/lego
    # ./renew-certificate.sh

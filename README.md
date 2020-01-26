# chime.py

Play doorbell chimes in response to an HTTP request.

## Details

This is a simple Python script which runs a small HTTP server and listens for requests to play
a doorbell chime. Actually it doesn't have to be a doorbell chime, but that's what I use it for.

You just need to make some minimal customizations to `config.yml` to tell the script about the
doorbell chimes it should play and maybe set up a few other options, and then run the script:

```
chime.py config.yml
```

Configuration options are listed in the `config.yml` file, but they're really simple.

There's a sample unit definition to run the script as a service, if you're using `systemd`.

## Triggering the doorbell

HTTP requests should look like this:

```
http://<address>:<port>/chime?type=<chime_type>
```

`chime_type` refers to one of the types of chimes you define in `config.yml`; it determines what
audio file will be played.

## FAQ

### What are the requirements?

Python 3.x, `pygame`, and `PyYAML`, and a sound setup supported by `pygame`. It probably works on
Windows or Linux, but I've only tested Linux.

### Does it work with Python 2.7?

Doubt it.

### Is there any security on the web server.

Nope. I run this on my LAN and I don't really need any security. It doesn't have any encryption
nor support any authentication.

### Can I use this with IFTTT?

There's no authentication or security of any sort, so I wouldn't recommend exposing it to the
Internet, no.

### I ignored your advice and now hackers are making my doorbell ring 24/7. What do?

I can't even.

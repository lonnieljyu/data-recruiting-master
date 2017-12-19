# OrderGroove Data Engineer Test

## High Level

Hi there, in this test you'll be provided a simple flask app and giving it a new data backend - we've provided a naive reference implementation. For your convenience, we've provided a `Vagrantfile` with provisioning scripts to help you get started. Using vagrant is *optional* and you may freely use the platform of your choice, so long as you provide some extra details on your system to help us evaluate your submission.

Time spent should be less than four hours.

#### The exercise

1. Make any helpful changes to the database or data models as you see fit, probably depends on point (3) below.
2. Write any interface code required for the 4 API endpoints.
3. Specifically: for the `GET @ /dashboard/symbol/<symbol>` endpoint, use one of these technologies:
    1. elasticsearch
    2. mongodb
    3. rabbitmq
    4. redis
    5. neo4j
    6. some other 'nosql' or 'Big Data' tech. The ones above are already installed via `vagrant up` for your convenience. If you're unsure whether something you want to use qualifies just send us a note.

We also installed MariaDB for you with user `og`, password `og` and all privileges on database `og`. Whatever, naming is hard.

#### The Rules

1. The only changes allowed in `server/app.py` are to the `data_interface` assignment L7-8, ie by assigning a new `DataInterface` implementation. Your `DataInterface` implementation does not need to be 1-to-1 with any particular technology.
2. No changes allowed to `client/client.py`, `server/data_interface.py`, `server/sqlite_interface.py`, `server/initdb.py`.
3. Your implementation should mirror the interface described in `server/data_interface:DataInterface`.
4. All required system changes (`pip install`, `apt-get install`, `mkdir`, config changes, etc) must be reproducible on our end with either a simple `vagrant up` or detailed in sufficient documentation.

Note that there is a `requirements.txt` file located in `/vagrant/`, feel free to modify and use this in your provision scripts. It may be especially helpful if you decide to not use vagrant.

## The Details

The server's job is pretty simple: just respond to 4 types of requests, 2 for interacting with the client and 2 for the "business user" via a dashboard.

#### Client interaction

The main interaction with the client is as follows:

1. `POST @ /initial`. This is the request that initiates any contact between a client and our little app. The client provides some id (`uuid.uuid4`) and a "symbol", which is just any char in `[a-z]`. The role of the server is to respond with it's 'best guess' at whether the symbol is a vowel (yeah it's a silly model).
2. The client (already implemented in `client.py`) takes a look at what the server has said and decides whether it wants to keep talking. It's a bit mercurial but if it does then
3. `POST @/followup`. This one just has the client `uuid`; the client doesn't resend its `symbol`.

#### Dashboard

The server is also responsible for backstopping a dashboard with some simple aggregates.

* `GET @ /dashboard/symbol/<symbol>` where `symbol` in `[a-z]`. The response should provide the following summary statistics relating to requests around `<symbol>`, e.g. for some fake data w symbol `e`:

    ```javascript
        {
          'count': 3650,
          'symbol': u'e',
          'earliest': u'2017-06-28 19:34:14.486693',
          'latest': u'2017-06-29 13:15:01.173535',
          'followups': 65
        }
    ```
* `GET @ /dashboard/range/<lower>/<upper>`, where `lower` and `upper` are date strings. Get summaries within the given date range:
    ```javascript
        [
          {
            'count': 3650,
            'symbol': u'a',
            'earliest': u'2017-06-28 17:34:14.486693',
            'latest': u'2017-06-29 13:15:01.173535',
            'followups': 65
          },
          {
            'count': 1250,
            'symbol': u'b',
            'earliest': u'2017-06-28 19:34:14.486693',
            'latest': u'2017-06-29 12:15:01.173535',
            'followups': 25
          },
          ...
      ]
    ```


#### The interfaces

You are given `server/app.py` which is a Flask app that hooks into a database interface subclassing `server/data_interface.py:DataInterface` (or whatever you want, ducktyping etc). We've provided two example interfaces: `NullInterface` and `SQLiteInterface`. `NullInterface` literally does nothing and is only useful for benchmarking an upper bound on your speed. `SQLiteInterface` does as suggested.

All of this is to say that there's room for improvement.

## Getting started

#### Optional: vagrant

First, install [vagrant](https://www.vagrantup.com/). Then run these lines and go get some coffee (this takes 10-15 minutes):

```
> vagrant up
> vagrant ssh
```

You could speed up future builds using `vagrant package` or something but that's probably more trouble than it's worth. It'll take quite a while just to build the `package.box` file. Maybe if you want to reuse our fancy provisioning scripts for yourself in the future or something?

Anyway, your app and client now live under `/vagrant/app/`.

#### Without vagrant

You'll need to install everything on your own. Also, you'll have to change some hard-coded paths in `initdb.py`, `sqlite_interface.py` and the `FLASK_APP` environmental variable.

#### In general...

To run the app,

```
> flask run -h 0.0.0.0
```

And the client (change the path if you're not using vagrant).

```
> python /vagrant/app/client/client.py
```

The client only uses 2 of 4 routes. To see the response from the `dashboard` routes, we have set up a private network with your VM accesible @ 192.168.50.4. Not on vagrant? Use `localhost` instead.

```
> flask run -h 0.0.0.0
[In your browser or postman etc] 192.168.50.4:5000/dashboard/symbol/e
```

#### Note on using vagrant

Using vagrant is *optional* and is provided as a convenience for you. If you don't use it just let us know any important details about the platform/system you did your work on.

Since we want to be able to launch your solution via a simple `vagrant up`, we recommend periodically upgrading your provisioning scripts with any changes and running `vagrant destroy && vagrant up`. This way you can help guarantee your VM is free from ad hoc changes that aren't preserved in the provisioning process and which would prevent us from launching on our end. Sad!

One common tactic when using vagrant is to put all your code within a shared folder. This makes it simultaneously accessible to your favorite editor/IDE and executable within your VM. By default, the folder containing your `Vagrantfile` is shared in your VM under `/vagrant/`.

Any provisioning scripts that need to be executed from userspace should have the `privileged: false` flag in `Vagrantfile`. Without this flag all scripts run as root.

## Your Solution

#### Requirements

1. All endpoints work and provide accurate data.
2. The raw event data must still be stored/accessible for future analysis lol. Tell us where to find this in your writeup.
3. Either it just works with `vagrant up` or has suitable system documentation.

#### Submission format

Just send us any new files and (optionally) your modified `Vagrantfile` with any extra instructions. Please also provide a brief discussion of the motivations behind your decisions.

#### Evaluation

We will evaluate this using the following criterion (shown in priority order):

1. *Design decisions.* What changes you made and why. This includes evaluating the performance and scalability of your design. `SQLiteInterface` is pretty bad, how much better can you do?
2. *Requirements met.* See above.
3. *Code quality.* Did you write efficient queries, create [easy to read code](https://xkcd.com/1513/), etc?
4. *Documentation.* As necessary.

We will definitely accept partial solutions.
